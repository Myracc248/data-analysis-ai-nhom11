import pandas as pd

# =========================
# 1. CẤU HÌNH
# =========================

GBP_TO_VND = 34758  # Tỷ giá cố định ngày 18/09/2026

TESCO_PATH = "data/processed/tesco-grocery-uk(1).csv"
TIKI_PATH = "data/processed/vietnamese_tiki_products_backpacks_suitcases(1).csv"


# =========================
# 2. ĐỌC DỮ LIỆU
# =========================

tesco = pd.read_csv(TESCO_PATH)
tiki = pd.read_csv(TIKI_PATH)


# =========================
# 3. CHUẨN HÓA TESCO
# GBP -> VND
# =========================

tesco["Source_Currency"] = "GBP"

tesco["Original_Price_VND"] = (
    tesco["Original_Price"] * GBP_TO_VND
).round()

tesco["Discount_Price_VND"] = (
    tesco["Discount_Price"] * GBP_TO_VND
).round()


# =========================
# 4. CHUẨN HÓA TIKI
# Giá gốc đã là VND
# =========================

tiki["Source_Currency"] = "VND"

tiki["Original_Price_VND"] = tiki["Original_Price"]
tiki["Discount_Price_VND"] = tiki["Discount_Price"]


# =========================
# 5. KIỂM TRA
# =========================

print("=== TESCO ===")
print(
    tesco[
        [
            "Product_ID",
            "Original_Price",
            "Original_Price_VND",
            "Source_Currency"
        ]
    ].head()
)

print("\nSố sản phẩm Tesco thiếu giá:")
print(tesco["Discount_Price_VND"].isna().sum())


print("\n=== TIKI ===")
print(
    tiki[
        [
            "Product_ID",
            "Original_Price",
            "Original_Price_VND",
            "Source_Currency"
        ]
    ].head()
)


# =========================
# 6. LƯU FILE MỚI
# Không ghi đè dữ liệu ban đầu
# =========================

tesco.to_csv(
    "data/processed/tesco_products_vnd.csv",
    index=False,
    encoding="utf-8-sig"
)

tiki.to_csv(
    "data/processed/tiki_products_vnd.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nChuẩn hóa tiền tệ hoàn tất.")