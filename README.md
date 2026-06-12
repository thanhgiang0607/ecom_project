# 📊 Olist E-Commerce Analytics Platform


[![Live Demo](https://img.shields.io/badge/Live-Demo-red?style=flat-square&logo=streamlit)](https://ecomprojectgit-546sw5cdmkkqffyltmbq7u.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)]()
[![dbt](https://img.shields.io/badge/dbt-Core-orange?style=flat-square&logo=dbt)]()
[![DuckDB](https://img.shields.io/badge/DuckDB-Data_Warehouse-yellow?style=flat-square)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)]()

> End-to-End Modern Data Stack (MDS) project for transforming, analyzing, and visualizing Brazilian e-commerce data.

> End-to-End Modern Data Stack (MDS) project for transforming, analyzing, and visualizing Brazilian e-commerce data using DuckDB, dbt, Python, and Streamlit.

---

## 🚀 Project Overview

This project demonstrates a complete analytics workflow built on the **Modern Data Stack (MDS)** paradigm. Raw transactional data from the Olist Brazilian E-Commerce dataset is transformed into business-ready analytical models, enriched with advanced customer analytics, and delivered through an interactive executive dashboard.

The platform enables stakeholders to monitor operational performance, evaluate customer retention, and identify high-value customer segments through data-driven insights.

---

## 🎯 Business Objectives

The project addresses three key business questions:

- How is the e-commerce operation performing across orders, revenue, and logistics?
- Which customer segments generate the highest business value?
- How effectively does the platform retain customers over time?

---

## 🏗️ Architecture

```text
                   ┌───────────────────┐
                   │   Raw CSV Files   │
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │      DuckDB       │
                   │ Data Warehouse    │
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │       dbt         │
                   │ Data Modeling     │
                   └─────────┬─────────┘
                             │
          ┌──────────────────┴──────────────────┐
          ▼                                     ▼
 ┌─────────────────┐                 ┌─────────────────┐
 │  RFM Analysis   │                 │ Cohort Analysis │
 │    (Python)     │                 │    (Python)     │
 └────────┬────────┘                 └────────┬────────┘
          └──────────────────┬───────────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Streamlit Dashboard │
                  └─────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---------|------------|
| Storage | DuckDB |
| Data Transformation | dbt Core |
| Data Processing | Python, Pandas, NumPy |
| Visualization | Plotly |
| Dashboard | Streamlit |
| Version Control | Git & GitHub |

---

## 📂 Project Structure

```text
ecom_project/
│
├── data/
│   └── raw/                    # Raw Olist dataset (CSV)
│
├── olist_pipeline/             # dbt Core Transformation Layer
│   ├── models/
│   │   ├── staging.sql
│   │   └── marts.sql
│   └── dbt_project.yml
│
├── ai_visualizations/          # ML Model evaluation plots
│
├── app.py                      # Streamlit High-Fidelity Dashboard
├── model_training.py           # AI/ML Intelligence Pipeline
├── load_data.py                # Data Acquisition Script
├── requirements.txt            # Dependency Manifest
└── README.md
```

---

## 🧠 AI/ML Intelligence Layer

The platform is powered by an automated machine learning pipeline (`model_training.py`) that enriches transactional data with predictive insights:

### 1. AI Churn Prediction
- **Algorithm:** Gradient Boosting Classifier
- **Features:** RFM metrics (Recency, Frequency, Monetary)
- **Outcome:** Calculates churn risk probability for every customer.
- **Business Value:** Enables proactive retention campaigns for "At-Risk" segments.

### 2. Collaborative Filtering Recommendation Engine
- **Methodology:** Latent Factor Modeling via Truncated SVD (Matrix Factorization)
- **Logic:** Analyzes historical purchase patterns to predict the top 3 most relevant product categories for each unique customer.
- **Business Value:** Powers personalized marketing and cross-selling strategies.

### 3. NLP Sentiment Analysis
- **Scope:** Analyzes customer order reviews.
- **Outcome:** Classifies customer sentiment into Positive, Neutral, and Negative states.
- **Business Value:** Provides immediate feedback on customer satisfaction and operational bottlenecks.

---

## 📈 Key Analytics Modules

### 1. Operations & Logistics Analytics
Monitor revenue trends, order volume, and delivery performance. Average delivery time is approximately **12 days**, with significant regional variations.

### 2. Customer Segmentation (RFM + AI)
Customers are segmented using the RFM methodology and enriched with **AI Churn Risk Scores**.
- **Champions & Loyalists:** High-value targets.
- **At-Risk:** Identified by both RFM position and AI churn probability.

### 3. Cohort Retention Analysis
Monthly customer cohorts are tracked to evaluate repeat purchase behavior. The dashboard provides interactive heatmaps and retention curves to visualize the customer lifecycle.

---

## 📊 Dashboard Features

### Executive Overview
- KPI cards for Revenue, Orders, Freight, and Fulfillment.
- Monthly Revenue Velocity and Top 10 Categories.
- NLP Sentiment Breakdown.

### Customer Intelligence Explorer
- Interactive RFM segmentation.
- **AI-Powered Drill-down:** View individual customer churn risk and personalized product recommendations.

### Retention Analytics
- Cohort heatmaps (M+1 to M+12).
- Retention curves for historical cohorts.

---

## ⚡ Getting Started

### 1. Clone & Setup
```bash
git clone https://github.com/thanhgiang0607/ecom_project.git
cd ecom_project
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Data Acquisition
```bash
python load_data.py
```

### 3. Run dbt Models
```bash
cd olist_pipeline
dbt run
cd ..
```

### 4. Train AI Models
```bash
python model_training.py
```

### 5. Launch Dashboard
```bash
streamlit run app.py
```

The dashboard will be available locally at:

```text
http://localhost:8501
```

---

## 📌 Key Outcomes

✅ Built a complete Modern Data Stack pipeline

✅ Implemented dimensional data modeling with dbt

✅ Developed customer segmentation using RFM methodology

✅ Performed cohort retention analysis

✅ Created an interactive executive dashboard

✅ Delivered actionable business insights from raw transactional data

---

## 🌐 Live Demo

Experience the deployed application here:

🚀 **Interactive Dashboard:**  
https://ecomprojectgit-546sw5cdmkkqffyltmbq7u.streamlit.app/

The dashboard is publicly hosted on Streamlit Community Cloud and provides access to:

- Executive KPI monitoring
- Revenue & logistics analytics
- RFM customer segmentation
- Cohort retention analysis
- Interactive filtering and drill-down exploration

No installation required — simply open the link and start exploring the insights.

---


## 👨‍💻 Author

**Thanh Giang Nguyen**

Data Analytics • Data Engineering • Business Intelligence • E-commerce • Data Visualization

GitHub: https://github.com/thanhgiang0607

---

⭐ If you find this project useful, consider giving it a star.