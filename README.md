# data-analysis-ai-nhom11

**Đề tài:** Phân tích Dữ liệu Hệ thống Bán lẻ & Thương mại Điện tử

Dự án thuộc môn học Nhập môn Phân tích Dữ liệu & AI, tập trung vào việc thu thập, tích hợp, làm sạch, lưu trữ, phân tích khám phá (EDA) và xây dựng các mô hình Machine Learning trên dữ liệu bán lẻ & thương mại điện tử.

---

## 👥 Danh sách Thành viên & Phân công

* **Vị trí 0 (Nhóm trưởng - Quản lý & Tích hợp):** Hà Xuân Khoa
* **Vị trí 1 (Thu thập Dữ liệu Tĩnh & Gộp):** Vương Quốc Tiến
* **Vị trí 2 (Giả lập Dữ liệu Động):** Nguyễn Tuấn Duy
* **Vị trí 3 (Quản trị CSDL Modern):** Phan Chí Thanh
* **Vị trí 4 (Làm sạch Dữ liệu Nâng cao):** Nguyễn Huỳnh Thanh Tuấn
* **Vị trí 5 (Phân tích EDA & Trực quan hóa):** Nguyễn Vương Quốc Tuấn

---

# 🟦 STAGE 1 — Data Collection, Wrangling & EDA

## 🎯 Bước 0: Định nghĩa Bài toán (Define the Question)

* **Mục tiêu phân tích (Analytical Goal):** Phân tích các yếu tố có liên hệ với doanh thu và mức độ hài lòng của khách hàng đối với các mặt hàng bán lẻ & thương mại điện tử, từ đó xác định các xu hướng và nhóm khách hàng có hành vi mua sắm nổi bật.
* **Đối tượng phục vụ (For Whom):** Ban giám đốc / Giám đốc sản phẩm của hệ thống bán lẻ để hỗ trợ phân tích hành vi khách hàng, chiến lược giá và nhập hàng.
* **Thước đo thành công (Success Metric):** Khám phá được ít nhất 3 tập khách hàng hoặc 3 yếu tố có mối liên hệ đáng chú ý với hành vi mua hàng, doanh thu hoặc mức độ hài lòng thông qua phân tích và trực quan hóa dữ liệu.
* **Biến mục tiêu chính:** `Rating` (mức độ hài lòng của khách hàng).
* **Biến mục tiêu cho Regression:** `Revenue` (doanh thu giao dịch).
* **Biến mục tiêu cho Classification:** Sẽ được xác định sau EDA và Feature Engineering.

> **Lưu ý:** Missing values tại biến mục tiêu sẽ được đánh giá riêng. Việc loại bỏ bản ghi (`dropna`) chỉ được thực hiện khi có lý do phân tích phù hợp; các biến còn lại sẽ áp dụng chiến lược điền khuyết (imputation) tương ứng với kiểu dữ liệu. Nghiêm cấm xóa dòng tùy tiện.

---

## 🗂️ Bước 1: Thu thập Dữ liệu Tĩnh (Static Data)
**Đảm nhiệm:** Vương Quốc Tiến (Vị trí 1)

### Yêu cầu
- [x ] Thu thập dữ liệu từ **ít nhất 2 nguồn khác nhau**.
- [x ] Mỗi nguồn dữ liệu đạt **tối thiểu 300 records**.
- [x ] Chuẩn hóa tên cột và kiểu dữ liệu giữa các nguồn.
- [x ] Kiểm tra dữ liệu trước khi sử dụng `pd.concat()`.
- [x ] Lưu dữ liệu gốc vào `data/raw/`.
- [x ] Lưu dữ liệu đã chuẩn hóa vào `data/processed/`.

---

## ⚙️ Bước 2: Tạo Dữ liệu Động (Dynamic Data)
**Đảm nhiệm:** Nguyễn Tuấn Duy (Vị trí 2)

