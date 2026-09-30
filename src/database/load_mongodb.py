from getpass import getpass
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from pymongo import MongoClient, ReplaceOne

csv_path = Path(__file__).resolve().parents[2] / "data/final/master_dataset.csv"
df = pd.read_csv(csv_path, low_memory=False)

if df["Transaction_ID"].isna().any() or df["Transaction_ID"].duplicated().any():
    raise ValueError("Transaction_ID bị thiếu hoặc trùng trong CSV")

# Giữ giá trị thiếu dưới dạng null trong MongoDB
records = df.astype(object).where(pd.notna(df), None).to_dict("records")

uri_mau = input("Dán chuỗi mongodb+srv (giữ <db_password>): ").strip()
if "<db_password>" not in uri_mau:
    raise ValueError("Chuỗi kết nối phải giữ nguyên <db_password>")

mat_khau = getpass("Nhập mật khẩu database user: ")
uri = uri_mau.replace("<db_password>", quote_plus(mat_khau))

client = MongoClient(uri, serverSelectionTimeoutMS=15000)

try:
    collection = client["retail_analytics"]["transactions"]
    client.admin.command("ping")

    for start in range(0, len(records), 500):
        batch = records[start:start + 500]
        operations = []

        for record in batch:
            transaction_id = str(record["Transaction_ID"])
            record["_id"] = transaction_id
            operations.append(
                ReplaceOne({"_id": transaction_id}, record, upsert=True)
            )

        collection.bulk_write(operations)
        print(f"Đã xử lý {min(start + 500, len(records))}/{len(records)} giao dịch")

    print("Số dòng CSV:", len(records))
    print("Số documents MongoDB:", collection.count_documents({}))
finally:
    client.close()