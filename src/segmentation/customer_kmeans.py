"""Customer segmentation for Stage 2 Task 2. No mutation of shared input data."""
from pathlib import Path
from itertools import combinations
import hashlib
import json
import platform
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
import joblib
from sklearn.cluster import KMeans
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from threadpoolctl import threadpool_limits

NUMERIC = ['Recency', 'Frequency', 'Monetary', 'Mean_Discount_Ratio']
CATEGORICAL = ['Gender', 'City']
SEED = 42

def load_and_audit(path):
    df = pd.read_csv(path)
    required = ['Transaction_ID','Customer_ID','Transaction_Date','Revenue','Quantity',
                'Unit_Price_VND','Discount_Ratio','Age','Gender','City']
    missing = sorted(set(required) - set(df.columns))
    if missing:
        raise ValueError(f'Thiếu cột: {missing}')
    if df[required].isna().any().any():
        raise ValueError('Cột cốt lõi bị thiếu; cần giải thích và xử lý trước khi gom cụm.')
    if df['Transaction_ID'].duplicated().any():
        raise ValueError('Transaction_ID trùng, có nguy cơ đếm giao dịch nhiều lần.')
    dates = pd.to_datetime(df.Transaction_Date, errors='raise')
    if not np.isfinite(df[['Revenue','Quantity','Unit_Price_VND','Discount_Ratio','Age']].to_numpy()).all():
        raise ValueError('Có giá trị không hữu hạn.')
    if (df.Revenue < 0).any() or (df.Quantity <= 0).any() or not df.Discount_Ratio.between(0,1).all():
        raise ValueError('Giá trị doanh thu/số lượng/tỷ lệ giảm không hợp lệ.')
    inconsistent = df.groupby('Customer_ID')[['Age','Gender','City']].nunique().gt(1).sum()
    if inconsistent.any():
        raise ValueError(f'Thuộc tính khách không nhất quán: {inconsistent.to_dict()}')
    audit = {'rows':len(df),'columns':len(df.columns),'customers':df.Customer_ID.nunique(),
             'missing_by_column':df.isna().sum()[lambda s:s>0].to_dict(),
             'revenue_formula_mismatch':int((~np.isclose(df.Revenue,df.Quantity*df.Unit_Price_VND)).sum()),
             'date_min':str(dates.min()),'date_max':str(dates.max()),
             'input_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest()}
    return df, audit

def build_customers(df, reference_date=None):
    dates = pd.to_datetime(df.Transaction_Date, errors='raise')
    reference = pd.Timestamp(reference_date) if reference_date else dates.max().normalize()+pd.Timedelta(days=1)
    if (dates >= reference).any():
        raise ValueError('Chỉ dùng giao dịch trước mốc tham chiếu; chọn snapshot phù hợp.')
    work = df.assign(_date=dates)
    c = work.groupby('Customer_ID',sort=True).agg(
        Last_Purchase=('_date','max'), Frequency=('Transaction_ID','nunique'),
        Monetary=('Revenue','sum'), Mean_Discount_Ratio=('Discount_Ratio','mean'),
        Total_Quantity=('Quantity','sum'), Mean_Rating=('Rating','mean'),
        Age=('Age','first'), Gender=('Gender','first'), City=('City','first'))
    c['Recency'] = (reference-c.Last_Purchase).dt.total_seconds()/86400
    c['Average_Transaction_Value'] = c.Monetary/c.Frequency
    c = c.reset_index()
    assert c.Customer_ID.is_unique and len(c)==df.Customer_ID.nunique()
    assert c[NUMERIC].notna().all().all()
    return c, str(reference)

def make_preprocessor(demographics=False):
    log_pipe = Pipeline([('impute',SimpleImputer(strategy='median')),
                         ('log',FunctionTransformer(np.log1p,feature_names_out='one-to-one')),
                         ('scale',StandardScaler())])
    ratio_pipe = Pipeline([('impute',SimpleImputer(strategy='median')),('scale',StandardScaler())])
    transformers = [('log_numeric',log_pipe,['Recency','Frequency','Monetary']),
                    ('ratio',ratio_pipe,['Mean_Discount_Ratio'])]
    if demographics:
        transformers.append(('categorical',Pipeline([
            ('impute',SimpleImputer(strategy='most_frequent')),
            ('onehot',OneHotEncoder(handle_unknown='ignore',sparse_output=False))]),CATEGORICAL))
    return ColumnTransformer(transformers,remainder='drop',sparse_threshold=0)

def prepare_spaces(customers):
    pre = make_preprocessor(); X=pre.fit_transform(customers)
    # Refit PCA on customer-level features. Do not use transaction-level Task 1 model.
    pca = PCA(n_components=.90,svd_solver='full'); Z=pca.fit_transform(X)
    return pre,pca,{'non_PCA':X,'PCA':Z}

def evaluate_k(spaces):
    rows=[]; models={}
    with threadpool_limits(limits=1):
        for name,X in spaces.items():
            for k in range(1,11):
                start=time.perf_counter()
                model=KMeans(n_clusters=k,n_init=30,random_state=SEED).fit(X)
                labels=model.labels_; counts=np.bincount(labels,minlength=k)
                rows.append({'space':name,'K':k,'WCSS':model.inertia_,
                    'Silhouette_native':silhouette_score(X,labels) if k>1 else np.nan,
                    'Silhouette_common':silhouette_score(spaces['non_PCA'],labels) if k>1 else np.nan,
                    'smallest_cluster_fraction':counts.min()/len(X),
                    'seconds':time.perf_counter()-start})
                models[(name,k)]=model
    return pd.DataFrame(rows),models

def choose_models(metrics,spaces,models):
    decisions=[]
    for name in spaces:
        m=metrics[metrics.space==name].sort_values('K')
        x=(m.K.to_numpy()-1)/9
        y=(m.WCSS.to_numpy()-m.WCSS.iloc[-1])/(m.WCSS.iloc[0]-m.WCSS.iloc[-1])
        elbow=int(m.iloc[np.argmax((1-x)-y)].K)
        candidates=m[(m.K>=2)&(m.smallest_cluster_fraction>=.02)]
        if candidates.empty:
            candidates=m[m.K>=2]
        near=candidates[candidates.Silhouette_native>=candidates.Silhouette_native.max()-.02].copy()
        near['elbow_distance']=(near.K-elbow).abs()
        selected=near.sort_values(['elbow_distance','K']).iloc[0]
        k=int(selected.K); X=spaces[name]
        with threadpool_limits(limits=1):
            labels=[KMeans(n_clusters=k,n_init=30,random_state=s).fit_predict(X) for s in [7,21,42,84,123]]
        stability=[adjusted_rand_score(a,b) for a,b in combinations(labels,2)]
        decisions.append({**selected.drop(labels=['elbow_distance']).to_dict(),
                          'K':k,'elbow_K':elbow,'seed_ARI_mean':np.mean(stability),
                          'seed_ARI_min':np.min(stability)})
    summary=pd.DataFrame(decisions)
    # Common feature space is used to compare different representations.
    eligible=summary[summary.Silhouette_common>=summary.Silhouette_common.max()-.01]
    winner='non_PCA' if 'non_PCA' in eligible.space.values else eligible.sort_values('Silhouette_common',ascending=False).iloc[0].space
    k=int(summary.set_index('space').loc[winner,'K'])
    return summary,winner,k,models[(winner,k)]

def demographic_sensitivity(customers,base_labels,k):
    pre=make_preprocessor(demographics=True)
    X=pre.fit_transform(customers)
    with threadpool_limits(limits=1):
        model=KMeans(n_clusters=k,n_init=30,random_state=SEED).fit(X)
        score=silhouette_score(X,model.labels_)
    return {'features':'4 behavioral + one-hot Gender, City','dimensions':X.shape[1],
            'K':k,'ARI_vs_selected_behavioral':adjusted_rand_score(base_labels,model.labels_),
            'Silhouette_native':score,
            'note':'Sensitivity only; a different feature definition, not evidence of improvement.'}

def make_profiles(customers,labels):
    c=customers.copy(); c['Cluster_Label']=labels
    med=c.groupby('Cluster_Label')[NUMERIC].median()
    # Stable human-readable ordering by median spend, not raw arbitrary KMeans labels.
    order=med.Monetary.sort_values().index.tolist()
    mapping={int(raw):i for i,raw in enumerate(order)}
    c.Cluster_Label=c.Cluster_Label.map(mapping)
    profile=c.groupby('Cluster_Label').agg(
        Customers=('Customer_ID','size'),Recency_median=('Recency','median'),
        Frequency_median=('Frequency','median'),Monetary_median=('Monetary','median'),
        Monetary_mean=('Monetary','mean'),Discount_median=('Mean_Discount_Ratio','median'),
        Revenue_total=('Monetary','sum'),Age_median=('Age','median'),Rating_mean=('Mean_Rating','mean'))
    profile['Customer_share']=profile.Customers/len(c)
    names={int(i):f'Nhóm {int(i)+1} — mức chi tiêu trung vị hạng {int(i)+1}/{len(profile)}' for i in profile.index}
    c['Cluster_Name']=c.Cluster_Label.map(names)
    return c,profile,mapping,names

def save_figures(metrics,summary,spaces,pca,customers,models,profile,outdir):
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    paths=[]
    def save(name):
        p=outdir/name;plt.tight_layout();plt.savefig(p,dpi=150,bbox_inches='tight');plt.close();paths.append(p)
    fig,axes=plt.subplots(2,2,figsize=(12,8))
    for i,name in enumerate(spaces):
        m=metrics[metrics.space==name]; decision=summary.set_index('space').loc[name]
        axes[i,0].plot(m.K,m.WCSS,'o-');axes[i,0].axvline(decision.elbow_K,ls='--',c='orange',label='Elbow heuristic')
        axes[i,0].axvline(decision.K,ls=':',c='black',label='Chosen K');axes[i,0].legend()
        axes[i,0].set(title=f'{name}: Elbow',xlabel='K',ylabel='WCSS (within representation)')
        axes[i,1].plot(m.K,m.Silhouette_native,'o-',label='Native space')
        axes[i,1].plot(m.K,m.Silhouette_common,'s--',label='Common behavioral space')
        axes[i,1].axvline(decision.K,ls=':',c='black');axes[i,1].legend()
        axes[i,1].set(title=f'{name}: Silhouette',xlabel='K',ylabel='Silhouette')
    save('01_elbow_silhouette.png')
    full=PCA().fit(spaces['non_PCA']);ev=np.cumsum(full.explained_variance_ratio_)
    plt.figure(figsize=(7,4));plt.plot(np.arange(1,len(ev)+1),ev,'o-');plt.axhline(.9,ls='--');plt.xticks(range(1,len(ev)+1))
    plt.xlabel('Number of components');plt.ylabel('Cumulative explained variance');plt.title('Customer-level PCA')
    save('02_pca_variance.png')
    view=PCA(n_components=2).fit(spaces['non_PCA']);coords=view.transform(spaces['non_PCA'])
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    for ax,(name,X) in zip(axes,spaces.items()):
        k=int(summary.set_index('space').loc[name,'K']);labels=models[(name,k)].labels_
        points=ax.scatter(coords[:,0],coords[:,1],c=labels,cmap='tab10',s=12,alpha=.55)
        handles, legend_labels = points.legend_elements()
        ax.legend(handles, legend_labels, title='Raw cluster')
        ax.set(title=f'{name}, K={k} (raw labels)',xlabel='PC1',ylabel='PC2')
    fig.suptitle(f'Same 2D projection; retained variance {view.explained_variance_ratio_.sum():.1%}')
    save('03_clusters_common_projection.png')
    fig,axes=plt.subplots(1,2,figsize=(12,5))
    for label,g in customers.groupby('Cluster_Label'):
        axes[0].scatter(g.Frequency,g.Monetary,s=14,alpha=.4,label=f'Cluster {label}')
        axes[1].scatter(g.Recency,g.Monetary,s=14,alpha=.4,label=f'Cluster {label}')
    for ax,x in zip(axes,['Frequency (transactions)','Recency (days)']):
        ax.set_yscale('log');ax.set(xlabel=x,ylabel='Monetary (VND, log scale)');ax.legend()
    save('04_selected_customer_segments.png')
    profile.Customers.plot.bar(figsize=(7,4),color='#2878a0');plt.xlabel('Cluster label');plt.ylabel('Customers');plt.title('Selected cluster sizes')
    save('05_cluster_sizes.png')
    return paths

def predict_customers(bundle,features):
    for c in NUMERIC:
        if c not in features or features[c].isna().any() or not np.isfinite(features[c]).all():
            raise ValueError(f'Đặc trưng không hợp lệ: {c}')
    if (features[['Recency','Monetary']]<0).any().any() or (features.Frequency<1).any() or not features.Mean_Discount_Ratio.between(0,1).all():
        raise ValueError('Đặc trưng nằm ngoài miền hợp lệ.')
    raw=bundle['pipeline'].predict(features)
    return np.array([bundle['label_mapping'][int(x)] for x in raw])

def export_results(root,df,customers,metrics,summary,winner,k,pre,pca,model,profile,mapping,names,reference,audit,sensitivity):
    root=Path(root);data_dir=root/'data/final/task2';report_dir=root/'report/task2';model_dir=root/'src/models'
    for p in [data_dir,report_dir,model_dir]:p.mkdir(parents=True,exist_ok=True)
    steps=[('preprocessor',pre)]
    if winner=='PCA':steps.append(('pca',pca))
    steps.append(('kmeans',model));pipeline=Pipeline(steps)
    bundle={'pipeline':pipeline,'label_mapping':mapping,'cluster_names':names,
            'feature_names':NUMERIC,'reference_date':reference,'window_start':audit['date_min'],
            'selected_space':winner,'K':k,'source_sha256':audit['input_sha256'],
            'versions':{'python':platform.python_version(),'sklearn':sklearn.__version__,'numpy':np.__version__,'pandas':pd.__version__},
            'usage':'Input: one row per customer with NUMERIC columns; aggregate the same observation window. Use label_mapping after pipeline.predict.',
            'limitations':'Synthetic, exploratory full-snapshot clustering; no independent generalization estimate.'}
    model_path=model_dir/'customer_kmeans_bundle.joblib';joblib.dump(bundle,model_path)
    loaded=joblib.load(model_path)
    assert np.array_equal(predict_customers(loaded,customers),customers.Cluster_Label.to_numpy())
    labels=customers[['Customer_ID','Cluster_Label','Cluster_Name']]
    merged=df.merge(labels,on='Customer_ID',how='left',validate='many_to_one',sort=False)
    assert len(merged)==len(df) and merged.Transaction_ID.is_unique and merged.Cluster_Label.notna().all()
    assert merged.Transaction_ID.tolist()==df.Transaction_ID.tolist()
    customers.to_csv(data_dir/'customer_segments.csv',index=False,encoding='utf-8-sig')
    merged.to_csv(data_dir/'transactions_with_clusters.csv',index=False,encoding='utf-8-sig')
    metrics.to_csv(report_dir/'k_search_metrics.csv',index=False)
    summary.to_csv(report_dir/'model_comparison.csv',index=False)
    profile.to_csv(report_dir/'cluster_profiles.csv',encoding='utf-8-sig')
    payload={'audit':audit,'reference_date':reference,'selected_space':winner,'K':k,
             'pca_components':int(pca.n_components_),'retained_variance':float(pca.explained_variance_ratio_.sum()),
             'sensitivity':sensitivity,'versions':bundle['versions']}
    (report_dir/'run_summary.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2,default=lambda x:x.item() if hasattr(x,'item') else str(x)))
    assert hashlib.sha256((root/'data/final/cleaned_dataset.csv').read_bytes()).hexdigest()==audit['input_sha256']
    return bundle,merged
