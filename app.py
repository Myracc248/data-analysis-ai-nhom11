from datetime import date, datetime, time
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st

from src.segmentation.customer_kmeans import predict_customers


ROOT_DIR = Path(__file__).resolve().parent
MODEL_DIR = ROOT_DIR / "src" / "models"

st.set_page_config(
    page_title="Retail & E-commerce ML",
    page_icon="🛍️",
    layout="wide",
)


@st.cache_resource
def load_models():
    model_paths = {
        "pca": MODEL_DIR / "pca_model.joblib",
        "regression": MODEL_DIR / "regression_model.joblib",
        "classification": MODEL_DIR / "best_classification_pipeline.joblib",
        "segmentation": MODEL_DIR / "customer_kmeans_bundle.joblib",
    }
    missing = [str(path.relative_to(ROOT_DIR)) for path in model_paths.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(
            "Thiếu model đã train: "
            + ", ".join(missing)
            + ". Hãy đặt các artifact vào src/models/ trước khi chạy ứng dụng."
        )
    return {name: joblib.load(path) for name, path in model_paths.items()}


def age_group(age: int) -> str:
    groups = pd.cut(
        pd.Series([age]),
        bins=[0, 25, 40, 60, 100],
        labels=["Young", "Adult", "Middle_Aged", "Senior"],
    )
    return str(groups.iloc[0])


def quantity_group(quantity: int) -> str:
    groups = pd.cut(
        pd.Series([quantity]),
        bins=[0, 1, 3, 10, 100],
        labels=["Single", "Small", "Medium", "Bulk"],
    )
    return str(groups.iloc[0])


def build_classification_features(
    age: int,
    quantity: int,
    original_price: float,
    discount_ratio: float,
    gender: str,
    city: str,
    category: str,
    source: str,
) -> pd.DataFrame:
    discount_price = original_price * (1 - discount_ratio)
    unit_price = discount_price
    return pd.DataFrame(
        [
            {
                "Age": age,
                "Quantity": quantity,
                "Unit_Price_VND": unit_price,
                "Revenue": unit_price * quantity,
                "Original_Price_VND": original_price,
                "Discount_Price_VND": discount_price,
                "Discount_Amount": original_price - discount_price,
                "Discount_Percentage": discount_ratio * 100,
                "Discount_Ratio": discount_ratio,
                "Gender": gender,
                "City": city,
                "Category": category,
                "Source": source,
                "Age_Group": age_group(age),
                "Quantity_Group": quantity_group(quantity),
            }
        ]
    )


def build_regression_features(
    original_price: float,
    discount_ratio: float,
    age: int,
    transaction_date: date,
) -> pd.DataFrame:
    day_of_week = transaction_date.weekday()
    return pd.DataFrame(
        [
            {
                "Original_Price_VND": original_price,
                "Discount_Ratio": discount_ratio,
                "Age": age,
                "Month": transaction_date.month,
                "DayOfWeek": day_of_week,
                "Is_Weekend": int(day_of_week >= 5),
            }
        ]
    )


def build_pca_features(
    age: int,
    quantity: int,
    original_price: float,
    discount_ratio: float,
    transaction_datetime: datetime,
    feature_names: list[str],
) -> pd.DataFrame:
    discount_price = original_price * (1 - discount_ratio)
    month_position = transaction_datetime.month - 1
    weekday_position = transaction_datetime.weekday()
    hour_position = transaction_datetime.hour + transaction_datetime.minute / 60
    features = {
        "Age": age,
        "Quantity": quantity,
        "Original_Price_VND": np.log1p(original_price),
        "Discount_Price_VND": np.log1p(discount_price),
        "Discount_Ratio": discount_ratio,
        "Month_sin": np.sin(2 * np.pi * month_position / 12),
        "Month_cos": np.cos(2 * np.pi * month_position / 12),
        "Weekday_sin": np.sin(2 * np.pi * weekday_position / 7),
        "Weekday_cos": np.cos(2 * np.pi * weekday_position / 7),
        "Hour_sin": np.sin(2 * np.pi * hour_position / 24),
        "Hour_cos": np.cos(2 * np.pi * hour_position / 24),
    }
    return pd.DataFrame([[features[name] for name in feature_names]], columns=feature_names)


@st.cache_data
def load_pca_background(
    dataset_path: str,
    model_path: str,
    dataset_mtime_ns: int,
    model_mtime_ns: int,
) -> pd.DataFrame:
    del dataset_mtime_ns, model_mtime_ns
    dataset_file = Path(dataset_path)
    model_file = Path(model_path)
    if not dataset_file.is_file():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu PCA: {dataset_file}")
    if not model_file.is_file():
        raise FileNotFoundError(f"Không tìm thấy model PCA: {model_file}")

    model_bundle = joblib.load(model_file)
    transactions = pd.read_csv(dataset_file)
    required_columns = [*model_bundle["pca_features"], "Transaction_Date"]
    missing_columns = sorted(set(required_columns) - set(transactions.columns))
    if missing_columns:
        raise ValueError(f"Dataset PCA thiếu cột: {missing_columns}")

    features = transactions[model_bundle["pca_features"]].copy()
    features["Original_Price_VND"] = np.log1p(features["Original_Price_VND"])
    features["Discount_Price_VND"] = np.log1p(features["Discount_Price_VND"])

    transaction_dates = pd.to_datetime(transactions["Transaction_Date"], errors="coerce")
    cyclic_features = {
        "Month": (transaction_dates.dt.month - 1, 12),
        "Weekday": (transaction_dates.dt.dayofweek, 7),
        "Hour": (
            transaction_dates.dt.hour + transaction_dates.dt.minute / 60,
            24,
        ),
    }
    for feature_name, (position, period) in cyclic_features.items():
        features[f"{feature_name}_sin"] = np.sin(2 * np.pi * position / period)
        features[f"{feature_name}_cos"] = np.cos(2 * np.pi * position / period)

    features = features[model_bundle["feature_names"]]
    imputed = model_bundle["imputer"].transform(features)
    scaled = model_bundle["scaler"].transform(imputed)
    components = model_bundle["pca"].transform(scaled)
    if not np.isfinite(components[:, :2]).all():
        raise ValueError("Phép chiếu PCA của dataset tạo ra tọa độ không hữu hạn.")

    return pd.DataFrame({"PC1": components[:, 0], "PC2": components[:, 1]})


def render_classification(model_bundle) -> None:
    st.subheader("Dự đoán đánh giá cao")
    st.caption(
        "Phân loại Rating >= 4 (1) hay dưới 4 (0). Các biến giá, doanh thu và nhóm tuổi/số lượng "
        "được tạo theo đúng cách notebook Task 4 đã huấn luyện."
    )
    with st.form("classification_form"):
        first, second, third = st.columns(3)
        age = first.number_input("Tuổi", min_value=1, max_value=100, value=30)
        quantity = second.number_input("Số lượng", min_value=1, max_value=100, value=2)
        original_price = third.number_input(
            "Giá gốc (VND)", min_value=0.0, value=250_000.0, step=10_000.0
        )

        first, second, third = st.columns(3)
        discount_percent = first.slider("Giảm giá (%)", 0.0, 100.0, 10.0, 1.0)
        gender = second.selectbox("Giới tính", ["Female", "Male"])
        source = third.selectbox("Nguồn", ["Tiki", "Tesco"])

        first, second = st.columns(2)
        city = first.text_input("Thành phố", value="TP. Hồ Chí Minh")
        category = second.text_input("Danh mục sản phẩm", value="Thời Trang")
        submitted = st.form_submit_button("Dự đoán Rating")

    if submitted:
        features = build_classification_features(
            age=age,
            quantity=quantity,
            original_price=original_price,
            discount_ratio=discount_percent / 100,
            gender=gender,
            city=city.strip(),
            category=category.strip(),
            source=source,
        )
        prediction = int(model_bundle["pipeline"].predict(features)[0])
        if prediction == 1:
            st.success("Mô hình dự đoán: **Rating cao (4–5 sao)**")
        else:
            st.info("Mô hình dự đoán: **Rating chưa cao (1–3 sao)**")

        pipeline = model_bundle["pipeline"]
        if hasattr(pipeline, "predict_proba"):
            probabilities = pipeline.predict_proba(features)[0]
            class_values = pipeline.classes_
            st.metric(
                "Độ tin cậy của lớp dự đoán",
                f"{probabilities[list(class_values).index(prediction)]:.1%}",
            )
        st.caption(
            f"Mô hình: {model_bundle['best_model_name']} · "
            f"Macro-F1 khi đánh giá: {model_bundle['macro_f1']:.3f}. "
            "Dữ liệu được mô phỏng; kết quả chỉ mang tính tham khảo."
        )


def render_regression(model) -> None:
    st.subheader("Dự đoán doanh thu giao dịch")
    st.caption("Nhập thông tin sản phẩm, khách hàng và ngày giao dịch.")
    with st.form("regression_form"):
        first, second, third = st.columns(3)
        original_price = first.number_input(
            "Giá gốc (VND)", min_value=0.0, value=250_000.0, step=10_000.0
        )
        discount_percent = second.slider("Giảm giá (%)", 0.0, 100.0, 10.0, 1.0)
        age = third.number_input("Tuổi khách hàng", min_value=1, max_value=100, value=30)
        transaction_date = st.date_input("Ngày giao dịch", value=date.today())
        submitted = st.form_submit_button("Dự đoán doanh thu")

    if submitted:
        features = build_regression_features(
            original_price, discount_percent / 100, age, transaction_date
        )
        prediction = float(model.predict(features)[0])
        st.metric("Doanh thu dự đoán", f"{prediction:,.0f} VND")
        st.caption(
            "Mô hình hồi quy được nạp từ src/models/regression_model.joblib; "
            "kết quả trên dữ liệu mô phỏng chỉ mang tính tham khảo."
        )


def render_segmentation(model_bundle) -> None:
    st.subheader("Phân khúc khách hàng")
    st.caption(
        "Các chỉ số cần tổng hợp ở cấp khách hàng trong cùng một cửa sổ quan sát; "
        "không nhập một giao dịch đơn lẻ."
    )
    with st.form("segmentation_form"):
        first, second = st.columns(2)
        recency = first.number_input("Recency (ngày từ lần mua gần nhất)", min_value=0.0, value=30.0)
        frequency = second.number_input("Frequency (số giao dịch)", min_value=1, value=3)
        first, second = st.columns(2)
        monetary = first.number_input("Monetary (tổng chi tiêu, VND)", min_value=0.0, value=1_000_000.0, step=50_000.0)
        discount_ratio = second.slider("Tỷ lệ giảm giá trung bình", 0.0, 1.0, 0.1, 0.01)
        submitted = st.form_submit_button("Xác định phân khúc")

    if submitted:
        customer_features = pd.DataFrame(
            [
                {
                    "Recency": recency,
                    "Frequency": frequency,
                    "Monetary": monetary,
                    "Mean_Discount_Ratio": discount_ratio,
                }
            ]
        )
        cluster = int(predict_customers(model_bundle, customer_features)[0])
        cluster_name = model_bundle["cluster_names"][cluster]
        st.success(f"Phân khúc dự đoán: **{cluster_name}**")
        st.caption(
            f"K={model_bundle['K']} · Không gian đầu vào: {model_bundle['selected_space']}. "
            f"Dữ liệu và phân khúc mang tính khám phá, được xây dựng trên dữ liệu mô phỏng."
        )


def render_pca(model_bundle) -> None:
    st.subheader("Phân tích thành phần chính (PCA)")
    st.caption(
        "PCA chuyển các đặc trưng giao dịch thành các thành phần chính; "
        "đây là phép giảm chiều, không phải mô hình dự đoán nhãn."
    )
    with st.form("pca_form"):
        first, second, third = st.columns(3)
        age = first.number_input("Tuổi khách hàng", min_value=1, max_value=100, value=30)
        quantity = second.number_input("Số lượng", min_value=1, max_value=100, value=2)
        original_price = third.number_input(
            "Giá gốc (VND)", min_value=0.0, value=250_000.0, step=10_000.0
        )
        first, second = st.columns(2)
        discount_percent = first.slider("Giảm giá (%)", 0.0, 100.0, 10.0, 1.0, key="pca_discount")
        transaction_date = second.date_input("Ngày giao dịch", value=date.today(), key="pca_date")
        transaction_time = st.time_input("Giờ giao dịch", value=time(12, 0))
        submitted = st.form_submit_button("Tính các thành phần PCA")

    if submitted:
        features = build_pca_features(
            age,
            quantity,
            original_price,
            discount_percent / 100,
            datetime.combine(transaction_date, transaction_time),
            model_bundle["feature_names"],
        )
        transformed = model_bundle["scaler"].transform(
            model_bundle["imputer"].transform(features)
        )
        components = model_bundle["pca"].transform(transformed)[0]
        component_names = [f"PC{i + 1}" for i in range(len(components))]

        st.subheader("1. Tọa độ thành phần chính của input")
        st.dataframe(
            pd.DataFrame({"Thành phần": component_names, "Giá trị": components}),
            hide_index=True,
            width="stretch",
        )

        st.subheader("2. Explained variance của model đã train")
        st.metric(
            "Phương sai tích lũy giữ lại khi train",
            f"{model_bundle['cumulative_explained_variance']:.2%}",
        )
        variance = pd.DataFrame(
            {
                "Thành phần": component_names,
                "Phương sai giải thích": model_bundle["explained_variance_ratio"],
            }
        ).set_index("Thành phần")
        st.bar_chart(variance)

        st.subheader("3. Vị trí input trên mặt phẳng PC1–PC2")
        dataset_path = ROOT_DIR / "data" / "final" / "cleaned_dataset.csv"
        model_path = MODEL_DIR / "pca_model.joblib"
        background = load_pca_background(
            str(dataset_path),
            str(model_path),
            dataset_path.stat().st_mtime_ns,
            model_path.stat().st_mtime_ns,
        )
        figure, axis = plt.subplots(figsize=(9, 5))
        axis.scatter(
            background["PC1"],
            background["PC2"],
            color="#2878a0",
            alpha=0.28,
            s=14,
            label="Giao dịch trong cleaned_dataset.csv",
        )
        axis.scatter(
            components[0],
            components[1],
            color="#e63946",
            edgecolor="black",
            linewidth=1,
            marker="*",
            s=300,
            zorder=3,
            label="Input hiện tại",
        )
        axis.annotate(
            "Input hiện tại",
            (components[0], components[1]),
            xytext=(8, 8),
            textcoords="offset points",
            fontweight="bold",
        )
        explained_variance = model_bundle["explained_variance_ratio"]
        axis.set(
            xlabel=f"PC1 ({explained_variance[0]:.2%} explained variance)",
            ylabel=f"PC2 ({explained_variance[1]:.2%} explained variance)",
            title="Input và giao dịch đã chiếu bằng cùng PCA đã train",
        )
        axis.grid(alpha=0.2)
        axis.legend()
        figure.tight_layout()
        st.pyplot(figure)
        plt.close(figure)
        st.caption(
            "Điểm nền là giao dịch thật trong cleaned_dataset.csv; "
            "điểm input được biến đổi bằng cùng feature schema, imputer, scaler và PCA. "
            "Tọa độ PC chỉ biểu diễn vị trí trong không gian PCA, không phải dự đoán hay độ chính xác."
        )


def main() -> None:
    st.title("Phân tích dữ liệu bán lẻ & thương mại điện tử")
    st.write(
        "Ứng dụng sử dụng các model đã train trong `src/models/` để phân tích PCA, "
        "dự đoán doanh thu/đánh giá và phân khúc khách hàng."
    )
    models = load_models()

    pca_tab, segmentation_tab, regression_tab, classification_tab = st.tabs(
        ["PCA", "K-Means", "Regression", "Classification"]
    )
    with pca_tab:
        render_pca(models["pca"])
    with segmentation_tab:
        render_segmentation(models["segmentation"])
    with regression_tab:
        render_regression(models["regression"])
    with classification_tab:
        render_classification(models["classification"])


if __name__ == "__main__":
    main()
