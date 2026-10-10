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
- [x] Thu thập dữ liệu từ ít nhất 02 nguồn khác nhau (Tesco UK và Tiki VN).
- [x] Mỗi nguồn dữ liệu có tối thiểu 300 records.
- [x] Chuẩn hóa tên cột.
- [x] Chuẩn hóa kiểu dữ liệu.
- [x] Hỗ trợ quy đổi tiền tệ sang VND để đồng nhất (Script của Vị trí 2 hỗ trợ).
- [x] Lưu dữ liệu nguồn vào `data/raw/`.
- [x] Lưu dữ liệu sau chuẩn hóa vào `data/processed/`.

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
- [x] Lấy danh sách `Product_ID` hợp lệ từ dữ liệu Static đã chuẩn hóa.
- [x] Sinh thông tin khách hàng (Customer_ID, Gender, Age, City) và thời gian giao dịch.
- [x] Tạo `Quantity` và tính toán `Revenue` hợp lý (`Revenue = Quantity * Discount_Price`).
- [x] Tạo `Rating` (từ 1–5).
- [x] Dùng Ollama sinh `Customer_Review` tương ứng với `Rating`.
- [x] Lưu Dynamic Data vào `data/processed/dynamic_transactions.csv`.

---

## Bước 3: Tích hợp Dữ liệu (Data Integration)
[↩️ Xem mục lục](https://github.com/Myracc248/data-analysis-ai-nhom11/blob/main/README.md#-b%C6%B0%E1%BB%9Bc-3-t%C3%ADch-h%E1%BB%A3p-d%E1%BB%AF-li%E1%BB%87u-data-integration)
**Đảm nhiệm:** Hà Xuân Khoa (Nhóm trưởng)

> **Nguyên tắc cốt lõi:** Bước này CHỈ thực hiện đồng bộ cấu trúc (Schema Alignment) và gộp bảng. **TUYỆT ĐỐI KHÔNG** tự ý xóa dữ liệu (`dropna`) hay điền khuyết (`fillna`) để giảm Missing Values.

### 3.1 Vertical Concatenation — `pd.concat()`
[↩️ Xem mục lục](https://github.com/Myracc248/data-analysis-ai-nhom11/blob/main/README.md#31-vertical-concatenation--pdconcat)
- [x] Đọc 02 nguồn Static (`tesco_products_vnd.csv` và `vietnamese_tiki_products_backpacks_suitcases.csv` từ thư mục `processed`).
- [x] Kiểm tra tên cột và kiểu dữ liệu đảm bảo khớp Schema 6 cột.
- [x] Sử dụng `pd.concat()` để nối dữ liệu theo chiều dọc tạo thành `Unified Static Master Table`.
- [x] Kiểm tra tính duy nhất của `Product_ID`, đảm bảo không có ID trùng lặp từ 2 nguồn.

### 3.2 Horizontal Merging — `pd.merge()`
[↩️ Xem mục lục](https://github.com/Myracc248/data-analysis-ai-nhom11/blob/main/README.md#32-horizontal-merging--pdmerge)
- [x] Merge bảng `Unified Static Master` với `dynamic_transactions.csv`.
- [x] Sử dụng **LEFT JOIN** với bảng gốc bên trái là Dynamic Data để bảo toàn 100% giao dịch thực tế.
- [x] Kiểm tra số lượng giao dịch trước và sau Merge (đảm bảo không bị nhân bản dòng).
- [x] Xuất dataset tích hợp cuối cùng vào `data/final/master_dataset.csv`.

---

## 🗄️ Bước 4: Lưu trữ Cơ sở dữ liệu (Modern Data Storage)
**Đảm nhiệm:** Phan Chí Thanh (Vị trí 3)

### Yêu cầu hành động
- [x] Lựa chọn tối thiểu 02 hệ quản trị/công nghệ Database (MongoDB Atlas, Vector DB, hoặc SQL).
- [x] Thiết kế cấu trúc lưu trữ phù hợp.
- [x] Viết script nạp `master_dataset.csv` vào Database.
- [x] Viết script kết nối và truy xuất dữ liệu từ CSDL về Python cho EDA.
- [x] Giải thích lý do lựa chọn mô hình lưu trữ trong báo cáo.

---

## 🧹 Bước 5: Làm sạch Dữ liệu & EDA
**Đảm nhiệm:** Nguyễn Huỳnh Thanh Tuấn (Vị trí 4) & Nguyễn Vương Quốc Tuấn (Vị trí 5)

### 5.1 Data Cleaning & Missing Value Strategy
- [x] Kiểm tra kích thước, cấu trúc và kiểu dữ liệu.
- [x] Đánh giá số lượng và tỷ lệ Missing Values của từng cột.
- [x] Trực quan hóa Missing Values bằng thư viện `missingno`.
- [x] Phân tích cơ chế thiếu dữ liệu (MCAR / MAR / MNAR).
- [x] Lựa chọn phương pháp xử lý Imputation phù hợp (Mean, Median, Mode, Unknown). Giải thích rõ lý do nếu dùng `dropna()`.
- [x] So sánh phân phối dữ liệu Before / After Imputation.
- [x] Phát hiện Outliers bằng IQR / Z-score và xử lý (Drop/Clip) tùy đặc điểm biến.

### 5.2 Exploratory Data Analysis (EDA)
- [x] Phân tích Univariate (Thống kê mô tả, phân phối).
- [x] Phân tích Bivariate/Multivariate và ma trận tương quan (Correlation Heatmap).
- [x] Vẽ tối thiểu **05 biểu đồ** bằng Matplotlib / Seaborn (đầy đủ Title, X/Y labels).
- [x] Viết nhận xét/insight giải thích dưới mỗi biểu đồ. Phân biệt rõ Correlation và Causation.
- [x] Xác định các yếu tố nổi bật liên quan đến Revenue, Rating, và Customer Segmentation.
- [x] Đề xuất Feature cho Stage 2.

---

# 🟩 STAGE 2 — MACHINE LEARNING & DEPLOYMENT

## 1. 📌 Tổng quan Stage 2
Stage 2 sử dụng dữ liệu đã được làm sạch và tiền xử lý từ Stage 1 để xây dựng, đánh giá và triển khai các mô hình Machine Learning. 

Dữ liệu đầu vào chính là tập dataset dùng chung cho toàn bộ nhóm:
> 📁 `data/final/cleaned_dataset.csv`

**Luồng hình thành dữ liệu:**
Raw Data ➔ Static + Dynamic Data ➔ Data Integration ➔ Master Dataset ➔ Database ➔ Cleaning & EDA ➔ **`cleaned_dataset.csv`**

Stage 2 bao gồm 5 Task chính. Mỗi Task sẽ tự thực hiện các bước Feature Engineering và Preprocessing cần thiết cho bài toán tương ứng, đồng thời tuân thủ nguyên tắc tránh Data Leakage. Cuối cùng, nhóm sẽ tổng hợp kết quả, so sánh hiệu năng và đưa ra các đề xuất kinh doanh thực tế (Business Recommendations).

---

## 2. 👥 Phân công Stage 2

| Vị trí | Thành viên | Nhiệm vụ chính (Stage 2) |
| :--- | :--- | :--- |
| **Vị trí 0** | **Hà Xuân Khoa** | Task 5 — Web UI + Final Integration |
| **Vị trí 1** | **Vương Quốc Tiến** | Task 1 — PCA |
| **Vị trí 2** | **Nguyễn Tuấn Duy** | Task 2 — K-Means |
| **Vị trí 3** | **Phan Chí Thanh** | Final Integration, Insight Review & Support |
| **Vị trí 4** | **Nguyễn Huỳnh Thanh Tuấn** | Task 3 — Regression |
| **Vị trí 5** | **Nguyễn Vương Quốc Tuấn** | Task 4 — Classification |

---

## 🧩 Task 1: Unsupervised Learning — PCA
**Đảm nhiệm:** Vương Quốc Tiến (Vị trí 1)
**Mục tiêu:** Áp dụng phân tích thành phần chính (PCA) để giảm số chiều dữ liệu nhưng vẫn giữ lại phần lớn lượng thông tin.

- [x] Chọn các đặc trưng dạng số (numerical features) phù hợp.
- [x] **Feature Scaling:** Bắt buộc chuẩn hóa dữ liệu trước khi chạy PCA bằng `StandardScaler` hoặc `MinMaxScaler`.
- [x] Áp dụng PCA và tính toán tỷ lệ phương sai giải thích tích lũy (Cumulative Explained Variance).
- [x] Chọn số lượng component tối thiểu để giữ lại **85%–95%** phương sai.
- [x] **Trực quan hóa:** Vẽ biểu đồ Explained Variance và Scatter plot 2D/3D cho không gian PCA.
- [x] Giải thích lý do chọn số lượng component và phân tích kết quả PCA.

---

## 👥 Task 2: Customer Segmentation — K-Means
**Đảm nhiệm:** Nguyễn Tuấn Duy (Vị trí 2)
**Mục tiêu:** Áp dụng thuật toán gom cụm K-Means để nhận diện các nhóm khách hàng/sản phẩm/giao dịch nổi bật.

- [x] **Feature Preparation:** Encode các biến Categorical và Scale các biến Numerical phù hợp cho thuật toán đo khoảng cách.
- [x] Xác định số cụm tối ưu ($K$) bằng cả 2 phương pháp: **Elbow Method (WCSS)** và **Silhouette Score**.
- [x] **So sánh mô hình:** Chạy và so sánh kết quả K-Means trên tập dữ liệu đã qua PCA vs tập dữ liệu gốc chưa qua PCA (non-PCA).
- [x] **Trực quan hóa:** Vẽ Scatter plot 2D/3D tô màu theo cụm.
- [x] Map nhãn `Cluster_Label` ngược lại vào primary dataset để phân tích đặc điểm từng cụm.

---

## 📈 Task 3: Supervised Learning — Regression
**Đảm nhiệm:** Nguyễn Huỳnh Thanh Tuấn (Vị trí 4)
**Mục tiêu:** Xây dựng mô hình hồi quy để dự đoán biến mục tiêu liên tục: **`Revenue`** (Doanh thu).

- [x] **Feature Preparation:** Tạo các đặc trưng thời gian (Feature Engineering) phù hợp từ cột `Transaction_Date` như: Tháng, Ngày trong tuần và Cuối tuần.
- [x] **Train/Test Split:** Thực hiện chia tập dữ liệu. Đảm bảo các bước preprocessing không gây rò rỉ dữ liệu (data leakage).
- [x] **So sánh mô hình:** Huấn luyện và so sánh `LinearRegression` vs `DecisionTreeRegressor`.
- [x] Đánh giá mô hình bằng các chỉ số: **MSE, RMSE, R²**.
- [x] **Trực quan hóa:** Vẽ biểu đồ Actual vs Predicted hoặc Residual plot. Xác định mô hình hiệu năng tốt nhất.

---

## 🏷️ Task 4: Supervised Learning — Classification
**Đảm nhiệm:** Nguyễn Vương Quốc Tuấn (Vị trí 5)
**Mục tiêu:** Xây dựng mô hình phân lớp dự đoán một biến mục tiêu rời rạc (được định nghĩa từ kết quả EDA).

- [x] **Feature Engineering:** Tạo biến, Binning (phân nhóm), Encoding và lựa chọn đặc trưng cho bài toán phân lớp.
- [x] **Class Imbalance:** Kiểm tra phân phối class. Nếu mất cân bằng, áp dụng `class_weight='balanced'` hoặc kỹ thuật sampling phù hợp, đảm bảo việc xử lý không gây Data Leakage.
- [x] **So sánh mô hình:** Huấn luyện và so sánh `LogisticRegression` vs `DecisionTreeClassifier`.
- [x] Đánh giá mô hình bằng: **Accuracy, Precision, Recall, F1-score**, và in ra toàn bộ `classification_report`.
- [x] **Trực quan hóa:** Vẽ Confusion Matrix dưới dạng Heatmap. Xác định mô hình hiệu năng tốt nhất.

---

## 🖥️ Task 5: Web UI & Model Deployment
**Đảm nhiệm:** Hà Xuân Khoa (Vị trí 0)
**Mục tiêu:** Xây dựng ứng dụng Web tương tác để người dùng sử dụng các mô hình Machine Learning đã huấn luyện.

- [ ] Xây dựng Web UI bằng framework **Streamlit**.
- [ ] Thiết kế giao diện nhập liệu (Input fields) và hiển thị kết quả dự đoán rõ ràng.
- [ ] Thêm Tab Trực quan hóa (Optional): Hiển thị biểu đồ PCA hoặc K-Means cluster.
> 💡 *Technical Choice (Lựa chọn triển khai của nhóm):* Để Web UI chạy trực tiếp mà không cần train lại, các mô hình và preprocessor ở Task 1-4 sau khi huấn luyện xong sẽ được export (bằng `joblib` hoặc `pickle`) và lưu vào thư mục `src/models/`.

---

## 📊 Documentation & Business Recommendations (Báo cáo & Đề xuất)
*Nhiệm vụ chung toàn nhóm sau khi hoàn thành Task 1-5.*

- **[ ] Phân tích PCA:** Giải thích số component giữ lại, phương sai đạt được và đóng góp của PCA vào bài toán.
- **[ ] Phân tích K-Means:** Đánh giá Elbow/Silhouette, giải thích ý nghĩa các cụm và sự khác biệt giữa có PCA/không PCA.
- **[ ] Đánh giá Regression:** Tuyên bố rõ mô hình chiến thắng (*Best Regression Model: ...*) kèm chứng minh từ Metrics.
- **[ ] Đánh giá Classification:** Tuyên bố rõ mô hình chiến thắng (*Best Classification Model: ...*) kèm phân tích dựa trên Precision, Recall, Accuracy và F1-score.
- **[ ] Giao diện UI:** Bổ sung hình ảnh (screenshots) của app hoạt động thực tế.
- **[ ] Business Recommendations:** Dựa vào insight từ EDA và Model, đưa ra **2–3 đề xuất kinh doanh thực tế, dựa trên dữ liệu** thay vì lý thuyết sáo rỗng.

---

## 🔄 Stage 2 Workflow

```text
                  cleaned_dataset.csv
                         │
        ┌────────────────┼────────────────┐
        │                │                │               │
        ▼                ▼                ▼               ▼
     Task 1            Task 2           Task 3          Task 4
      PCA             K-Means         Regression    Classification
        │                │                │               │
        └────────────────┴───────┬────────┴───────────────┘
                                 │
                                 ▼
                          Task 5 — Web UI
                                 │
                                 ▼
                   Documentation & Final Insights
                                 │
                                 ▼
                     Business Recommendations
(Ghi chú: Các Task từ 1-4 chạy song song và độc lập. Mỗi Task tự chịu trách nhiệm tiền xử lý (Preprocessing) và Feature Engineering theo yêu cầu riêng, sử dụng chung nguồn đầu vào cleaned_dataset.csv và tuân thủ quy tắc chống Data Leakage).

📁 Cấu trúc Thư mục Stage 2
Plaintext
project/
├── data/
│   ├── raw/
│   ├── processed/
│   └── final/
│       ├── master_dataset.csv
│       └── cleaned_dataset.csv         ← Dữ liệu đầu vào cho Stage 2
│
├── notebooks/                          ← Notebook của các Tasks tương ứng
│   ├── 01_static_data.ipynb
│   ├── 02_dynamic_data.ipynb
│   ├── 03_data_integration.ipynb
│   ├── 04_database.ipynb
│   ├── 05_cleaning_eda.ipynb
│   │
│   ├── 06_pca.ipynb                    (Task 1 - Vị trí 1)
│   ├── 07_kmeans.ipynb                 (Task 2 - Vị trí 2)
│   ├── 08_regression.ipynb             (Task 3 - Vị trí 4)
│   └── 09_classification.ipynb         (Task 4 - Vị trí 5)
│── report/                             ← Báo cáo của nhóm
├── src/
│   ├── crawler/
│   ├── data_generation/
│   ├── integration/
│   ├── database/
│   └── models/                         ← Chứa các model (.pkl) đã train xong
│
├── app.py                              (Task 5 - Vị trí 0)
└── README.md
