# 📊 Phân tích Dữ liệu Hệ thống Bán lẻ & Thương mại Điện tử

## 1. 📌 Tổng quan Dự án

Dự án thuộc môn học Nhập môn Phân tích Dữ liệu & AI, tập trung vào việc thu thập, tích hợp, làm sạch, lưu trữ, phân tích khám phá dữ liệu (EDA) và xây dựng các mô hình Machine Learning trên dữ liệu bán lẻ & thương mại điện tử.

Dữ liệu được xây dựng từ nhiều nguồn Static và Dynamic nhằm mô phỏng một hệ thống bán lẻ có cả:
- Thông tin sản phẩm.
- Thông tin giao dịch.
- Thông tin khách hàng.
- Đánh giá và phản hồi của khách hàng.

### 1.1. Mục tiêu phân tích
Phân tích các yếu tố có liên hệ với doanh thu và mức độ hài lòng của khách hàng đối với các mặt hàng bán lẻ & thương mại điện tử, từ đó xác định các xu hướng và nhóm khách hàng có hành vi mua sắm nổi bật.

- **Đối tượng phục vụ:** Ban giám đốc / Giám đốc sản phẩm của hệ thống bán lẻ để hỗ trợ phân tích hành vi khách hàng, chiến lược giá và nhập hàng.
- **Thước đo thành công:** Khám phá được ít nhất 3 tập khách hàng hoặc 3 yếu tố có mối liên hệ đáng chú ý với hành vi mua hàng, doanh thu hoặc mức độ hài lòng.

### 1.2. Biến mục tiêu (Target Variables)
- **Biến mục tiêu chính:** `Rating` (mức độ hài lòng của khách hàng).
- **Biến mục tiêu cho Regression:** `Revenue` (doanh thu giao dịch).
- **Biến mục tiêu cho Classification:** Sẽ được xác định sau EDA và Feature Engineering.

---

## 2. 👥 Danh sách Thành viên & Phân công

| Vị trí | Thành viên | Nhiệm vụ chính |
| :--- | :--- | :--- |
| **Vị trí 0** | **Hà Xuân Khoa** | Nhóm trưởng, quản lý tiến độ và tích hợp dữ liệu (Step 3). |
| **Vị trí 1** | **Vương Quốc Tiến** | Thu thập và chuẩn hóa Static Data. |
| **Vị trí 2** | **Nguyễn Tuấn Duy** | Sinh Dynamic Data & Script đồng bộ quy đổi tỷ giá. |
| **Vị trí 3** | **Phan Chí Thanh** | Xây dựng và quản lý Modern Database. |
| **Vị trí 4** | **Nguyễn Huỳnh Thanh Tuấn** | Data Cleaning và xử lý dữ liệu nâng cao. |
| **Vị trí 5** | **Nguyễn Vương Quốc Tuấn** | EDA và Visualization. |

---

# 🟦 STAGE 1 — DATA PREPARATION & ANALYSIS

## 🗂️ Bước 1: Thu thập Dữ liệu Tĩnh (Static Data)
**Đảm nhiệm:** Vương Quốc Tiến (Vị trí 1)

### Yêu cầu hành động
- [ ] Thu thập dữ liệu từ ít nhất 02 nguồn khác nhau (Tesco UK và Tiki VN).
- [ ] Mỗi nguồn dữ liệu có tối thiểu 300 records.
- [ ] Chuẩn hóa tên cột.
- [ ] Chuẩn hóa kiểu dữ liệu.
- [ ] Hỗ trợ quy đổi tiền tệ sang VND để đồng nhất (Script của Vị trí 2 hỗ trợ).
- [ ] Lưu dữ liệu nguồn vào `data/raw/`.
- [ ] Lưu dữ liệu sau chuẩn hóa vào `data/processed/`.

### 📌 Schema Static Data chuẩn (Hợp đồng dữ liệu)
Các nguồn Static bắt buộc phải được chuẩn hóa theo bộ thuộc tính cốt lõi sau trước khi mang đi Integration:
| Tên cột | Mô tả |
| :--- | :--- |
| **Product_ID** | Khóa chính (Primary Key) của sản phẩm. |
| **Product_Name** | Tên sản phẩm. |
| **Category** | Danh mục sản phẩm. |
| **Brand** | Thương hiệu sản phẩm. |
| **Original_Price** | Giá gốc của sản phẩm. |
| **Discount_Price** | Giá sau khi áp dụng khuyến mãi. |

