# 📌 Where & When: Optimizing Aadhaar Enrolment and Update Services

**Hackathon:** UIDAI Data Hackathon 2026  
**Problem Owner:** Unique Identification Authority of India (UIDAI)

## 👥 Team Members
- **Sharafath Ahammed V**
- **Hanan Hafees Mohammed**
- **Anagha P**
- **Marzook KK**

🔗 **GitHub Repository:**  
https://github.com/sharafath07/Uidai-Hackathon

---

## 🧠 Problem Overview

Aadhaar enrolment and biometric update centres experience **uneven service demand across regions and seasons**.  
Certain regions face **large biometric update backlogs**, while specific months see **sudden demand spikes** that lead to long queues and system overload. At the same time, low-demand periods cause underutilization of resources.

Due to the absence of data-driven planning, authorities often respond **reactively rather than proactively**.

---

## 🎯 Project Objective

This project answers two critical questions:

- **WHERE** do biometric update gaps exist?
- **WHEN** does Aadhaar service demand peak?

By combining **regional (spatial)** and **seasonal (temporal)** analysis, the project enables **efficient resource allocation** and smoother Aadhaar service delivery.

---

## 📊 Core Ideas

### 1️⃣ Regional Update Gaps (WHERE)

We calculate the biometric update gap using:

Update Gap = Eligible Population (5–17) − Updates Completed


Regions with large negative gaps indicate persistent biometric update backlogs.

---

### 2️⃣ Seasonal Workload Analysis (WHEN)

Monthly enrolment and biometric update data is analyzed to identify:
- Busy months
- Slow months
- Sudden demand spikes
- Seasonal workload patterns

---

### 3️⃣ Priority Score (WHERE + WHEN)

A **Priority Score** is computed by combining:
- Normalized regional update gaps
- Normalized monthly workload intensity

High scores indicate **regions that require urgent intervention during critical months**.

---

## 🛠️ Methodology

1. Load and merge multiple UIDAI CSV datasets  
2. Clean and standardize dates, states, districts, and pincodes  
3. Compute:
   - Regional update gaps
   - Monthly workload
   - 3-month moving average
   - Seasonal index  
4. Detect unusual demand spikes using statistical thresholds  
5. Generate priority scores and ranked outputs  

---

## 📈 Outputs

### 📂 Generated CSV Files
- `state_update_gap.csv`
- `monthly_workload_analysis.csv`
- `priority_districts.csv`

### 🖼️ Generated Visualizations (PNG)
- Regional biometric update gap (bar chart)
- Monthly Aadhaar workload trend
- Busy vs slow months (pie chart)
- Unusual demand spikes
- 3-month moving average
- Seasonal index
- High-priority districts

All outputs are saved inside the `/output` directory.

---

## 🧪 Tech Stack

- **Python**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**

---

## ▶️ How to Run the Project

```bash
pip install pandas numpy matplotlib seaborn
python run_analysis.py
