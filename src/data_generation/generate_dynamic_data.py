import json
from datetime import datetime

import numpy as np
import pandas as pd
from faker import Faker


# ============================================================
# CẤU HÌNH
# ============================================================

N_TRANSACTIONS = 10000
N_CUSTOMERS = 2000
RANDOM_SEED = 42

TESCO_PATH = "data/processed/tesco_products_vnd.csv"
TIKI_PATH = "data/processed/tiki_products_vnd.csv"

REVIEW_BANK_PATH = "data/processed/review_bank.json"

OUTPUT_PATH = "data/processed/dynamic_transactions.csv"


# ============================================================
# RANDOM SEED
# ============================================================

np.random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

fake = Faker()


# ============================================================
# 1. ĐỌC STATIC DATA
# ============================================================

tesco = pd.read_csv(TESCO_PATH)
tiki = pd.read_csv(TIKI_PATH)

products = pd.concat(
    [tesco, tiki],
    ignore_index=True
)

# Chỉ giữ sản phẩm có giá hợp lệ
products = products.dropna(
    subset=["Discount_Price_VND"]
).reset_index(drop=True)


print("=== PRODUCT POOL ===")
print("Số sản phẩm hợp lệ:", len(products))
print("Số Product_ID unique:", products["Product_ID"].nunique())
print(
    "Missing price:",
    products["Discount_Price_VND"].isna().sum()
)


# ============================================================
# 2. ĐỌC REVIEW BANK
# ============================================================

with open(
    REVIEW_BANK_PATH,
    "r",
    encoding="utf-8"
) as f:
    review_bank = json.load(f)


for rating in range(1, 6):
    key = str(rating)

    if key not in review_bank:
        raise ValueError(
            f"Không có review cho Rating {rating}"
        )

    if len(review_bank[key]) != 20:
        raise ValueError(
            f"Rating {rating} không đủ 20 review"
        )


print("\nReview bank loaded successfully.")


# ============================================================
# 3. TẠO CUSTOMER MASTER
# ============================================================

VIETNAM_CITIES = [
    "Hà Nội",
    "TP. Hồ Chí Minh",
    "Đà Nẵng",
    "Hải Phòng",
    "Cần Thơ",
    "Huế",
    "Nha Trang",
    "Vũng Tàu",
    "Đà Lạt",
    "Biên Hòa"
]


customers = []

for i in range(1, N_CUSTOMERS + 1):
    customers.append({
        "Customer_ID": f"C{i:05d}",
        "Gender": np.random.choice(
            ["Male", "Female"]
        ),
        "Age": int(
            np.random.randint(18, 66)
        ),
        "City": np.random.choice(
            VIETNAM_CITIES
        )
    })


customers_df = pd.DataFrame(customers)


print("\n=== CUSTOMER DATA ===")
print(customers_df.head())
print("Số khách hàng:", len(customers_df))


# ============================================================
# 4. SINH TRANSACTION
# ============================================================

START_DATE = datetime(2025, 9, 18)
END_DATE = datetime(2026, 9, 18)

transactions = []


for i in range(N_TRANSACTIONS):

    # Chọn sản phẩm
    product_index = np.random.randint(
        0,
        len(products)
    )

    product = products.iloc[
        product_index
    ]


    # Customer
    customer_number = np.random.randint(
        1,
        N_CUSTOMERS + 1
    )

    customer_id = (
        f"C{customer_number:05d}"
    )


    # Quantity
    quantity = int(
        np.random.randint(1, 6)
    )


    # Rating
    rating = int(
        np.random.randint(1, 6)
    )


    # Giá bán
    unit_price = int(
        round(
            product["Discount_Price_VND"]
        )
    )


    # Revenue
    revenue = (
        unit_price * quantity
    )


    # Review đúng theo Rating
    customer_review = np.random.choice(
        review_bank[str(rating)]
    )


    # Ngày giao dịch
    transaction_date = (
        fake.date_time_between(
            start_date=START_DATE,
            end_date=END_DATE
        )
    )


    # Thêm transaction
    transactions.append({
        "Transaction_ID": f"T{i + 1:06d}",
        "Customer_ID": customer_id,
        "Product_ID": int(
            product["Product_ID"]
        ),
        "Transaction_Date": transaction_date,
        "Quantity": quantity,
        "Unit_Price_VND": unit_price,
        "Revenue": revenue,
        "Rating": rating,
        "Customer_Review": customer_review
    })


dynamic_df = pd.DataFrame(
    transactions
)


# ============================================================
# 5. MERGE CUSTOMER INFORMATION
# ============================================================

dynamic_df = dynamic_df.merge(
    customers_df,
    on="Customer_ID",
    how="left"
)


# ============================================================
# 6. SẮP XẾP CỘT
# ============================================================

dynamic_df = dynamic_df[
    [
        "Transaction_ID",
        "Customer_ID",
        "Product_ID",
        "Transaction_Date",
        "Quantity",
        "Unit_Price_VND",
        "Revenue",
        "Rating",
        "Customer_Review",
        "Gender",
        "Age",
        "City"
    ]
]


# ============================================================
# 7. VALIDATION
# ============================================================

print("\n=== VALIDATION ===")


# Đúng số transaction
assert len(dynamic_df) == N_TRANSACTIONS


# Transaction_ID phải unique
assert (
    dynamic_df["Transaction_ID"].nunique()
    == N_TRANSACTIONS
)


# Product_ID phải tồn tại trong static data
assert (
    dynamic_df["Product_ID"]
    .isin(products["Product_ID"])
    .all()
)


# Quantity phải từ 1 đến 5
assert (
    dynamic_df["Quantity"]
    .between(1, 5)
    .all()
)


# Rating phải từ 1 đến 5
assert (
    dynamic_df["Rating"]
    .between(1, 5)
    .all()
)


# Revenue phải đúng
assert (
    dynamic_df["Revenue"]
    ==
    dynamic_df["Unit_Price_VND"]
    * dynamic_df["Quantity"]
).all()


# Không được missing
assert (
    dynamic_df
    .isna()
    .sum()
    .sum()
    == 0
)


# Customer Review phải đúng với Rating
for rating in range(1, 6):

    subset = dynamic_df[
        dynamic_df["Rating"] == rating
    ]

    valid_reviews = set(
        review_bank[str(rating)]
    )

    assert (
        subset["Customer_Review"]
        .isin(valid_reviews)
        .all()
    )


print("Validation passed.")


# ============================================================
# 8. THỐNG KÊ NHANH
# ============================================================

print("\n=== DYNAMIC DATA ===")
print(dynamic_df.head())


print("\nShape:")
print(dynamic_df.shape)


print("\nRating distribution:")
print(
    dynamic_df["Rating"]
    .value_counts()
    .sort_index()
)


print("\nMissing values:")
print(
    dynamic_df
    .isna()
    .sum()
)


# ============================================================
# 9. LƯU FILE
# ============================================================

dynamic_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)


print("\n================================")
print("DYNAMIC DATA GENERATION PASSED")
print(f"Transactions: {len(dynamic_df)}")
print(
    "Customers:",
    dynamic_df["Customer_ID"].nunique()
)
print(
    "Products used:",
    dynamic_df["Product_ID"].nunique()
)
print(f"Saved: {OUTPUT_PATH}")
print("================================")