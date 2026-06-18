# 📊 Olist E-Commerce Analytics Platform

[![Live Demo](https://img.shields.io/badge/Live-Demo-red?style=flat-square&logo=streamlit)](https://ecomprojectgit-546sw5cdmkkqffyltmbq7u.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)]()
[![dbt](https://img.shields.io/badge/dbt-Core-orange?style=flat-square&logo=dbt)]()
[![DuckDB](https://img.shields.io/badge/DuckDB-Data_Warehouse-yellow?style=flat-square)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red?style=flat-square&logo=streamlit)]()

> **End-to-End Modern Data Stack (MDS) project** for transforming, analyzing, and visualizing Brazilian e-commerce data using DuckDB, dbt, Python, and Streamlit.

---

## 🚀 Project Overview

This platform demonstrates a complete analytics workflow built on the **Modern Data Stack (MDS)** paradigm. Raw transactional data from the Olist Brazilian E-Commerce dataset is transformed into business-ready analytical models, enriched with advanced predictive insights, and delivered through a high-fidelity interactive dashboard.

The project bridges the gap between raw data engineering and executive decision-making by providing automated pipelines for data cleaning, dimensional modeling, and machine learning.

---

## 🏗️ Architecture & Data Flow

The project follows a modular architecture, ensuring scalability and separation of concerns:

```text
                   ┌───────────────────┐
                   │   Raw CSV Files   │ (Kaggle Dataset)
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │      DuckDB       │ (Local Data Warehouse)
                   │  OLAP Database    │
                   └─────────┬─────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │       dbt         │ (Staging & Marts Layers)
                   │ Data Modeling     │
                   └─────────┬─────────┘
                             │
          ┌──────────────────┴──────────────────┐
          ▼                                     ▼
 ┌─────────────────┐                 ┌─────────────────┐
 │  AI/ML Pipeline │                 │ Business Logic  │
 │ (model_training)│                 │  (Analytics)    │
 └────────┬────────┘                 └────────┬────────┘
          └──────────────────┬───────────────┘
                             ▼
                  ┌─────────────────────┐
                  │ Streamlit Dashboard │ (Executive Insights)
                  └─────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology | Description |
|---------|------------|-------------|
| **Storage** | **DuckDB** | In-process OLAP database for fast analytical queries. |
| **Orchestration** | **dbt Core** | Transformation layer for modular SQL modeling. |
| **Processing** | **Python (Pandas)** | Data manipulation and engineering. |
| **Intelligence** | **Scikit-Learn** | Machine learning for Churn & Recommendations. |
| **Visualization** | **Plotly** | High-fidelity interactive charting. |
| **Dashboard** | **Streamlit** | Modern web interface for data exploration. |

---

## 📂 Project Structure

```text
ecom_project/
├── data/raw/               # Raw Olist dataset (9 CSV files)
├── olist_pipeline/         # dbt Transformation Layer
│   ├── models/
│   │   ├── staging.sql     # Data cleaning & type casting
│   │   └── marts.sql       # Business logic & KPIs (Revenue, Logistics)
│   └── dbt_project.yml
├── ai_visualizations/      # ML Model evaluation plots (PNG)
├── app.py                  # Streamlit Dashboard (UI/UX Layer)
├── model_training.py       # AI/ML Pipeline (Churn, Recs, NLP)
├── load_data.py            # Data Acquisition (Kaggle API)
├── analytics.ipynb         # Deep-dive RFM research
├── eda.ipynb               # Exploratory Data Analysis
├── requirements.txt        # Dependency Manifest
└── README.md               # Documentation
```

---

## 🧠 AI/ML Intelligence Layer

The platform is powered by an automated machine learning pipeline (`model_training.py`) that enriches transactional data with predictive insights:

### 1. AI Churn Prediction
- **Algorithm:** `GradientBoostingClassifier`
- **Features:** RFM metrics (Recency, Frequency, Monetary).
- **Outcome:** Calculates churn risk probability for every customer.
- **Business Value:** Enables proactive retention campaigns for "At-Risk" segments.

### 2. Product Recommendation Engine
- **Methodology:** Latent Factor Modeling via `TruncatedSVD` (Matrix Factorization).
- **Logic:** Analyzes historical purchase patterns across categories to predict the top 3 most relevant products for each customer.
- **Business Value:** Powers personalized marketing and cross-selling.

### 3. NLP Sentiment Analysis
- **Scope:** Rule-based analysis of customer order reviews.
- **Outcome:** Classifies customer sentiment into **Positive**, **Neutral**, and **Negative**.
- **Business Value:** Provides immediate feedback on customer satisfaction and logistics bottlenecks.

---

## 📈 Key Analytics Modules

### 1. Executive Operations
- **Revenue Velocity:** Monthly trends and growth rates.
- **Logistics Performance:** Average delivery time (~12 days) and shipping cost analysis.
- **Geographic Distribution:** Top performing states (SP, RJ, MG).

### 2. Customer Intelligence (RFM)
Advanced segmentation categorizing customers into:
- **Champions:** Best customers, frequent and high spenders.
- **Loyalists:** Regular buyers with high potential.
- **At-Risk:** High churn probability identified by the AI model.

### 3. Cohort Retention
- **Retention Heatmaps:** Track customer stickiness over a 12-month horizon.
- **Cohort Curves:** Compare the health of different acquisition periods.

---

## ⚡ Getting Started

### 1. Environment Setup
```bash
git clone https://github.com/thanhgiang0607/ecom_project.git
cd ecom_project
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Data Ingestion
*Note: Requires Kaggle API credentials.*
```bash
python load_data.py
```

### 3. Data Transformation (dbt)
```bash
cd olist_pipeline
dbt run
cd ..
```

### 4. AI Model Training
```bash
python model_training.py
```

### 5. Launch Dashboard
```bash
streamlit run app.py
```

---

## 🌐 Live Demo

🚀 **Interactive Dashboard:** [Streamlit Cloud Link](https://ecomprojectgit-546sw5cdmkkqffyltmbq7u.streamlit.app/)

---

## 👨‍💻 Author

**Vu Thanh Giang Nguyen (Ciara)**

Data Analytics • Data Engineering • Machine Learning

GitHub: [thanhgiang0607](https://github.com/thanhgiang0607)
