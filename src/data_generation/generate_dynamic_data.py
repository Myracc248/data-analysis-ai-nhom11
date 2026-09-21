import json
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker


# ============================================================
# CẤU HÌNH
# ============================================================

N_TRANSACTIONS = 10000
N_CUSTOMERS = 2000
RANDOM_SEED = 42

ROOT = Path(__file__).resolve().parents[2]

TESCO_PATH = ROOT / "data" / "processed" / "tesco_products_vnd.csv"
TIKI_PATH = ROOT / "data" / "processed" / "tiki_products_vnd.csv"

REVIEW_BANK_PATH = ROOT / "data" / "processed" / "review_bank.json"

OUTPUT_PATH = ROOT / "data" / "processed" / "dynamic_transactions.csv"


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
    [
        tesco[["Product_ID", "Discount_Price_VND"]],
        tiki[["Product_ID", "Discount_Price_VND"]],
    ],
    ignore_index=True,
)

products["Product_ID"] = pd.to_numeric(
    products["Product_ID"],
    errors="coerce",
)

products["Discount_Price_VND"] = pd.to_numeric(
    products["Discount_Price_VND"],
    errors="coerce",
)

# Chỉ giữ sản phẩm có Product_ID và giá hợp lệ
products = products.dropna(
    subset=[
        "Product_ID",
        "Discount_Price_VND",
    ]
).copy()

products["Product_ID"] = (
    products["Product_ID"]
    .astype("int64")
)

products["Discount_Price_VND"] = (
    products["Discount_Price_VND"]
    .round()
    .astype("int64")
)

# Loại Product_ID bị trùng
products = products.drop_duplicates(
    subset=["Product_ID"],
    keep="first",
).reset_index(drop=True)


# ============================================================
# VALIDATE PRODUCT POOL
# ============================================================

assert len(products) > 0

assert products["Product_ID"].notna().all()

assert products["Discount_Price_VND"].notna().all()

assert products["Product_ID"].is_unique

assert (
    products["Discount_Price_VND"] >= 0
).all()


print("=== PRODUCT POOL ===")
print("Số sản phẩm hợp lệ:", len(products))
print(
    "Số Product_ID unique:",
    products["Product_ID"].nunique(),
)


# ============================================================
# 2. ĐỌC REVIEW BANK
# ============================================================

with open(
    REVIEW_BANK_PATH,
    "r",
    encoding="utf-8",
) as f:
    review_bank = json.load(f)


for rating in range(1, 6):

    key = str(rating)

    assert key in review_bank, (
        f"Thiếu review cho Rating {rating}"
    )

    assert len(review_bank[key]) == 20, (
        f"Rating {rating} không đủ 20 review"
    )


print("Review bank: PASSED")


# ============================================================
# 3. CUSTOMER MASTER
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
    "Biên Hòa",
]


customers_df = pd.DataFrame(
    {
        "Customer_ID": [
            f"C{i:05d}"
            for i in range(
                1,
                N_CUSTOMERS + 1,
            )
        ],

        "Gender": np.random.choice(
            ["Male", "Female"],
            size=N_CUSTOMERS,
        ),

        "Age": np.random.randint(
            18,
            66,
            size=N_CUSTOMERS,
        ),

        "City": np.random.choice(
            VIETNAM_CITIES,
            size=N_CUSTOMERS,
        ),
    }
)


assert len(customers_df) == N_CUSTOMERS
assert customers_df["Customer_ID"].is_unique


print("Customers:", len(customers_df))


# ============================================================
# 4. TẠO TRANSACTIONS
# ============================================================

START_DATE = datetime(2025, 9, 21)
END_DATE = datetime(2026, 9, 21)

transactions = []


