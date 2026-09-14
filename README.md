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
* **Mục tiêu phân tích (Analytical Goal):** Phân tích các yếu tố ảnh hưởng đến doanh thu và mức độ hài lòng của khách hàng đối với các mặt hàng thiết bị điện tử, từ đó dự đoán xu hướng mua sắm.
* **Đối tượng phục vụ (For Whom):** Ban giám đốc / Giám đốc sản phẩm của hệ thống bán lẻ để tối ưu hóa chiến lược giá và nhập hàng.
* **Thước đo thành công (Success Metric):** Khám phá được ít nhất 3 tập khách hàng hoặc 3 yếu tố quan trọng nhất quyết định việc mua hàng thông qua biểu đồ trực quan.
* **Biến mục tiêu (Target Variable):** `Rating` (Điểm đánh giá) hoặc `Revenue` (Doanh thu). 
> **Lưu ý quan trọng:** Mọi dòng dữ liệu khuyết ở biến mục tiêu này sẽ bị xóa bỏ hoàn toàn (dropna).

---

## 🗂️ Yêu cầu Khung dữ liệu (Data Schema)
Để đảm bảo việc gộp bảng (Merge) diễn ra thành công, Dữ liệu Tĩnh và Dữ liệu Động bắt buộc phải tuân thủ định dạng các cột cốt lõi dưới đây:

### 📌 Dữ liệu Tĩnh - Đảm nhiệm: Vương Quốc Tiến (Vị trí 1)
**Yêu cầu:** Tạo Bảng Master Sản phẩm (Gộp từ cào web hoặc file Kaggle).

| Tên Cột | Mô tả |
| :--- | :--- |
| **`Product_ID`** | **Khóa chính (Primary Key)** - Định dạng chuỗi hoặc số (VD: SP001, SP002...). |
| `Product_Name` | Tên sản phẩm. |
| `Category` | Danh mục sản phẩm (VD: Laptop, Điện thoại, Chuột, Bàn phím...). |
| `Brand` | Thương hiệu. |
| `Original_Price` | Giá gốc của sản phẩm. |
| `Discount_Price` | Giá sau khi đã áp dụng khuyến mãi. |

### 📌 Dữ liệu Động - Đảm nhiệm: Nguyễn Tuấn Duy (Vị trí 2)
**Yêu cầu:** Dùng thư viện Python (`Faker`, `numpy`) và LLM/Ollama để giả lập Bảng Giao dịch & Đánh giá khách hàng.

| Tên Cột | Mô tả |
| :--- | :--- |
| **`Transaction_ID`** | **Khóa chính (Primary Key)** - Tạo chuỗi ngẫu nhiên duy nhất cho mỗi giao dịch. |
| **`Product_ID`** | **Khóa ngoại (Foreign Key) - BẮT BUỘC BỐC TỪ DANH SÁCH ID CỦA VỊ TRÍ 1 SANG.** |
| `Customer_Age` | Tuổi khách hàng - Dùng `numpy.random` sinh ngẫu nhiên khoảng 18-50. |
| `Purchase_Date` | Ngày mua hàng - Dùng `pd.date_range` sinh thời gian trong năm 2025-2026. |
| **`Rating`** | Điểm đánh giá từ 1 đến 5 sao - **(BIẾN MỤC TIÊU)**. |
| `Customer_Review` | Dùng API / LLM / Ollama sinh ra một câu review ngắn tương ứng với số sao ở cột Rating. |
