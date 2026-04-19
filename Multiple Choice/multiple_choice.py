import pandas as pd
import numpy as np

DATA_DIR = "./Data/"

print("Loading data...")
orders    = pd.read_csv(DATA_DIR + "orders.csv",     parse_dates=["order_date"])
products  = pd.read_csv(DATA_DIR + "products.csv")
returns   = pd.read_csv(DATA_DIR + "returns.csv")
web       = pd.read_csv(DATA_DIR + "web_traffic.csv")
items     = pd.read_csv(DATA_DIR + "order_items.csv")
customers = pd.read_csv(DATA_DIR + "customers.csv")
geo       = pd.read_csv(DATA_DIR + "geography.csv")
payments  = pd.read_csv(DATA_DIR + "payments.csv")

print("=" * 30)

# Q1
o = orders.sort_values(["customer_id", "order_date"])
o["gap"] = o.groupby("customer_id")["order_date"].diff().dt.days
median_gap = o[o["gap"].notna()]["gap"].median()
q1 = min(["A","B","C","D"], key=lambda x: abs(median_gap - [30,90,180,365][["A","B","C","D"].index(x)]))
print(f"Q1: {q1}  (median gap = {median_gap:.1f} ngày)")

# Q2
products["margin"] = (products["price"] - products["cogs"]) / products["price"]
ans = products.groupby("segment")["margin"].mean()
seg_map = {"Premium":"A", "Performance":"B", "Activewear":"C", "Standard":"D"}
q2 = seg_map.get(ans.idxmax(), ans.idxmax())
print(f"Q2: {q2}  ({ans.idxmax()}, margin = {ans.max():.4f})")

# Q3
merged3 = returns.merge(products[["product_id","category"]], on="product_id")
sw = merged3[merged3["category"] == "Streetwear"]
top_reason = sw["return_reason"].value_counts().idxmax()
reason_map = {"defective":"A", "wrong_size":"B", "changed_mind":"C", "not_as_described":"D"}
q3 = reason_map.get(top_reason, top_reason)
print(f"Q3: {q3}  ({top_reason})")

# Q4
ans4 = web.groupby("traffic_source")["bounce_rate"].mean()
top_src = ans4.idxmin()
src_map = {"organic_search":"A", "paid_search":"B", "email_campaign":"C", "social_media":"D"}
q4 = src_map.get(top_src, top_src)
print(f"Q4: {q4}  ({top_src}, bounce = {ans4.min():.4f})")

# Q5
pct = items["promo_id"].notna().mean() * 100
if pct < 18:        q5 = "A"
elif pct < 31:      q5 = "B"
elif pct < 46:      q5 = "C"
else:               q5 = "D"
print(f"Q5: {q5}  ({pct:.1f}%)")

# Q6
order_counts = orders.groupby("customer_id").size().reset_index(name="n_orders")
cust = customers[customers["age_group"].notna()].merge(order_counts, on="customer_id", how="left")
cust["n_orders"] = cust["n_orders"].fillna(0)
ans6 = cust.groupby("age_group")["n_orders"].mean()
top_age = ans6.idxmax()
age_map = {"55+":"A", "25-34":"B", "35-44":"C", "45-54":"D"}
q6 = age_map.get(top_age, top_age)
print(f"Q6: {q6}  ({top_age}, avg orders = {ans6.max():.3f})")

# Q7
order_rev = items.copy()
order_rev["line_rev"] = order_rev["quantity"] * order_rev["unit_price"] - order_rev["discount_amount"]
order_rev = order_rev.groupby("order_id")["line_rev"].sum().reset_index()
merged7 = orders[["order_id","zip"]].merge(geo[["zip","region"]], on="zip").merge(order_rev, on="order_id")
ans7 = merged7.groupby("region")["line_rev"].sum()
top_region = ans7.idxmax()
reg_map = {"West":"A", "Central":"B", "East":"C"}
q7 = reg_map.get(top_region, "D")
print(f"Q7: {q7}  ({top_region}, revenue = {ans7.max():,.0f})")

# Q8
cancelled = orders[orders["order_status"] == "cancelled"]
top_pay = cancelled["payment_method"].value_counts().idxmax()
pay_map = {"credit_card":"A", "cod":"B", "paypal":"C", "bank_transfer":"D"}
q8 = pay_map.get(top_pay, top_pay)
print(f"Q8: {q8}  ({top_pay})")

# Q9
items_s = items.merge(products[["product_id","size"]], on="product_id")
ret_s   = returns.merge(products[["product_id","size"]], on="product_id")
sizes = ["S","M","L","XL"]
total   = items_s[items_s["size"].isin(sizes)].groupby("size").size()
ret_cnt = ret_s[ret_s["size"].isin(sizes)].groupby("size").size()
rate    = ret_cnt / total
top_size = rate.idxmax()
size_map = {"S":"A", "M":"B", "L":"C", "XL":"D"}
q9 = size_map.get(top_size, top_size)
print(f"Q9: {q9}  ({top_size}, rate = {rate.max():.4f})")

# Q10
ans10 = payments.groupby("installments")["payment_value"].mean()
top_inst = ans10.idxmax()
inst_map = {1:"A", 3:"B", 6:"C", 12:"D"}
q10 = inst_map.get(top_inst, str(top_inst))
print(f"Q10: {q10}  ({top_inst} kỳ, avg = {ans10.max():,.2f})")

print("=" * 30)
print(f"\nTóm tắt đáp án:")
print(f"Q1={q1}  Q2={q2}  Q3={q3}  Q4={q4}  Q5={q5}")
print(f"Q6={q6}  Q7={q7}  Q8={q8}  Q9={q9}  Q10={q10}")