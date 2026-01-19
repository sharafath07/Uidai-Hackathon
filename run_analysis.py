import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# =====================================================
# CONFIGURATION
# =====================================================
DATA_DIR = "data"
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BIOMETRIC_FILES = [
    "api_data_aadhar_biometric_1.csv",
    "api_data_aadhar_biometric_2.csv",
    "api_data_aadhar_biometric_3.csv"
]

ENROLMENT_FILES = [
    "api_data_aadhar_enrolment_1.csv",
    "api_data_aadhar_enrolment_2.csv",
    "api_data_aadhar_enrolment_3.csv"
]

# =====================================================
# HELPER FUNCTION
# =====================================================
def load_and_merge(files, columns):
    frames = []
    for f in files:
        print(f"Loading {f}...")
        df = pd.read_csv(os.path.join(DATA_DIR, f))
        df = df[columns]
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

# =====================================================
# LOAD DATA
# =====================================================
biometric = load_and_merge(
    BIOMETRIC_FILES,
    ["date", "state", "district", "bio_age_5_17"]
)

enrolment = load_and_merge(
    ENROLMENT_FILES,
    ["date", "state", "district", "age_0_5", "age_5_17", "age_18_greater"]
)

# =====================================================
# DATE PROCESSING
# =====================================================
for df in [biometric, enrolment]:
    df["date"] = pd.to_datetime(df["date"], dayfirst=True, errors="coerce")
    df.dropna(subset=["date"], inplace=True)
    df["month"] = df["date"].dt.to_period("M")

# =====================================================
# 1. WHERE – UPDATE GAP ANALYSIS
# =====================================================
need = enrolment.groupby(["state", "district"])["age_5_17"].sum()
done = biometric.groupby(["state", "district"])["bio_age_5_17"].sum()

gap_df = pd.concat([need, done], axis=1).fillna(0)
gap_df.columns = ["eligible", "completed"]
gap_df["update_gap"] = gap_df["eligible"] - gap_df["completed"]
gap_df["update_gap_ratio"] = gap_df["update_gap"] / gap_df["eligible"].replace(0, 1)

gap_df.to_csv(f"{OUTPUT_DIR}/regional_update_gaps.csv")

# ---- VISUAL 1: STATE UPDATE GAP ----
state_gap = gap_df.groupby("state")["update_gap"].sum().sort_values(ascending=False)

plt.figure(figsize=(10,6))
state_gap.head(10).plot(kind="bar")
plt.title("Top 10 States with Highest Biometric Update Backlogs")
plt.ylabel("Update Gap")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/state_update_gap.png")
plt.close()

# =====================================================
# 2. WHEN – SEASONAL WORKLOAD
# =====================================================
enrolment["total_enrolments"] = (
    enrolment["age_0_5"] +
    enrolment["age_5_17"] +
    enrolment["age_18_greater"]
)

monthly_enrol = enrolment.groupby("month")["total_enrolments"].sum()
monthly_updates = biometric.groupby("month")["bio_age_5_17"].sum()

monthly = pd.concat([monthly_enrol, monthly_updates], axis=1).fillna(0)
monthly.columns = ["enrolments", "updates"]
monthly["total_workload"] = monthly["enrolments"] + monthly["updates"]

monthly.to_csv(f"{OUTPUT_DIR}/monthly_workload.csv")

# Convert PeriodIndex → string for plotting
x = monthly.index.astype(str)

# ---- VISUAL 2: MONTHLY WORKLOAD ----
plt.figure(figsize=(10,5))
plt.plot(x, monthly["total_workload"], marker="o")
plt.title("Monthly Aadhaar Workload")
plt.ylabel("Total Transactions")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/monthly_workload.png")
plt.close()

# ---- VISUAL 3: BUSY VS SLOW MONTHS ----
avg_load = monthly["total_workload"].mean()
busy = (monthly["total_workload"] > avg_load).sum()
slow = (monthly["total_workload"] <= avg_load).sum()

plt.figure()
plt.pie(
    [busy, slow],
    labels=["Busy Months", "Slow Months"],
    autopct="%1.1f%%"
)
plt.title("Busy vs Slow Months")
plt.savefig(f"{OUTPUT_DIR}/busy_vs_slow_months.png")
plt.close()

# =====================================================
# 3. SPIKE DETECTION
# =====================================================
mean = monthly["total_workload"].mean()
std = monthly["total_workload"].std()

monthly["spike"] = monthly["total_workload"] > (mean + 2 * std)

# ---- VISUAL 4: SPIKES ----
colors = ["red" if v else "blue" for v in monthly["spike"]]

plt.figure(figsize=(10,5))
plt.plot(x, monthly["total_workload"], marker="o")
plt.scatter(x, monthly["total_workload"], c=colors)
plt.title("Unusual Monthly Demand Spikes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/monthly_spikes.png")
plt.close()

# =====================================================
# 4. 3-MONTH MOVING AVERAGE
# =====================================================
monthly["moving_avg_3"] = monthly["total_workload"].rolling(3).mean()

# ---- VISUAL 5: MOVING AVERAGE ----
plt.figure(figsize=(10,5))
plt.plot(x, monthly["total_workload"], label="Actual")
plt.plot(x, monthly["moving_avg_3"], label="3-Month Moving Average")
plt.legend()
plt.title("3-Month Moving Average of Aadhaar Workload")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/moving_average.png")
plt.close()

# =====================================================
# 5. SEASONAL INDEX
# =====================================================
overall_avg = monthly["total_workload"].mean()
monthly["seasonal_index"] = monthly["total_workload"] / overall_avg
monthly.to_csv(f"{OUTPUT_DIR}/monthly_seasonal_index.csv")

# ---- VISUAL 6: SEASONAL INDEX ----
plt.figure(figsize=(10,5))
plt.bar(x, monthly["seasonal_index"])
plt.title("Seasonal Index by Month")
plt.ylabel("Seasonal Index")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/seasonal_index.png")
plt.close()

# =====================================================
# 6. PRIORITY SCORE (WHERE + WHEN)
# =====================================================
gap_norm = (
    gap_df["update_gap"] - gap_df["update_gap"].min()
) / (
    gap_df["update_gap"].max() - gap_df["update_gap"].min()
)

month_norm = (
    monthly["total_workload"] - monthly["total_workload"].min()
) / (
    monthly["total_workload"].max() - monthly["total_workload"].min()
)

priority_records = []

for (state, district), g in gap_norm.items():
    for m, mv in month_norm.items():
        priority_records.append({
            "state": state,
            "district": district,
            "month": str(m),
            "priority_score": g * mv
        })

priority_df = pd.DataFrame(priority_records)
priority_df = priority_df.sort_values("priority_score", ascending=False)
priority_df.to_csv(f"{OUTPUT_DIR}/priority_scores.csv", index=False)

# ---- VISUAL 7: TOP PRIORITY DISTRICTS ----
top_priority = (
    priority_df
    .groupby("district")["priority_score"]
    .max()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10,6))
top_priority.plot(kind="bar")
plt.title("Top 10 High-Priority Districts")
plt.ylabel("Priority Score")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/top_priority_districts.png")
plt.close()

# =====================================================
# FINAL MESSAGE
# =====================================================
print("\n✅ ALL ANALYSIS & VISUALIZATION COMPLETED SUCCESSFULLY")
print("All CSV files and PNG charts saved in 'output/' folder")
