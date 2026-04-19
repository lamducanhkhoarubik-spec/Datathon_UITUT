# 🏆 Datathon 2026 – The Grid Breakers (HCM-UIT & HCM-UT Collaboration)

### Breaking Business Boundaries with Data

🚀 Official repository for our participation in **Datathon 2026 – The Grid Breakers**,  
a data science competition hosted by **VinTelligence** and **VinUniversity Data Science & AI Club**.

This repository showcases our work for Datathon 2026, including data analysis, visualization, and sales forecasting models.

---

## 👥 Team Members

**Lâm Đức Anh Khoa**¹,  
**Trần Minh Khôi**¹,  
**Phạm Sơn Phúc**²,  
**Trần Ngọc Cát Tường**²

<br>

¹ Ho Chi Minh City University of Technology, VNU-HCM, Vietnam  
² Ho Chi Minh City University of Information Technology, VNU-HCM, Vietnam

---

## Team Task Assignment

| Member | Part | Task | Output |
|---|---|---|---|
| A | MCQ ✅ | Query all 10 multiple choice questions from data | `answers.txt` |
| B | EDA — Descriptive | Revenue trends, product breakdown, customer profile | 3-4 charts + insight |
| C | EDA — Diagnostic | Promo effectiveness, return reasons, customer behavior | 3-4 charts + insight |
| D | EDA — Predictive + Prescriptive | Inventory forecast, promo optimization, personalization | 3-4 charts + insight |
| E | Forecasting | ML pipeline, feature engineering, Kaggle submission | `submission.csv` |
| F | Report | LaTeX NeurIPS template, compile charts + insights | `report.pdf` |

---

## Analytics Framework — 4 Pillars

> **Rule:** Every analysis must cover all 4 levels. Never stop at Descriptive.

| Level | Question | Example |
|---|---|---|
| **Descriptive** | What happened? | Revenue in Nov–Dec is 40% above monthly average |
| **Diagnostic** | Why did it happen? | Year-end promotions + holiday season drove order spikes |
| **Predictive** | What will happen? | Pattern will repeat → forecast Nov 2023 up ~35% |
| **Prescriptive** | What should we do? | Stock up 30% from October, concentrate ad budget in week 3–4 of November |

---

## EDA Checklist

### 1. Descriptive Analytics — *What happened? (2012–2022)*

> Reconstruct the full business picture from historical data.

- [ ] **Revenue & Profitability** — Total `Revenue`, `COGS`, and gross profit over time (yearly / quarterly / monthly)
- [ ] **Product Mix** — Sales breakdown by `category`, `segment`, color, and size
- [ ] **Customer Profile** — Distribution by `age_group`, `gender`, and geography (`region`, `city`)
- [ ] **Acquisition Channels** — Share of customers by `acquisition_channel` and `device_type`
- [ ] **Operations** — Average delivery time (`order_date` → `delivery_date`) and average `shipping_fee`

---

### 2. Diagnostic Analytics — *Why did it happen?*

> Cross-join tables to explain fluctuations and root causes.

- [ ] **Promotion Effectiveness** — Compare revenue between orders with `promo_id` (not null) vs without. Check whether `stackable_flag` actually increases basket size (`quantity`)
- [ ] **Return Root Cause** — Join `returns.csv` + `products.csv` to identify if specific product lines or `size` values are frequently returned due to `defective` or `wrong_size`
- [ ] **Customer Behavior** — Compute inter-order gap to understand loyalty vs churn patterns
- [ ] **Web Traffic Correlation** — Check whether high `bounce_rate` is tied to specific `traffic_source` values

---

### 3. Predictive Analytics — *What will happen?*

> Use trends to forecast risks and opportunities.

- [ ] **Revenue Forecast** *(Part 3 requirement)* — Predict `Revenue` and `COGS` for 01/01/2023 – 01/07/2024
- [ ] **Inventory Stockout Forecast** — Use `sell_through_rate` and `days_of_supply` to flag products at risk of `stockout_flag = 1` next month
- [ ] **Regional Demand Forecast** — Predict which `region` will see the highest revenue growth based on new `signup_date` trends

---

