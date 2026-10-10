# Task 2 — K-Means

**Kết quả chọn: non_PCA, K=3.**

- **Cụm 0**: 559 khách (28.1%); trung vị chi tiêu 2,370,000 VND; tần suất 3 giao dịch; lần mua gần nhất cách mốc 108.6 ngày; tỷ lệ giảm giá trung vị 0.0%.
- **Cụm 1**: 338 khách (17.0%); trung vị chi tiêu 5,208,140 VND; tần suất 4 giao dịch; lần mua gần nhất cách mốc 65.1 ngày; tỷ lệ giảm giá trung vị 13.1%.
- **Cụm 2**: 1091 khách (54.9%); trung vị chi tiêu 10,570,312 VND; tần suất 6 giao dịch; lần mua gần nhất cách mốc 33.2 ngày; tỷ lệ giảm giá trung vị 2.8%.

Silhouette cùng không gian = 0.279; ARI trung bình qua các seed = 0.999.
Silhouette thấp/không cao phải được công bố; việc K-Means luôn chia được cụm không chứng minh phân khúc tự nhiên rõ rệt.

**Đề xuất kiểm chứng trên dữ liệu thật:**
1. Nhóm chi tiêu cao: thử chăm sóc sau bán, đo tỷ lệ mua lại và lợi nhuận thay vì mặc định họ trung thành.
2. Nhóm lâu chưa mua: thử chiến dịch tái tương tác có nhóm đối chứng; chưa gọi là rời bỏ khi chưa định nghĩa ngưỡng theo ngành.
3. Nhóm thường mua có giảm giá: thử ưu đãi có kiểm soát và đo lợi nhuận tăng thêm; không suy ra tác động nhân quả từ tỷ lệ giảm quan sát.

## So sánh

  space  K        WCSS  Silhouette_native  Silhouette_common  smallest_cluster_fraction  seconds  elbow_K  seed_ARI_mean  seed_ARI_min
non_PCA  3 4668.451645           0.278644           0.278644                    0.17002 0.147805        4       0.999309      0.998273
    PCA  3 4668.451645           0.278644           0.278644                    0.17002 0.136155        4       0.999309      0.998273

Dữ liệu mô phỏng; đánh giá nội bộ toàn snapshot. Chưa đánh giá tổng quát hóa. Mô hình chính dùng hành vi, one-hot Gender/City chỉ là thử độ nhạy. Revenue là giá trị sau clip; 10 dòng khác công thức đơn giá × số lượng.