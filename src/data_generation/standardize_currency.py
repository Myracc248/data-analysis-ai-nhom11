from pathlib import Path
import pandas as pd


# =========================
# CẤU HÌNH
# =========================

GBP_TO_VND = 34758

ROOT = Path(__file__).resolve().parents[2]

TESCO_INPUT = ROOT / "data" / "processed" / "tesco-grocery-uk.csv"
TIKI_INPUT = ROOT / "data" / "processed" / "vietnamese_tiki_products_backpacks_suitcases.csv"

TESCO_OUTPUT = ROOT / "data" / "processed" / "tesco_products_vnd.csv"
TIKI_OUTPUT = ROOT / "data" / "processed" / "tiki_products_vnd.csv"


# =========================
# ĐỌC DỮ LIỆU
# =========================

tesco = pd.read_csv(TESCO_INPUT)
tiki = pd.read_csv(TIKI_INPUT)


# =========================
# TESCO: GBP -> VND
# =========================

tesco["Source_Currency"] = tesco["currency"].fillna("GBP")

tesco["Original_Price_VND"] = (
    pd.to_numeric(tesco["Original_Price"], errors="coerce")
    * GBP_TO_VND
).round()

tesco["Discount_Price_VND"] = (
    pd.to_numeric(tesco["Discount_Price"], errors="coerce")
    * GBP_TO_VND
).round()


# =========================
# TIKI: VND
# =========================

tiki["Source_Currency"] = "VND"

tiki["Original_Price_VND"] = pd.to_numeric(
    tiki["Original_Price"],
    errors="coerce"
).round()

tiki["Discount_Price_VND"] = pd.to_numeric(
    tiki["Discount_Price"],
    errors="coerce"
).round()


# =========================
# VALIDATION
# =========================

assert "Product_ID" in tesco.columns
assert "Product_ID" in tiki.columns

assert "Discount_Price_VND" in tesco.columns
assert "Discount_Price_VND" in tiki.columns

assert tiki["Discount_Price_VND"].notna().all()


# =========================
# LƯU FILE
# =========================

tesco.to_csv(
    TESCO_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)

tiki.to_csv(
    TIKI_OUTPUT,
    index=False,
    encoding="utf-8-sig"
)


# =========================
# SUMMARY
# =========================

print("=== TESCO ===")
print("Rows:", len(tesco))
print(
    "Missing Discount_Price_VND:",
    tesco["Discount_Price_VND"].isna().sum()
)

print("\n=== TIKI ===")
print("Rows:", len(tiki))
print(
    "Missing Discount_Price_VND:",
    tiki["Discount_Price_VND"].isna().sum()
)

print("\nSaved:")
print(TESCO_OUTPUT)
print(TIKI_OUTPUT)

print("\nSTANDARDIZE CURRENCY PASSED")