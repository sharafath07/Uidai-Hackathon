# Where & When: Optimizing Aadhaar Enrolment and Update Services

## UIDAI Data Hackathon 2026

## 👥 Team Members
- [Sharafath Ahammed V](https://github.com/sharafath07)
- [Hanan Hafees Mohammed](https://github.com/hananhafees09)
- [Anagha P](https://github.com/anaghapraveen2007)
- [Marzook KK](https://github.com/marzook771)


GitHub Repository:  
https://github.com/sharafath07/Uidai-Hackathon

---

## 📌 Project Overview

Aadhaar enrolment and biometric update centres experience uneven service demand across regions and seasons.  
Some regions face persistent biometric update backlogs, while specific months experience sudden demand spikes that overload infrastructure.  

This project applies **statistical and time-series analysis** to answer two key questions:

- **WHERE** do Aadhaar service gaps exist?
- **WHEN** does demand peak?

By combining both dimensions into a **Priority Score**, the system enables proactive resource allocation, staff planning, and improved service delivery.

---

## 🎯 Objectives

- Identify regions with high biometric update backlogs  
- Detect busy and slow months using workload analysis  
- Detect unusual demand spikes  
- Forecast short-term workload trends  
- Combine spatial and temporal pressure into a Priority Score  

---

## 📂 Dataset Requirements (IMPORTANT)

To run the analysis successfully, **all CSV files must be saved inside a folder named `data/`**  
and **the filenames must be exactly as listed below**:

### Aadhaar Enrolment Files

api_data_aadhar_enrolment_1.csv
api_data_aadhar_enrolment_2.csv
api_data_aadhar_enrolment_3.csv


### Aadhaar Biometric Update Files

api_data_aadhar_biometric_1.csv
api_data_aadhar_biometric_2.csv
api_data_aadhar_biometric_3.csv


⚠️ **Do not rename the files**  
⚠️ **Do not move them outside the `data/` folder**

The analysis code automatically loads and merges these files based on the above names.

---

## 📁 Recommended Folder Structure

Uidai-Hackathon/
│
├── data/
│ ├── api_data_aadhar_enrolment_1.csv
│ ├── api_data_aadhar_enrolment_2.csv
│ ├── api_data_aadhar_enrolment_3.csv
│ ├── api_data_aadhar_biometric_1.csv
│ ├── api_data_aadhar_biometric_2.csv
│ └── api_data_aadhar_biometric_3.csv
│
├── output/
│ ├── charts/
│ └── csv/
│
├── run_analysis.py
├── requirements.txt
└── README.md


---

## ⚙️ How to Run the Project

1. Install dependencies:
```bash
   pip install -r requirements.txt 
```

2. Ensure all CSV files are placed correctly inside the data/ folder.

3. Run the analysis:
```bash
   python run_analysis.py
```

## 📊 Outputs Generated

The script automatically generates:

## 📈 Visual Outputs (saved as PNG)

- Regional update gap bar charts

- Busy vs slow month pie chart

- Monthly workload trend line

- Unusual demand spike detection

- 3-month moving average plot

- Seasonal index bar chart

- Quadrant of Neglect scatter plot

- Top high-risk states and districts

All images are saved in:
```bash
   output/charts/
```

## 📄 CSV Outputs

- State-wise update gap analysis

- Monthly workload summary

- Priority-ranked districts

Saved in:
```bash
   output/csv/
``` 
## 🔍 Methodology Summary

- Update Gap = Eligible Population − Updates Completed

- Monthly Workload = Enrolments + Biometric Updates

- Seasonal Index = Monthly Workload / Average Workload

- Priority Score = Normalized Update Gap + Normalized Monthly Load

This ensures decisions are based on both geography and seasonality, not either in isolation.

## 📄 Final Report

A detailed PDF report including explanations, equations, insights, and visual outputs is included in the repository.

## 🏁 Conclusion

This project transforms raw Aadhaar transaction data into actionable intelligence.
By identifying where service backlogs exist and when system pressure peaks, UIDAI can deploy targeted, timely interventions to ensure smoother Aadhaar service delivery.