### Yêu cầu
Dùng thư viện Python (`Faker`, `numpy`) và LLM/Ollama để giả lập dữ liệu giao dịch và đánh giá khách hàng.
- [ x] Tạo dữ liệu giao dịch.
- [ x] `Product_ID` phải được lấy từ danh sách `Product_ID` của dữ liệu Static.
- [x ] Tạo dữ liệu khách hàng và thời gian giao dịch.
- [x ] Tạo `Rating` từ 1 đến 5 và sinh `Customer_Review` tương ứng.
- [x ] Tạo `Quantity` và tính `Revenue`.
- [x ] Lưu Dynamic Data vào `data/processed/`.

---

## 🔗 Bước 3: Tích hợp Dữ liệu (Data Integration)
**Đảm nhiệm:** Hà Xuân Khoa (Nhóm trưởng)

### 3.1 Vertical Concatenation — `pd.concat()`
- [ ] Kiểm tra và đồng bộ tên cột, kiểu dữ liệu từ 2 nguồn Static.
- [ ] Sử dụng `pd.concat()` để tạo `Unified Static Master Table`.
- [ ] Lưu `Unified Static Master Table` vào `data/final/`.

### 3.2 Horizontal Merging — `pd.merge()`
- [ ] Merge `Unified Static Master Table` với Dynamic Transaction Data qua khóa `Product_ID`.
- [ ] Lựa chọn loại JOIN phù hợp (`Left Join`, `Inner Join`...) và giải thích trong báo cáo.
- [ ] Kiểm tra dữ liệu sau khi Merge.
- [ ] Lưu dataset tích hợp vào `data/final/`.

---

## 🗄️ Bước 4: Lưu trữ Cơ sở dữ liệu (Modern Data Storage)
**Đảm nhiệm:** Phan Chí Thanh (Vị trí 3)
> 🚧 *Đang thực hiện*
- [ ] Chọn 2 hệ cơ sở dữ liệu (MongoDB Atlas, Vector DB hoặc SQL).
- [ ] Thiết kế cấu trúc lưu trữ.
- [ ] Viết script nạp Master Dataset vào CSDL.
- [ ] Viết script kết nối và truy xuất dữ liệu từ CSDL về Python.
- [ ] Đảm bảo dữ liệu có thể được sử dụng cho EDA và Machine Learning.

---

## 🧹 Bước 5: Làm sạch Dữ liệu & EDA
**Đảm nhiệm:** Nguyễn Huỳnh Thanh Tuấn (Vị trí 4) & Nguyễn Vương Quốc Tuấn (Vị trí 5)
> 🚧 *Đang thực hiện*

### 5.1 Missing Value Strategy
- [ ] Đánh giá số lượng và tỷ lệ Missing Values của từng cột.
- [ ] Phân tích cơ chế Missing (MCAR / MAR / MNAR).
- [ ] Trực quan hóa Missing Values bằng thư viện `missingno`.
- [ ] Áp dụng chiến lược Imputation phù hợp.
- [ ] So sánh phân phối dữ liệu Before / After Imputation.

### 5.2 Univariate Analysis
- [ ] Tính thống kê mô tả.
- [ ] Kiểm tra phân phối dữ liệu.
- [ ] Phát hiện và xử lý Outliers bằng IQR / Z-score.
- [ ] Xem xét `drop`, `clip` hoặc các phương pháp xử lý phù hợp.

### 5.3 Multivariate Analysis
- [ ] Lập ma trận tương quan.
- [ ] Phân tích mối quan hệ giữa các biến.
- [ ] So sánh các nhóm phân loại với các biến số.

### 📊 Visualizations & Insights
- [ ] Vẽ tối thiểu 5 biểu đồ bằng Matplotlib / Seaborn.
- [ ] Biểu đồ có đầy đủ Title, X/Y labels.
- [ ] Giải thích Insight dưới mỗi biểu đồ.
- [ ] Phân biệt rõ correlation và causation.
- [ ] Xác định các feature phù hợp cho Stage 2.

---