### 4. Prescriptive Analytics — *What should we do?*

> Deliver concrete, quantified business recommendations.

- [ ] **Basket Optimization** — Identify product pairs frequently bought together → design combo bundles to increase `payment_value`
- [ ] **Promotion Strategy** — Recommend optimal `discount_value` per `category` to stimulate demand while protecting gross margin (`price` − `cogs`)
- [ ] **Operations Improvement** — Recommend warehouse restructuring or alternative shipping partners for regions with long delivery times or high `shipping_fee`
- [ ] **Marketing Personalization** — Propose targeted ad messaging per customer segment (e.g. customers aged 25–34 who order via `mobile_app` on weekends)

---

## Storytelling Tips (for high creativity score)

**1. Connect the tables — don't analyze files in isolation**
```
web_traffic → orders → returns
= full customer journey from visit to purchase to return
```

**2. Always quantify your recommendations**
```
❌ "We should offer discounts on Streetwear"
✅ "A 10% discount on Streetwear could increase sales volume by 15%
    but reduce gross margin by 5% — net positive if volume uplift holds"
```

**3. Report format**
- Template: NeurIPS LaTeX (https://neurips.cc/Conferences/2025/CallForPapers)
- Max 4 pages (excluding references and appendix)
- Every chart must have: title, axis labels, legend, and a 2–3 line insight caption

---

## Forecasting Pipeline

```
1. Load sales.csv → plot raw series → decompose (Trend + Seasonality + Residual)
2. Feature engineering
3. Train XGBoost + Prophet
4. SHAP analysis → explain model in business language
5. Time-series cross validation (no random split — forward walk only)
6. Generate submission.csv
```

**Features to engineer:**
```python
# Lag features
lag_1, lag_7, lag_30, lag_365

# Rolling statistics
rolling_mean_7, rolling_mean_30

# Calendar features
month, quarter, dayofweek, is_weekend, dayofyear

# Derived features
cogs_ratio = COGS / Revenue
gross_profit = Revenue - COGS
```

**Avoid data leakage:**
```python
# ✅ Correct — time-series split only
from sklearn.model_selection import TimeSeriesSplit
tscv = TimeSeriesSplit(n_splits=5)

# ❌ Wrong — never use random split on time series
train_test_split(X, y, random_state=42)
```

---

## Project Structure

```
datathon-2026/
├── Data/
│   ├── customers.csv
│   ├── geography.csv
│   ├── inventory.csv
│   ├── order_items.csv
│   ├── orders.csv
│   ├── payments.csv
│   ├── products.csv
│   ├── promotions.csv
│   ├── returns.csv
│   ├── reviews.csv
│   ├── sales.csv
│   ├── sample_submission.csv
│   ├── shipments.csv
│   └── web_traffic.csv
├── Multiple Choice/
│   ├── mcq_explain.html
│   ├── multiple_choice.py
│   └── solve_mcq.ipynb
├── code/
│   ├── eda/
│   │   ├── descriptive.ipynb
│   │   ├── diagnostic.ipynb
│   │   └── predictive_prescriptive.ipynb
│   └── forecasting/
│       └── forecast_pipeline.ipynb
├── report/
│   └── main.tex
├── submission.csv
└── README.md
```

---

## Timeline

| Deadline | Task |
|---|---|
| Tonight | Setup GitHub, assign tasks, first draft |
| Tomorrow morning | MCQ finalized ✅ |
| Tomorrow afternoon | EDA draft complete with charts |
| Tomorrow evening | First Kaggle submission |
| Before final deadline | Report complete, GitHub pushed public |

---

## Submission Checklist

- [ ] `submission.csv` uploaded to Kaggle — correct row order matching `sample_submission.csv`
- [ ] Report PDF — max 4 pages, NeurIPS template
- [ ] GitHub repo public + README + link in report
- [ ] Official submission form filled
- [ ] Student ID photos from all members
- [ ] Confirmed attendance at Finals — 23/05/2026, VinUniversity, Hanoi

---

## Links

- Kaggle: https://www.kaggle.com/competitions/datathon-2026-round-1
- NeurIPS Template: https://neurips.cc/Conferences/2025/CallForPapers