import csv
from getpass import getpass
from pathlib import Path

import pyodbc


csv_path = Path(__file__).resolve().parents[2] / "data/final/master_dataset.csv"

with csv_path.open("r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    csv_columns = reader.fieldnames
    records = list(reader)

server = input("Nhập Server name như trong SSMS: ").strip()
password = getpass("Nhập mật khẩu sa: ")

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    f"SERVER={server};"
    "DATABASE=RetailAnalytics;"
    "UID=sa;"
    f"PWD={password};",
    timeout=10
)

try:
    cursor = conn.cursor()

    sql_columns = [
        row[0] for row in cursor.execute(
            """
            SELECT name
            FROM sys.columns
            WHERE object_id = OBJECT_ID(N'dbo.MasterTransactions')
            ORDER BY column_id
            """
        ).fetchall()
    ]

    if csv_columns != sql_columns:
        raise ValueError(
            f"Cột CSV và bảng SQL không khớp.\nCSV: {csv_columns}\nSQL: {sql_columns}"
        )

    existing_ids = {
        row[0] for row in cursor.execute(
            "SELECT Transaction_ID FROM dbo.MasterTransactions"
        ).fetchall()
    }

    seen_ids = set()
    new_rows = []

    for record in records:
        transaction_id = record["Transaction_ID"]

        if not transaction_id or transaction_id in seen_ids:
            raise ValueError(f"Transaction_ID thiếu hoặc trùng trong CSV: {transaction_id}")

        seen_ids.add(transaction_id)

        if transaction_id in existing_ids:
            continue

        # Ô trống của CSV được lưu thành NULL, không tự điền dữ liệu.
        new_rows.append(
            tuple(None if record[column] == "" else record[column]
                  for column in csv_columns)
        )

    column_names = ", ".join(f"[{column}]" for column in csv_columns)
    placeholders = ", ".join("?" for _ in csv_columns)
    insert_sql = (
        f"INSERT INTO dbo.MasterTransactions ({column_names}) "
        f"VALUES ({placeholders})"
    )

    for start in range(0, len(new_rows), 200):
        cursor.executemany(insert_sql, new_rows[start:start + 200])

    conn.commit()

    total = cursor.execute(
        "SELECT COUNT(*) FROM dbo.MasterTransactions"
    ).fetchone()[0]

    print("Số giao dịch trong CSV:", len(records))
    print("Số giao dịch vừa nạp:", len(new_rows))
    print("Tổng số giao dịch trong SQL Server:", total)

except Exception:
    conn.rollback()
    raise
finally:
    conn.close()