for i in range(N_TRANSACTIONS):

    # Chọn sản phẩm
    product_index = np.random.randint(
        0,
        len(products),
    )

    product = products.iloc[
        product_index
    ]


    # Chọn khách hàng
    customer_number = int(
        np.random.randint(
            1,
            N_CUSTOMERS + 1,
        )
    )

    customer_id = (
        f"C{customer_number:05d}"
    )


    # Quantity
    quantity = int(
        np.random.randint(
            1,
            6,
        )
    )


    # Rating
    rating = int(
        np.random.randint(
            1,
            6,
        )
    )


    # Giá
    unit_price = int(
        product[
            "Discount_Price_VND"
        ]
    )


    # Revenue
    revenue = (
        unit_price
        * quantity
    )


    # Review tương ứng Rating
    customer_review = str(
        np.random.choice(
            review_bank[
                str(rating)
            ]
        )
    )


    # Ngày giao dịch
    transaction_date = (
        fake.date_time_between(
            start_date=START_DATE,
            end_date=END_DATE,
        )
    )


    transactions.append(
        {
            "Transaction_ID":
                f"T{i + 1:06d}",

            "Customer_ID":
                customer_id,

            "Product_ID":
                int(
                    product[
                        "Product_ID"
                    ]
                ),

            "Transaction_Date":
                transaction_date,

            "Quantity":
                quantity,

            "Unit_Price_VND":
                unit_price,

            "Revenue":
                revenue,

            "Rating":
                rating,

            "Customer_Review":
                customer_review,
        }
    )


dynamic_df = pd.DataFrame(
    transactions
)


# ============================================================
# 5. MERGE CUSTOMER INFORMATION
# ============================================================

dynamic_df = dynamic_df.merge(
    customers_df,
    on="Customer_ID",
    how="left",
    validate="many_to_one",
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
        "City",
    ]
]


# ============================================================
# 7. VALIDATION
# ============================================================

print("\n=== VALIDATION ===")


# Đúng 10,000 transaction
assert (
    len(dynamic_df)
    == N_TRANSACTIONS
)


# Transaction_ID unique
assert (
    dynamic_df[
        "Transaction_ID"
    ].nunique()
    == N_TRANSACTIONS
)


# Product_ID phải thuộc static
assert (
    dynamic_df[
        "Product_ID"
    ]
    .isin(
        products[
            "Product_ID"
        ]
    )
    .all()
)


# Quantity từ 1 -> 5
assert (
    dynamic_df[
        "Quantity"
    ]
    .between(1, 5)
    .all()
)


# Rating từ 1 -> 5
assert (
    dynamic_df[
        "Rating"
    ]
    .between(1, 5)
    .all()
)


# Revenue đúng công thức
assert (
    dynamic_df[
        "Revenue"
    ]
    ==
    dynamic_df[
        "Unit_Price_VND"
    ]
    *
    dynamic_df[
        "Quantity"
    ]
).all()


# Không missing
assert (
    dynamic_df
    .isna()
    .sum()
    .sum()
    == 0
)


# Review phải đúng Rating
for rating in range(1, 6):

    rating_rows = dynamic_df[
        dynamic_df["Rating"]
        == rating
    ]

    valid_reviews = set(
        review_bank[
            str(rating)
        ]
    )

    assert (
        rating_rows[
            "Customer_Review"
        ]
        .isin(valid_reviews)
        .all()
    )


print("Validation passed.")


# ============================================================
# 8. SAVE
# ============================================================

dynamic_df.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig",
)


# ============================================================
# 9. SUMMARY
# ============================================================

print("\n=== DYNAMIC DATA ===")

print(
    "Shape:",
    dynamic_df.shape,
)

print(
    "Customers used:",
    dynamic_df[
        "Customer_ID"
    ].nunique(),
)

print(
    "Products used:",
    dynamic_df[
        "Product_ID"
    ].nunique(),
)

print("\nRating distribution:")

print(
    dynamic_df[
        "Rating"
    ]
    .value_counts()
    .sort_index()
)

print(
    "\nSaved:",
    OUTPUT_PATH,
)

print(
    "\nDYNAMIC DATA GENERATION PASSED"
)