# 🟩 STAGE 2 — Model Architecture & Evaluation
Stage 2 sử dụng dữ liệu đã được làm sạch và chuẩn bị từ Stage 1 để xây dựng, đánh giá và triển khai các mô hình Machine Learning.

## ⚙️ Bước 6: Feature Engineering & Preprocessing
**Đảm nhiệm:** Phan Chí Thanh (Kéo data từ DB) & Cả nhóm
- [ ] Kéo dữ liệu sạch từ CSDL.
- [ ] Xử lý biến `datetime`.
- [ ] Tạo các biến mới (Feature Engineering / Binning).
- [ ] Encoding các biến categorical.
- [ ] Chia dữ liệu thành Train / Test.
- [ ] Scaling các feature trước những thuật toán nhạy cảm với scale.
- [ ] Lưu các preprocessing transformer cần thiết để sử dụng lại khi Deployment.

---

## 🧩 Bước 7: Unsupervised Learning — PCA
**Đảm nhiệm:** Vương Quốc Tiến (Vị trí 1)
**Mục tiêu:** Giảm số chiều dữ liệu nhưng vẫn giữ lại phần lớn phương sai.
- [ ] Scale features bằng `StandardScaler` hoặc `MinMaxScaler`.
- [ ] Thực hiện PCA.
- [ ] Tính Cumulative Explained Variance Ratio.
- [ ] Chọn số lượng component giữ khoảng 85%–95% variance.
- [ ] Trực quan hóa dữ liệu PCA bằng scatter plot 2D/3D.
- [ ] **Lưu Scaler thành `scaler.pkl`.**
- [ ] **Lưu PCA transformer thành `pca.pkl`.**

---

## 👥 Bước 8: Customer Segmentation — K-Means
**Đảm nhiệm:** Nguyễn Tuấn Duy (Vị trí 2)
**Mục tiêu:** Phân nhóm khách hàng / sản phẩm có hành vi tương đồng.
- [ ] Xác định các feature sử dụng cho clustering.
- [ ] Sử dụng Elbow Method (WCSS) để khảo sát số cụm.
- [ ] Sử dụng Silhouette Analysis để đánh giá chất lượng phân cụm.
- [ ] So sánh clustering trên Original Features và PCA Features.
- [ ] Trực quan hóa các cụm.
- [ ] Gắn `Cluster_Label` vào dataset.
- [ ] **Lưu K-Means model thành `kmeans.pkl`.**

---

## 📈 Bước 9: Supervised Learning — Regression
**Đảm nhiệm:** Nguyễn Huỳnh Thanh Tuấn (Vị trí 4)
**Mục tiêu:** Dự đoán giá trị liên tục.
**Target:** `Revenue`
- [ ] Chuẩn bị Feature và Target.
- [ ] Chia Train / Test.
- [ ] Chạy và so sánh `Linear Regression` và `Decision Tree Regressor`.
- [ ] Đánh giá bằng MSE, RMSE, R² Score.
- [ ] Vẽ Actual vs Predicted và Residual Plot.
- [ ] Phân tích các lỗi và pattern trong dự đoán.
- [ ] **Lưu mô hình Regression phù hợp thành `regression.pkl`.**

---

## 🏷️ Bước 10: Supervised Learning — Classification
**Đảm nhiệm:** Nguyễn Vương Quốc Tuấn (Vị trí 5)
**Mục tiêu:** Dự đoán một biến phân loại được xác định sau EDA và Feature Engineering.
- [ ] Xác định Classification Target.
- [ ] Chuẩn bị Feature và Target.
- [ ] Chia Train / Test.
- [ ] Chạy và so sánh `Logistic Regression` và `Decision Tree Classifier`.
- [ ] Đánh giá bằng Confusion Matrix, Accuracy, Precision, Recall, F1-Score.
- [ ] Kiểm tra và xử lý Class Imbalance nếu cần.
- [ ] **Lưu mô hình Classification phù hợp thành `classification.pkl`.**

---