---

## ⚙️ Bước 2: Sinh Dữ liệu Động (Dynamic Data)
**Đảm nhiệm:** Nguyễn Tuấn Duy (Vị trí 2)

### Yêu cầu hành động
Dùng thư viện Python (`Faker`, `NumPy`) và LLM/Ollama để giả lập dữ liệu giao dịch:
- [ ] Lấy danh sách `Product_ID` hợp lệ từ dữ liệu Static đã chuẩn hóa.
- [ ] Sinh thông tin khách hàng (Customer_ID, Gender, Age, City) và thời gian giao dịch.
- [ ] Tạo `Quantity` và tính toán `Revenue` hợp lý (`Revenue = Quantity * Discount_Price`).
- [ ] Tạo `Rating` (từ 1–5).
- [ ] Dùng Ollama sinh `Customer_Review` tương ứng với `Rating`.
- [ ] Lưu Dynamic Data vào `data/processed/dynamic_transactions.csv`.

---

## Bước 3: Tích hợp Dữ liệu (Data Integration)
[↩️ Xem mục lục](https://github.com/Myracc248/data-analysis-ai-nhom11/blob/main/README.md#-b%C6%B0%E1%BB%9Bc-3-t%C3%ADch-h%E1%BB%A3p-d%E1%BB%AF-li%E1%BB%87u-data-integration)
**Đảm nhiệm:** Hà Xuân Khoa (Nhóm trưởng)

> **Nguyên tắc cốt lõi:** Bước này CHỈ thực hiện đồng bộ cấu trúc (Schema Alignment) và gộp bảng. **TUYỆT ĐỐI KHÔNG** tự ý xóa dữ liệu (`dropna`) hay điền khuyết (`fillna`) để giảm Missing Values.

### 3.1 Vertical Concatenation — `pd.concat()`
[↩️ Xem mục lục](https://github.com/Myracc248/data-analysis-ai-nhom11/blob/main/README.md#31-vertical-concatenation--pdconcat)
- [ ] Đọc 02 nguồn Static (`tesco_products_vnd.csv` và `vietnamese_tiki_products_backpacks_suitcases.csv` từ thư mục `processed`).
- [ ] Kiểm tra tên cột và kiểu dữ liệu đảm bảo khớp Schema 6 cột.
- [ ] Sử dụng `pd.concat()` để nối dữ liệu theo chiều dọc tạo thành `Unified Static Master Table`.
- [ ] Kiểm tra tính duy nhất của `Product_ID`, đảm bảo không có ID trùng lặp từ 2 nguồn.

### 3.2 Horizontal Merging — `pd.merge()`
[↩️ Xem mục lục](https://github.com/Myracc248/data-analysis-ai-nhom11/blob/main/README.md#32-horizontal-merging--pdmerge)
- [ ] Merge bảng `Unified Static Master` với `dynamic_transactions.csv`.
- [ ] Sử dụng **LEFT JOIN** với bảng gốc bên trái là Dynamic Data để bảo toàn 100% giao dịch thực tế.
- [ ] Kiểm tra số lượng giao dịch trước và sau Merge (đảm bảo không bị nhân bản dòng).
- [ ] Xuất dataset tích hợp cuối cùng vào `data/final/master_dataset.csv`.

---

## 🗄️ Bước 4: Lưu trữ Cơ sở dữ liệu (Modern Data Storage)
**Đảm nhiệm:** Phan Chí Thanh (Vị trí 3)

### Yêu cầu hành động
- [ ] Lựa chọn tối thiểu 02 hệ quản trị/công nghệ Database (MongoDB Atlas, Vector DB, hoặc SQL).
- [ ] Thiết kế cấu trúc lưu trữ phù hợp.
- [ ] Viết script nạp `master_dataset.csv` vào Database.
- [ ] Viết script kết nối và truy xuất dữ liệu từ CSDL về Python cho EDA.
- [ ] Giải thích lý do lựa chọn mô hình lưu trữ trong báo cáo.

---

## 🧹 Bước 5: Làm sạch Dữ liệu & EDA
**Đảm nhiệm:** Nguyễn Huỳnh Thanh Tuấn (Vị trí 4) & Nguyễn Vương Quốc Tuấn (Vị trí 5)

### 5.1 Data Cleaning & Missing Value Strategy
- [ ] Kiểm tra kích thước, cấu trúc và kiểu dữ liệu.
- [ ] Đánh giá số lượng và tỷ lệ Missing Values của từng cột.
- [ ] Trực quan hóa Missing Values bằng thư viện `missingno`.
- [ ] Phân tích cơ chế thiếu dữ liệu (MCAR / MAR / MNAR).
- [ ] Lựa chọn phương pháp xử lý Imputation phù hợp (Mean, Median, Mode, Unknown). Giải thích rõ lý do nếu dùng `dropna()`.
- [ ] So sánh phân phối dữ liệu Before / After Imputation.
- [ ] Phát hiện Outliers bằng IQR / Z-score và xử lý (Drop/Clip) tùy đặc điểm biến.

### 5.2 Exploratory Data Analysis (EDA)
- [ ] Phân tích Univariate (Thống kê mô tả, phân phối).
- [ ] Phân tích Bivariate/Multivariate và ma trận tương quan (Correlation Heatmap).
- [ ] Vẽ tối thiểu **05 biểu đồ** bằng Matplotlib / Seaborn (đầy đủ Title, X/Y labels).
- [ ] Viết nhận xét/insight giải thích dưới mỗi biểu đồ. Phân biệt rõ Correlation và Causation.
- [ ] Xác định các yếu tố nổi bật liên quan đến Revenue, Rating, và Customer Segmentation.
- [ ] Đề xuất Feature cho Stage 2.

---

# 🟩 STAGE 2 — MACHINE LEARNING
Stage 2 sử dụng dữ liệu đã được làm sạch và chuẩn bị từ Stage 1 để xây dựng, đánh giá và triển khai các mô hình Machine Learning.

> **⚠️ QUY TẮC QUAN TRỌNG CHO STAGE 2:** 
> Tất cả các mô hình và transformer sau khi huấn luyện thành công **BẮT BUỘC** phải được export thành file `.pkl` (bằng `joblib` hoặc `pickle`). Các file này phải lưu trong thư mục `src/models/` để Web UI tải trực tiếp lên dự đoán, không train lại mô hình trên UI.

## ⚙️ Bước 6: Feature Engineering & Preprocessing
**Đảm nhiệm:** Phan Chí Thanh & Cả nhóm
- [ ] Kéo dữ liệu sạch từ CSDL.
- [ ] Xử lý biến `datetime` và tạo các đặc trưng thời gian nếu cần.
- [ ] Tạo các biến mới (Feature Engineering / Binning).
- [ ] Encoding các biến categorical và Scaling biến numerical.
- [ ] Chia dữ liệu thành Train / Test.
- [ ] Lưu các preprocessing transformer vào `src/models/`.

## 🧩 Bước 7: Unsupervised Learning — PCA
**Đảm nhiệm:** Vương Quốc Tiến (Vị trí 1)
- [ ] Áp dụng PCA để giảm số chiều dữ liệu.
- [ ] Tính Cumulative Explained Variance Ratio và chọn số lượng component đạt 85%–95% variance.
- [ ] Trực quan hóa dữ liệu PCA (Scatter plot 2D/3D).
- [ ] **Lưu PCA transformer thành `src/models/pca_transformer.pkl`.**

## 👥 Bước 8: Customer Segmentation — K-Means
**Đảm nhiệm:** Nguyễn Tuấn Duy (Vị trí 2)
- [ ] Sử dụng Elbow Method (WCSS) và Silhouette Score để xác định số cụm.
- [ ] So sánh clustering trên Original Features và PCA Features.
- [ ] Phân tích đặc điểm của từng cluster (nhóm khách hàng nổi bật).
- [ ] Gắn `Cluster_Label` vào dataset.
- [ ] **Lưu K-Means model thành `src/models/kmeans_model.pkl`.**

## 📈 Bước 9: Supervised Learning — Regression (Target: Revenue)
**Đảm nhiệm:** Nguyễn Huỳnh Thanh Tuấn (Vị trí 4)
- [ ] Train 02 mô hình: Linear Regression & Decision Tree Regressor.
- [ ] Đánh giá bằng MSE, RMSE, R² Score.
- [ ] Vẽ Actual vs Predicted và Residual Plot.
- [ ] Phân tích Feature Importance.
- [ ] **Lưu mô hình tốt nhất thành `src/models/regression_model.pkl`.**

## 🏷️ Bước 10: Supervised Learning — Classification
**Đảm nhiệm:** Nguyễn Vương Quốc Tuấn (Vị trí 5)
- [ ] Train 02 mô hình: Logistic Regression & Decision Tree Classifier.
- [ ] Kiểm tra phân bố class và xử lý Imbalance (SMOTE, class_weight).
- [ ] Đánh giá bằng Confusion Matrix, Accuracy, Precision, Recall, F1-Score.
- [ ] **Lưu mô hình tốt nhất thành `src/models/classification_model.pkl`.**

## 🖥️ Bước 11: Model Deployment & Web UI
**Đảm nhiệm:** Hà Xuân Khoa (Nhóm trưởng)
- Xây dựng Web UI bằng Streamlit.
- **Luồng xử lý:** Nhận User Input → Preprocessing → Load Model từ `src/models/` → Predict → Visualize.

## 📊 Bước 12: Model Comparison & Final Insights
**Đảm nhiệm:** Cả nhóm
- [ ] So sánh hiệu năng, phân tích ưu/nhược điểm các mô hình.
- [ ] Đưa ra 2–3 kiến nghị kinh doanh thực tế.
- [ ] Hoàn thiện báo cáo cuối cùng (.docx).

---

## 📁 Cấu trúc Thư mục (Project Structure)

```text
data-analysis-ai-nhom11/
│
├── data/
│   ├── raw/                    ← Dữ liệu gốc nguyên thủy (tesco-grocery-uk.csv, tiki.csv)
│   ├── processed/              ← Dữ liệu trung gian đã chuẩn hóa Schema/VND và Dynamic Data
│   └── final/                  ← Dataset master_dataset.csv đã tích hợp sẵn sàng cho EDA
│
├── notebooks/                  ← Toàn bộ quá trình thực hiện của từng bước
│   ├── 01_static_data.ipynb
│   ├── 02_dynamic_data.ipynb
│   ├── 03_data_integration.ipynb
│   ├── 04_database.ipynb
│   ├── 05_cleaning_eda.ipynb
│   └── 06_machine_learning.ipynb
│
├── src/
│   ├── data_generation/        ← Code script hỗ trợ giả lập dữ liệu (Duy)
│   │   ├── standardize_currency.py
│   │   ├── generate_review_bank.py
│   │   └── generate_dynamic_data.py
│   ├── database/               ← Script thao tác với MongoDB / SQL (Thanh)
│   └── models/                 ← Chứa các model và transformer đã train (.pkl)
│       ├── pca_transformer.pkl
│       ├── kmeans_model.pkl
│       ├── regression_model.pkl
│       └── classification_model.pkl
│
├── app.py                      ← Streamlit Web UI (Load trực tiếp từ src/models/)
├── README.md
└── report/
    └── Bao_cao_nhom11.docx     ← Báo cáo cuối

    RAW DATA
   │
   ▼
data/raw/
   │
   ▼
STATIC / DYNAMIC PROCESSING
   │
   ▼
data/processed/
   │
   ▼
STEP 3 — DATA INTEGRATION (pd.concat -> pd.merge)
   │
   ▼
data/final/master_dataset.csv
   │
   ├──────────────► DATABASE
   │
   └──────────────► CLEANING + EDA
                          │
                          ▼
                   FEATURE ENGINEERING
                          │
                          ▼
                     MACHINE LEARNING
                          │
                          ▼
                       WEB UI
