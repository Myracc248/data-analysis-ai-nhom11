# Task 2 — K-Means hoàn chỉnh

## Chạy bài

1. Giải nén toàn bộ gói; giữ cấu trúc `notebooks/`, `src/`, `data/`, `report/`.
2. Khuyến nghị Python 3.12 (phiên bản đã kiểm tra).
3. Tại thư mục gốc: `python -m pip install -r requirements-task2.txt`.
4. Mở `notebooks/07_kmeans.ipynb`, chọn đúng Python kernel, Restart Kernel → Run All.

Notebook có sẵn outputs. Phải tải cả ZIP: notebook gọi hàm dùng chung trong `src/segmentation/customer_kmeans.py`.

## Kết quả

- 10.000 giao dịch → 1.988 khách hàng.
- Đặc trưng chính: Recency, Frequency, Monetary, Mean_Discount_Ratio.
- Elbow heuristic đề xuất K=4; Silhouette đạt cao nhất ở K=3. K=4 thấp hơn trên 0,02 nên chọn K=3 theo quy tắc đã công bố.
- Chọn non-PCA, Silhouette 0,2786: các nhóm chưa tách biệt mạnh.
- PCA cần 4/4 thành phần mới đạt 90% phương sai, thực tế giữ 100%; không giảm chiều. PCA đầy đủ không whitening bảo toàn khoảng cách Euclid, giải thích kết quả hai nhánh tương đương.
- ARI trung bình qua 5 seed khoảng 0,9993: ổn định với khởi tạo, không chứng minh tính đúng của phân khúc ngoài thực tế.
- Thử thêm one-hot Gender/City: ARI khoảng 0,9863 so với mô hình hành vi. Đây là kiểm tra độ nhạy, không chọn theo Silhouette giữa các không gian khác nhau.

## Tệp bàn giao

- `notebooks/07_kmeans.ipynb`: bài thực hành và kết quả.
- `src/segmentation/customer_kmeans.py`: tổng hợp khách, preprocessing, training, đánh giá, xuất và predict.
- `src/models/customer_kmeans_bundle.joblib`: pipeline đã fit + ánh xạ nhãn + metadata.
- `data/final/task2/customer_segments.csv`: đặc trưng và nhãn 1.988 khách.
- `data/final/task2/transactions_with_clusters.csv`: 10.000 giao dịch gắn nhãn khách.
- `report/task2/`: metrics, profile, báo cáo, thông tin lần chạy và 5 hình.
- `data/final/cleaned_dataset.csv`: bản đầu vào đúng commit để tái lập.

Không ghi đè dữ liệu Stage 1. Không dùng model PCA cấp giao dịch của Task 1 cho bảng khách hàng.

## Tích hợp Task 5

Chạy từ thư mục gốc của dự án:

```python
import joblib
import pandas as pd
from src.segmentation.customer_kmeans import predict_customers

bundle = joblib.load('src/models/customer_kmeans_bundle.joblib')
features = pd.DataFrame([{
    'Recency': 30.0,
    'Frequency': 5,
    'Monetary': 8000000.0,
    'Mean_Discount_Ratio': 0.05,
}])
label = int(predict_customers(bundle, features)[0])
print(bundle['cluster_names'][label])
```

Đầu vào phải là hồ sơ tổng hợp của khách, không phải một dòng giao dịch. Các con số ví dụ không phải khách hàng thật. Không fit lại scaler khi predict. Nếu gọi thẳng `bundle['pipeline'].predict`, phải dùng `label_mapping` để đổi nhãn thô sang nhãn xuất CSV.

Mốc tham chiếu huấn luyện: 2026-09-21, cửa sổ khoảng một năm. Với snapshot mới cần thống nhất cửa sổ lịch sử, tính lại Recency và đánh giá drift. Mô hình hiện chỉ minh họa triển khai, chưa có đánh giá theo thời gian trên khách mới.

## Giới hạn và dữ liệu

Giao dịch, khách hàng và Rating được mô phỏng. Nhóm chi tiêu cao không tự động là khách trung thành; mức giảm cao không chứng minh hiệu quả khuyến mãi. Không dùng kết quả để khẳng định hành vi thị trường thật.

File cleaned vẫn còn thiếu ở metadata do notebook 05 khởi tạo lại `df_cleaned = df.copy()` sau bước imputation. Các cột cốt lõi Task 2 không thiếu; audit sẽ dừng nếu chúng thiếu trong lần chạy khác. Revenue có 10 giá trị đã clip; Monetary sử dụng giá trị sau clip và không tự khôi phục doanh thu gốc.

Nguồn: https://github.com/Myracc248/data-analysis-ai-nhom11
Commit đầu vào: 33f2c4d73827c377835b1ff7a978e9d50fc6c8d2.
Đã kiểm tra toàn bộ 10 ô code theo thứ tự trong namespace mới; mô hình lưu/load cho cùng nhãn; ghép nhãn bảo toàn 10.000 giao dịch; SHA-256 đầu vào không đổi. Môi trường thực thi hạn chế mở kernel TCP nên kiểm tra bằng thực thi Python tuần tự tương đương các ô, không tuyên bố đã chạy kernel Jupyter tại đây.