## 🖥️ Bước 11: Model Deployment & Web UI
**Đảm nhiệm:** Hà Xuân Khoa (Nhóm trưởng)
**Công cụ:** Streamlit

### Quy tắc Deployment
> **File `06_machine_learning.ipynb` là nơi thực hiện việc huấn luyện (train). Sau khi train thành công, BẮT BUỘC phải export cả model lẫn transformer thành file `.pkl`. File `app.py` (Web UI) CHỈ dùng để load các model/transformer đã được lưu sẵn này, tuyệt đối không train lại model trong giao diện.**

### Luồng xử lý UI

    User Input
        ↓
    Preprocessing
        ↓
    Loaded Model/Transformer
        ↓
    Model.predict()
        ↓
    Prediction / Visualization
        ↓
    Web UI

---

## 📊 Bước 12: Model Comparison & Final Insights
**Đảm nhiệm:** Cả nhóm
- [ ] So sánh hiệu năng các mô hình.
- [ ] Phân tích ưu / nhược điểm của từng mô hình.
- [ ] Tổng hợp kết quả từ PCA, K-Means, Regression và Classification.
- [ ] Đưa ra 2–3 kiến nghị thực tế cho doanh nghiệp dựa trên kết quả phân tích.
- [ ] Hoàn thiện báo cáo cuối cùng.

---

## 📁 Project Structure

    data-analysis-ai-nhom11/
    │
    ├── README.md
    │
    ├── data/
    │   ├── raw/                    ← Dữ liệu gốc chưa xử lý
    │   ├── processed/              ← Dữ liệu đã chuẩn hóa / tạo
    │   └── final/                  ← Dataset đã tích hợp, sẵn sàng cho EDA/ML
    │
    ├── notebooks/
    │   ├── 01_static_data.ipynb
    │   ├── 02_dynamic_data.ipynb
    │   ├── 03_data_integration.ipynb
    │   ├── 04_database.ipynb
    │   ├── 05_cleaning_eda.ipynb
    │   └── 06_machine_learning.ipynb ← Nơi thực hiện train model và export ra .pkl
    │
    ├── src/
    │   ├── data_generation/        ← Code tạo dữ liệu động
    │   ├── integration/            ← Code tích hợp dữ liệu
    │   ├── database/               ← Code kết nối / truy xuất CSDL
    │   └── models/                 ← Chứa các model và transformer đã train (.pkl)
    │       ├── scaler.pkl
    │       ├── pca.pkl
    │       ├── kmeans.pkl
    │       ├── regression.pkl
    │       └── classification.pkl
    │
    ├── app.py                      ← Streamlit Web UI (Chỉ load file .pkl để dự đoán)
    │
    └── report/
        └── Bao_cao_nhom11.docx     ← Báo cáo cuối

---

## 🔄 Tổng quan Pipeline

                     STAGE 1
    ┌─────────────────────────────────────────┐
    │ Data Collection                         │
    │       ↓                                 │
    │ Data Loading                            │
    │       ↓                                 │
    │ Data Integration (concat / merge)       │
    │       ↓                                 │
    │ Database Storage                        │
    │       ↓                                 │
    │ Data Cleaning                           │
    │       ↓                                 │
    │ EDA + Visualization                     │
    └──────────────────┬──────────────────────┘
                       │
                       ▼
                     STAGE 2
    ┌─────────────────────────────────────────┐
    │ Feature Engineering & Preprocessing     │
    │ (06_machine_learning.ipynb)             │
    │       ↓                                 │
    │ ┌─────────┬───────────┬──────────────┐  │
    │ │   PCA   │  K-Means  │ Supervised ML│  │
    │ └─────────┴───────────┴──────────────┘  │
    │       ↓                                 │
    │ Model Evaluation                        │
    │       ↓                                 │
    │ Save trained models & transformers      │
    └──────────────────┬──────────────────────┘
                       │
                       ▼
             src/models/*.pkl
                       │
                       ▼
                  Streamlit app (app.py)
                       │
                       ▼
                 User Prediction
