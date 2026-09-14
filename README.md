# data-analysis-ai-nhom11
**Đề tài:** Phân tích Dữ liệu Hệ thống Bán lẻ & Thương mại Điện tử
Dự án thuộc môn học nhập môn Phân tích Dữ liệu & AI, tập trung vào việc thu thập, làm sạch, lưu trữ và phân tích khám phá (EDA) dữ liệu bán lẻ.

## 👥 Danh sách Thành viên & Phân công
* **Vị trí 0 (Nhóm trưởng - Quản lý & Tích hợp):** Hà Xuân Khoa
* **Vị trí 1 (Thu thập Dữ liệu Tĩnh & Gộp):** Vương Quốc Tiến
* **Vị trí 2 (Giả lập Dữ liệu Động):** Nguyễn Tuấn Duy
* **Vị trí 3 (Quản trị CSDL Modern):** Phan Chí Thanh
* **Vị trí 4 (Làm sạch Dữ liệu Nâng cao):** Nguyễn Huỳnh Thanh Tuấn
* **Vị trí 5 (Phân tích EDA & Trực quan hóa):** Nguyễn Vương Quốc Tuấn

---

## 🎯 Bước 0: Định nghĩa Bài toán (Define the question)
* **Mục tiêu phân tích (Analytical Goal):** Phân tích các yếu tố ảnh hưởng đến doanh thu và mức độ hài lòng của khách hàng đối với các mặt hàng thiết bị điện tử, từ đó xác định các xu hướng và nhóm khách hàng có hành vi mua sắm nổi bật.
* **Đối tượng phục vụ (For Whom):** Ban giám đốc / Giám đốc sản phẩm của hệ thống bán lẻ để tối ưu hóa chiến lược giá và nhập hàng.
* **Thước đo thành công (Success Metric):** Khám phá được ít nhất 3 nhóm khách hàng có hành vi mua sắm nổi bật **hoặc 3 yếu tố có mối quan hệ đáng chú ý với mức độ hài lòng (Rating) và doanh thu (Revenue) thông qua phân tích và trực quan hóa dữ liệu.
* **Biến mục tiêu (Target Variable):** `Rating` (Điểm đánh giá). Biến phân tích phụ: `Revenue` (Doanh thu).
> **Lưu ý:** Missing values tại biến mục tiêu sẽ được đánh giá riêng. Việc loại bỏ bản ghi (dropna) chỉ được thực hiện khi có lý do phân tích phù hợp; các biến còn lại sẽ áp dụng chiến lược điền khuyết (imputation) tương ứng với kiểu dữ liệu. Nghiêm cấm xóa dòng tùy tiện.

---

## 🗂️ Bước 1: Thu thập Dữ liệu Tĩnh (Static Data)
**Đảm nhiệm:** Vương Quốc Tiến (Vị trí 1)
**Yêu cầu:** 
- Thu thập dữ liệu từ **ít nhất 2 nguồn khác nhau** (ví dụ: 2 website, 2 danh mục, hoặc 2 dataset Kaggle/GitHub).
- Mỗi nguồn dữ liệu đạt **tối thiểu 300 records**.
- Chuẩn hóa tên cột và kiểu dữ liệu trước khi dùng lệnh `pd.concat()`.

| Tên Cột | Mô tả |
| :--- | :--- |
| **`Product_ID`** | **Khóa chính (Primary Key)** - Định dạng chuỗi hoặc số (VD: SP001, SP002...). |
| `Product_Name` | Tên sản phẩm. |
| `Category` | Danh mục sản phẩm (VD: Laptop, Điện thoại, Chuột, Bàn phím...). |
| `Brand` | Thương hiệu. |
| `Original_Price` | Giá gốc của sản phẩm. |
| `Discount_Price` | Giá sau khi đã áp dụng khuyến mãi. |

---

## ⚙️ Bước 2: Tạo Dữ liệu Động (Dynamic Data)
**Đảm nhiệm:** Nguyễn Tuấn Duy (Vị trí 2)
**Yêu cầu:** Dùng thư viện Python (`Faker`, `numpy`) và LLM/Ollama để giả lập Bảng Giao dịch & Đánh giá khách hàng.

