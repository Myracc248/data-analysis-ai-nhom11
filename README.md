# Phân tích dữ liệu bán lẻ và thương mại điện tử · Nhóm 11

Đồ án cuối kỳ môn **Nhập môn Phân tích Dữ liệu & AI**, Trường Đại học Công nghiệp TP.HCM. Nhóm kết hợp danh mục sản phẩm Tesco UK và Tiki Việt Nam với 10.000 giao dịch mô phỏng để nghiên cứu ba câu hỏi: giá và số lượng liên hệ thế nào với doanh thu, khách hàng có thể được phân nhóm theo hành vi mua sắm ra sao, và thông tin giao dịch có giúp nhận biết đánh giá 4–5 sao hay không?

## Chạy bản demo bằng Docker

Mở Docker Desktop, sau đó mở terminal tại thư mục chứa `docker-compose.yml`. Lần đầu chạy hoặc sau khi cập nhật mã nguồn, dùng:

```powershell
docker compose up -d --build
docker compose ps
```

Mở **[http://localhost:8502](http://localhost:8502)**. Trong cấu hình `127.0.0.1:8502:8501`, trình duyệt trên máy dùng cổng **8502** và Streamlit bên trong container dùng cổng **8501**. Để kiểm tra cổng đang được công bố, chạy `docker compose port app 8501`.

| Thao tác | Lệnh |
|---|---|
| Mở lại bản đã build để demo | `docker compose up -d` |
| Xem log của Streamlit | `docker compose logs --tail=50 app` |
| Dừng ứng dụng, giữ dữ liệu trong volume | `docker compose down` |

Compose chạy hai dịch vụ `app` và `mongodb` trên mạng `retail_network`. Dịch vụ MongoDB dùng volume `mongodb_data`. Streamlit nạp bốn mô hình đã huấn luyện từ [src/models/](src/models/) và dùng CSV cho phần trực quan PCA. Thao tác dự đoán trên giao diện dùng các mô hình đã lưu. Việc ghi và đọc lại dữ liệu từ hai cơ sở dữ liệu được minh họa riêng trong notebook 04.

<details>
<summary>Chạy riêng Streamlit bằng Python</summary>

Từ thư mục gốc, dùng môi trường Python 3.13 và chạy:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Mở địa chỉ Streamlit in trong terminal. File `requirements.txt` dành cho ứng dụng và ghim scikit-learn 1.9.1. Bundle K-Means được xuất với phiên bản 1.8.0 nên có thể xuất hiện cảnh báo khác phiên bản khi nạp.

</details>

## Thành viên và phân công

Cột **Tiêu chí phụ trách** ghi theo barem cuối kỳ. Hai cột còn lại ghi phần triển khai và phối hợp của từng thành viên ở mỗi giai đoạn. Trọng số là tỷ trọng của tiêu chí trong điểm đồ án.

| Thành viên | Tiêu chí phụ trách | Stage 1 · Dữ liệu và EDA | Stage 2 · Mô hình, ứng dụng và báo cáo |
|---|---|---|---|
| Vương Quốc Tiến | Thu thập và tích hợp dữ liệu · 20% | Thu thập, chuẩn hóa danh mục Tesco và Tiki để tích hợp | Thực hiện PCA cấp giao dịch, chọn số thành phần và phân tích phương sai |
| Nguyễn Huỳnh Thanh Tuấn | Advanced EDA · 20% | Làm sạch dữ liệu, đánh giá giá trị thiếu, phân phối và ngoại lệ | So sánh hai mô hình hồi quy doanh thu |
| Nguyễn Vương Quốc Tuấn | Visual & Insights · 15% | Vẽ biểu đồ EDA, giải thích kết quả và liên hệ với lựa chọn đặc trưng | Phân lớp đánh giá cao, so sánh Logistic Regression và Decision Tree |
| Nguyễn Tuấn Duy | Machine Learning · 20% | Viết script quy đổi tiền tệ, sinh giao dịch và nhận xét mô phỏng | Phụ trách K-Means, chọn số cụm, đối chứng PCA và gắn nhãn khách hàng |
| Hà Xuân Khoa | Docker và giao diện · 15% | Trưởng nhóm, điều phối tiến độ, nối dữ liệu và kiểm tra kết quả tích hợp | Tích hợp bốn mô hình vào Streamlit, triển khai ứng dụng bằng Docker Compose |
| Phan Chí Thanh | Báo cáo và phân tích kinh doanh · 10% | Lưu và truy xuất dữ liệu bằng SQL Server và MongoDB Atlas | Hỗ trợ Nguyễn Tuấn Duy triển khai K-Means. Hỗ trợ tích hợp, rà soát kết quả và tổng hợp khuyến nghị kinh doanh cho báo cáo, slide |

## Stage 1 · Từ danh mục sản phẩm đến dữ liệu phân tích

| Bước | Công việc và kết quả | Mã nguồn |
|---|---|---|
| 01 · Dữ liệu tĩnh | Đọc hai danh mục sản phẩm, chuẩn hóa các trường dùng chung và giữ các thuộc tính riêng của từng nguồn. | [Nguồn 1](notebooks/01%20static%20data%201.ipynb) · [Nguồn 2](notebooks/01%20static%20data%202.ipynb) |
| 02 · Dữ liệu động | Quy đổi giá về VND, sinh khách hàng và giao dịch, gán số sao và lấy nhận xét tương ứng từ ngân hàng mẫu. Doanh thu ban đầu được tính bằng `Quantity × Unit_Price_VND`. | [Notebook 02](notebooks/02_dynamic_data.ipynb) · [Script sinh dữ liệu](src/data_generation/) |
| 03 · Tích hợp | Dùng `pd.concat` nối dọc hai danh mục. Dùng `pd.merge` với giao dịch làm bảng trái và `Product_ID` làm khóa để giữ đủ 10.000 giao dịch. Kết quả là `data/final/master_dataset.csv`. | [Notebook 03](notebooks/03_data_integration.ipynb) |
| 04 · Lưu trữ | Ghi dữ liệu tích hợp vào SQL Server và MongoDB Atlas. Kết quả đọc ngược từ mỗi hệ về DataFrame đều có **10.000 dòng × 39 cột**. | [Notebook 04](notebooks/04_database.ipynb) · [Script cơ sở dữ liệu](src/database/) |
| 05 · Làm sạch và EDA | Khảo sát tỷ lệ thiếu theo cột, trực quan bằng missingno, so sánh phân phối trước/sau điền và phát hiện ngoại lệ bằng IQR. Histogram, boxplot, heatmap, scatter và biểu đồ cột giúp đối chiếu giá, doanh thu và nhóm hàng. Đầu ra dùng cho Stage 2 là `data/final/cleaned_dataset.csv`. | [Notebook 05](notebooks/05_cleaning_eda.ipynb) |

**Cách đọc số lượng sản phẩm trong notebook 03.** Danh mục hợp nhất có **6.559** mã duy nhất. Có **3** mã thiếu giá bán nên **6.556** mã đủ điều kiện để sinh giao dịch. Quá trình lấy mẫu tạo ra 10.000 giao dịch của **1.988** khách hàng, trong đó có **5.099** mã sản phẩm thực sự xuất hiện. Sau phép nối trái vẫn có 10.000 dòng và 5.099 mã sản phẩm xuất hiện.

## Stage 2 · Kết quả và chức năng trên Streamlit

| Tab | Kết quả thực nghiệm | Notebook |
|---|---|---|
| PCA | Từ 11 đặc trưng cấp giao dịch, mô hình giữ **9 thành phần** và **91,44%** phương sai. Bảng tọa độ và biểu đồ phương sai của mô hình đã chọn hiển thị PC1–PC9. | [06 · PCA](notebooks/06_pca.ipynb) |
| K-Means | Nhóm 1.988 khách theo thời gian từ lần mua gần nhất, tần suất, tổng chi tiêu và tỷ lệ giảm giá trung bình. Nhóm chọn **K = 3** sau khi xét Elbow và Silhouette. Với cùng không gian đánh giá, bốn đặc trưng gốc cho Silhouette **0,2786**. Phương án giảm còn ba PC giữ **89,93%** phương sai và đạt **0,2779**. Ứng dụng dùng mô hình bốn đặc trưng gốc. | [07 · K-Means](notebooks/07_kmeans.ipynb) |
| Regression | Ước lượng `Revenue` bằng VND. **Linear Regression** đạt R² **0,8095**, RMSE khoảng **2.442.313 VND**. Decision Tree Regressor đạt R² **0,6526**, RMSE khoảng **3.298.003 VND**. | [08 · Regression](notebooks/08_regression.ipynb) |
| Classification | Nhãn `Target = 1` khi `Rating >= 4`, còn lại là lớp 0. Trên 2.000 giao dịch kiểm tra, **Decision Tree** đạt Macro-F1 **0,4960**, Accuracy **0,5080**. Logistic Regression đạt Macro-F1 **0,4733**, Accuracy **0,4745**. Nhóm chọn Decision Tree theo Macro-F1. | [09 · Classification](notebooks/09_classification.ipynb) |

PCA ở tab đầu mô tả **giao dịch**. Thử nghiệm ba PC trong K-Means mô tả **khách hàng** sau khi tổng hợp nhiều giao dịch theo `Customer_ID`. Kết quả phân cụm được lưu ở hai cấp: `customer_segments.csv` có một dòng cho mỗi khách hàng và `transactions_with_clusters.csv` gắn nhãn cụm của khách vào từng giao dịch.

## Diễn giải kết quả

Doanh thu mô phỏng được tính trực tiếp từ số lượng và đơn giá, nên R² của hồi quy chủ yếu phản ánh công thức sinh dữ liệu. Ba cụm khách có thể dùng để thiết kế thử nghiệm ưu đãi theo tần suất và mức chi tiêu, nhưng Silhouette khoảng 0,28 cho thấy các cụm còn chồng lấn. Số sao được sinh mô phỏng, và Accuracy của bộ phân lớp được chọn (50,8%) thấp hơn cách luôn đoán lớp phổ biến trên tập kiểm tra (1.190/2.000 = 59,5%). Khi demo, nên diễn giải kết quả phân lớp trong giới hạn đó.

## Tài liệu và đầu ra

- [Báo cáo cuối kỳ](report/) trình bày phương pháp, kết quả đánh giá, giao diện và khuyến nghị kinh doanh.
- [Dữ liệu đầu ra](data/final/) gồm dữ liệu tích hợp, dữ liệu đã làm sạch, hồ sơ cụm và giao dịch gắn nhãn.
- [Biểu đồ phân cụm](notebooks/figures/kmeans/) gồm Elbow, Silhouette, phương sai PCA và phân bố khách hàng theo cụm.
- [Mã giao diện](app.py) và [cấu hình Docker Compose](docker-compose.yml) là hai điểm bắt đầu để xem cách ứng dụng nạp mô hình và chạy bản demo.
