# Task 2 — K-Means

## Cách dùng bản cập nhật

Chép các file trong gói vào đúng vị trí của dự án đã clone. Giữ nguyên `data/final/cleaned_dataset.csv` của nhóm. Xóa hai thư mục output cũ `data/final/task2/` và `report/task2/` (chỉ kết quả riêng Task 2). Không xóa báo cáo cuối hoặc dữ liệu của task khác.

Cài thư viện từ `requirements-task2.txt` nếu cần. Mở `notebooks/07_kmeans.ipynb`, Restart Kernel rồi Run All.

## Cấu trúc đầu ra

| Đường dẫn | Nội dung |
|---|---|
| `data/final/customer_segments.csv` | Đặc trưng và nhãn 1.988 khách |
| `data/final/transactions_with_clusters.csv` | 10.000 giao dịch gắn nhãn khách |
| `notebooks/figures/kmeans/` | 5 hình kết quả |
| `src/models/customer_kmeans_bundle.joblib` | Pipeline, ánh xạ nhãn, metadata đánh giá |

Các bảng chọn K, so sánh mô hình, hồ sơ cụm và nhận xét được hiển thị trực tiếp trong notebook. Không xuất CSV phụ, JSON, Markdown báo cáo hay hình vào `report/`. Thư mục `report/` dành cho báo cáo cuối nhóm.

## Tích hợp model

```python
import joblib
from src.segmentation.customer_kmeans import predict_customers
bundle = joblib.load('src/models/customer_kmeans_bundle.joblib')
labels = predict_customers(bundle, customer_features)
```

`customer_features` phải có Recency, Frequency, Monetary, Mean_Discount_Ratio ở cấp khách hàng, cùng định nghĩa cửa sổ quan sát. Không truyền trực tiếp một dòng giao dịch. `predict_customers` áp dụng ánh xạ nhãn đúng với CSV.

Kết quả bản bàn giao: K=3, Silhouette khoảng 0,279. PCA giữ 4/4 chiều nên không giảm chiều; chọn non-PCA. Dữ liệu được mô phỏng; các nhóm chưa tách biệt mạnh, không suy ra phân khúc hay tác động kinh doanh thật. Notebook và mô hình giữ nguyên phương pháp, chỉ đổi cấu trúc output và trình bày bảng.
