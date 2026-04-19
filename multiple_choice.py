import pandas as pd
import numpy as np

DATA_DIR = "./Data/"   

def load(name):
    return pd.read_csv(DATA_DIR + name, parse_dates=True, low_memory=False)

print("Loading data...")
orders     = pd.read_csv(DATA_DIR + "orders.csv",      parse_dates=["order_date"])
products   = pd.read_csv(DATA_DIR + "products.csv")
returns    = pd.read_csv(DATA_DIR + "returns.csv")
web        = pd.read_csv(DATA_DIR + "web_traffic.csv")
items      = pd.read_csv(DATA_DIR + "order_items.csv")
customers  = pd.read_csv(DATA_DIR + "customers.csv")
geo        = pd.read_csv(DATA_DIR + "geography.csv")
payments   = pd.read_csv(DATA_DIR + "payments.csv")

print("\n" + "="*50)

# Q1 — Median inter-order gap
print("Q1: Median inter-order gap")
o = orders.sort_values(["customer_id","order_date"])
o["gap"] = o.groupby("customer_id")["order_date"].diff().dt.days
multi = o[o["gap"].notna()]
median_gap = multi["gap"].median()
print(f"  Median gap = {median_gap:.1f} days")
for opt, val in [("A",30),("B",90),("C",180),("D",365)]:
    if abs(median_gap - val) == min(abs(median_gap-v) for v in [30,90,180,365]):
        print(f"  => Đáp án: {opt}") ; break

print()

# Q2 — Segment có gross margin cao nhất
print("Q2: Segment với gross margin cao nhất")
products["margin"] = (products["price"] - products["cogs"]) / products["price"]
ans = products.groupby("segment")["margin"].mean()
print(ans.round(4).to_string())
print(f"  => Đáp án: {ans.idxmax()}")

print()

# Q3 — Return reason phổ biến nhất trong Streetwear
print("Q3: Return reason phổ biến nhất — Streetwear")
merged = returns.merge(products[["product_id","category"]], on="product_id")
sw = merged[merged["category"] == "Streetwear"]
ans = sw["return_reason"].value_counts()
print(ans.to_string())
print(f"  => Đáp án: {ans.idxmax()}")

print()

# Q4 — Traffic source có bounce rate thấp nhất
print("Q4: Traffic source — bounce rate thấp nhất")
ans = web.groupby("traffic_source")["bounce_rate"].mean()
print(ans.round(4).to_string())
print(f"  => Đáp án: {ans.idxmin()}")

print()

# Q5 — % order_items có promo
print("Q5: % dòng order_items có promo_id")
pct = items["promo_id"].notna().mean() * 100
print(f"  {pct:.1f}%")
for opt, lo, hi in [("A",0,18),("B",18,31),("C",31,46),("D",46,100)]:
    if lo <= pct < hi:
        print(f"  => Đáp án: {opt}") ; break

print()

# Q6 — Age group có avg orders/customer cao nhất
print("Q6: Age group — avg orders/customer cao nhất")
order_counts = orders.groupby("customer_id").size().reset_index(name="n_orders")
cust = customers[customers["age_group"].notna()].merge(order_counts, on="customer_id", how="left")
cust["n_orders"] = cust["n_orders"].fillna(0)
ans = cust.groupby("age_group")["n_orders"].mean()
print(ans.round(3).to_string())
print(f"  => Đáp án: {ans.idxmax()}")

print()

# Q7 — Region có tổng revenue cao nhất
print("Q7: Region có tổng revenue cao nhất")
order_rev = items.copy()
order_rev["line_rev"] = order_rev["quantity"] * order_rev["unit_price"] - order_rev["discount_amount"]
order_rev = order_rev.groupby("order_id")["line_rev"].sum().reset_index()
merged = orders[["order_id","zip"]].merge(geo[["zip","region"]], on="zip")
merged = merged.merge(order_rev, on="order_id")
ans = merged.groupby("region")["line_rev"].sum()
print(ans.round(0).to_string())
print(f"  => Đáp án: {ans.idxmax()}")

print()

# Q8 — Payment method phổ biến nhất trong đơn cancelled
print("Q8: Payment method trong đơn cancelled")
cancelled = orders[orders["order_status"] == "cancelled"]
ans = cancelled["payment_method"].value_counts()
print(ans.to_string())
print(f"  => Đáp án: {ans.idxmax()}")

print()

# Q9 — Size có return rate cao nhất
print("Q9: Size có return rate cao nhất")
items_s = items.merge(products[["product_id","size"]], on="product_id")
ret_s   = returns.merge(products[["product_id","size"]], on="product_id")
total   = items_s[items_s["size"].isin(["S","M","L","XL"])].groupby("size").size()
ret_cnt = ret_s[ret_s["size"].isin(["S","M","L","XL"])].groupby("size").size()
rate    = (ret_cnt / total).round(4)
print(rate.to_string())
print(f"  => Đáp án: {rate.idxmax()}")

print()

# Q10 — Installment plan có avg payment value cao nhất
print("Q10: Installment plan — avg payment value cao nhất")
ans = payments.groupby("installments")["payment_value"].mean()
print(ans.round(2).to_string())
print(f"  => Đáp án: {ans.idxmax()} kỳ")