| Tên Cột | Mô tả |
| :--- | :--- |
| **`Transaction_ID`** | **Khóa chính (Primary Key)** - Tạo chuỗi ngẫu nhiên duy nhất cho mỗi giao dịch. |
| **`Product_ID`** | **Khóa ngoại (Foreign Key) - BẮT BUỘC BỐC TỪ DANH SÁCH ID CỦA BƯỚC 1 SANG.** |
| `Customer_Age` | Tuổi khách hàng - Dùng `numpy.random` sinh ngẫu nhiên khoảng 18-50. |
| `Purchase_Date` | Ngày mua hàng - Dùng `pd.date_range` sinh dữ liệu trong khoảng 2025-2026. |
| `Quantity` | Số lượng sản phẩm mua. |
| `Revenue` | Doanh thu giao dịch (tính bằng công thức: `Discount_Price × Quantity`). |
| **`Rating`** | Điểm đánh giá từ 1 đến 5 sao - **(BIẾN MỤC TIÊU)**. |
| `Customer_Review` | Dùng API / LLM / Ollama sinh ra câu review ngắn tương ứng với số sao. |

---

## 🔗 Bước 3: Tích hợp Dữ liệu (Data Integration)
**Đảm nhiệm:** Hà Xuân Khoa (Nhóm trưởng)

### 3.1 Vertical Concatenation - `pd.concat()`
- Kiểm tra, đồng bộ tên cột và kiểu dữ liệu từ các nguồn tĩnh để gộp thành `Unified Static Master Table`.

### 3.2 Horizontal Merging - `pd.merge()`
- Merge `Unified Static Master Table` với bảng Dynamic Transaction Data.
- **Khóa liên kết:** `Product_ID`.
- **Kiểu JOIN:** Nhóm trưởng sẽ quyết định (`Left Join`, `Inner Join`...) khi code thực tế và viết giải thích chi tiết lý do lựa chọn loại JOIN đó trong báo cáo.

---

## 🗄️ Bước 4: Lưu trữ Cơ sở dữ liệu (Modern Data Storage)
**Đảm nhiệm:** Phan Chí Thanh (Vị trí 3)
> 🚧 *Đang thực hiện*
- [ ] Chọn 2 hệ cơ sở dữ liệu (MongoDB Atlas, Vector DB, hoặc SQL).
- [ ] Viết script nạp Master Dataset vào CSDL.
- [ ] Viết script kết nối truy xuất dữ liệu ngược ra Python phục vụ quá trình EDA.

---

## 🧹 Bước 5: Làm sạch Dữ liệu & EDA
**Đảm nhiệm:** N.H.T. Tuấn (Vị trí 4) & N.V.Q. Tuấn (Vị trí 5)
> 🚧 *Đang thực hiện*

### 5.1 Missing Value Strategy
- [ ] Đánh giá số lượng và tỷ lệ Missing Values của từng cột.
- [ ] Trực quan hóa Missing Values bằng thư viện `missingno`.
- [ ] Áp dụng chiến lược Imputation phù hợp (Mean/Median/Mode, Forward-fill...).
- [ ] So sánh phân phối dữ liệu Trước (Before) và Sau (After) khi Imputation.

### 5.2 Univariate Analysis
- [ ] Tính thống kê mô tả, kiểm tra phân phối, xử lý ngoại lai (Outliers) bằng IQR/Z-score.

### 5.3 Multivariate Analysis
- [ ] Lập ma trận tương quan, so sánh nhóm phân loại vs biến số.

### 📊 Visualizations
- [ ] Biểu đồ 1 (Kèm nhãn Title, X/Y labels chuẩn)
- [ ] Biểu đồ 2
- [ ] Biểu đồ 3
- [ ] Biểu đồ 4
- [ ] Biểu đồ 5

### 💡 Insights - "So What?"
- [ ] Báo cáo giải thích ý nghĩa biểu đồ và định hướng phân tích AI dưới mỗi biểu đồ.
