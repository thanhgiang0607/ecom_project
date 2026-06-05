import duckdb
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier 
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams.update({'font.size': 10, 'figure.titlesize': 12})

output_dir = "ai_visualizations"
os.makedirs(output_dir, exist_ok=True)

print("🔌 [DATABASE] Connecting to local DuckDB storage...")
con = duckdb.connect("/Users/ciaranguyen/Documents/ecom_project/dev.duckdb")
print("✅ [DATABASE] Connection established successfully.\n")

print("" + "="*70)
print("🚀 STARTING END-TO-END AUTOMATED AI & MACHINE LEARNING PIPELINE")
print("" + "="*70 + "\n")

# =========================================================================
# MODULE 1: AI CHURN PREDICTION 
# =========================================================================
print("🧠 [MODULE 1] Training Churn Prediction Model...")
df_rfm = con.execute("SELECT * FROM main.analytics_rfm").df()
print(f"   ↳ Loaded {len(df_rfm):,} customer profiles from 'analytics_rfm'.")

df_rfm['is_churned'] = np.where((df_rfm['recency'] > 300) | (df_rfm['Segment'].isin(['At Risk', 'Lost'])), 1, 0)

X = df_rfm[['recency', 'frequency', 'monetary']]
y = df_rfm['is_churned']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model_churn = GradientBoostingClassifier(n_estimators=50, random_state=42)
model_churn.fit(X_train, y_train)

y_pred = model_churn.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"   ⭐ [EVALUATION] Model Accuracy Score: {acc:.2%}")
print("   ⭐ [METRICS] Classification Report under Terminal:")
print(classification_report(y_test, y_pred, target_names=['Active', 'Churned']))

# 📊 VISUALIZATION 1: Confusion Matrix & Feature Importance
print("   ↳ Generating Matrix and Feature Importance plots...")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax1, 
            xticklabels=['Active', 'Churned'], yticklabels=['Active', 'Churned'])
ax1.set_title("Confusion Matrix (Model Validation)")
ax1.set_xlabel("Predicted Label")
ax1.set_ylabel("True Label")

importances = model_churn.feature_importances_
indices = np.argsort(importances)
ax2.barh(range(X.shape[1]), importances[indices], color='#6366f1', align='center')
ax2.set_yticks(range(X.shape[1]))
ax2.set_yticklabels([X.columns[i] for i in indices])
ax2.set_title("Feature Importance (RFM Weights)")
ax2.set_xlabel("Relative Importance Score")

plt.tight_layout()
fig.savefig(f"{output_dir}/module1_churn_evaluation.png", dpi=300)
plt.close()
print(f"   📸 [SAVED] Plot exported to '{output_dir}/module1_churn_evaluation.png'")

model_churn.fit(X, y)
df_rfm['churn_risk_probability'] = model_churn.predict_proba(X)[:, 1]

avg_churn_risk = df_rfm['churn_risk_probability'].mean()
print(f"   ↳ Average Churn Risk Across Customer Base: {avg_churn_risk:.1%}")
print("   ↳ Exporting predictive outcomes to 'rfm_data.csv'...")
df_rfm.to_csv("rfm_data.csv", index=False)
print("✅ [MODULE 1] Finished Churn Prediction Pipeline.\n")

print("-" * 50)

# =========================================================================
# MODULE 2: RECOMMENDATION ENGINE 
# =========================================================================
print("🛍️ [MODULE 2] Computing Collaborative Filtering Recommendations...")
df_marts = con.execute("""
    SELECT 
        c.customer_unique_id, 
        m.product_category, 
        COUNT(m.order_id) as purchase_count 
    FROM main.marts m
    JOIN read_csv_auto('data/raw/olist_orders_dataset.csv') o ON m.order_id = o.order_id
    JOIN read_csv_auto('data/raw/olist_customers_dataset.csv') c ON o.customer_id = c.customer_id
    WHERE m.product_category IS NOT NULL
    GROUP BY ALL
""").df()
print(f"   ↳ Loaded {len(df_marts):,} transactional pairs from marts layer.")

pivot_matrix = df_marts.pivot_table(index='customer_unique_id', columns='product_category', values='purchase_count', fill_value=0)
print(f"   ↳ Interaction Matrix Shape: {pivot_matrix.shape[0]:,} Customers x {pivot_matrix.shape[1]:,} Product Categories.")

n_features = min(10, pivot_matrix.shape[1]-1)
print(f"   ↳ Decomposing matrix into {n_features} latent features using TruncatedSVD...")
svd = TruncatedSVD(n_components=n_features, random_state=42)
latent_matrix = svd.fit_transform(pivot_matrix)
predicted_ratings = np.dot(latent_matrix, svd.components_)
df_preds = pd.DataFrame(predicted_ratings, index=pivot_matrix.index, columns=pivot_matrix.columns)

recs = {}
for cust_id in df_preds.index:
    top_cats = df_preds.loc[cust_id].nlargest(3).index.tolist()
    recs[cust_id] = ", ".join(top_cats)

df_recs = pd.DataFrame(list(recs.items()), columns=['customer_unique_id', 'ai_recommendations'])

print("   ⭐ [INSIGHT] Previewing Top 5 Generated System Recommendations:")
for idx, row in df_recs.head(5).iterrows():
    print(f"     ▪️ Cust ID: {row['customer_unique_id'][:10]}... ➔ Recs: {row['ai_recommendations']}")

# 📊 VISUALIZATION 2: Top AI Recommended Categories
print("   ↳ Plotting distribution of AI product recommendations...")
all_recs_series = df_recs['ai_recommendations'].str.split(', ').explode()
top_recs_counts = all_recs_series.value_counts().head(10)

plt.figure(figsize=(10, 5))
sns.barplot(x=top_recs_counts.values, y=top_recs_counts.index, palette="viridis", hue=top_recs_counts.index, legend=False)
plt.title("Top 10 Most Recommended Product Categories by AI Engine")
plt.xlabel("Recommendation Count Across All Customers")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig(f"{output_dir}/module2_recommendations_distribution.png", dpi=300)
plt.close()
print(f"   📸 [SAVED] Plot exported to '{output_dir}/module2_recommendations_distribution.png'")

print("   ↳ Exporting recommendation matrix to 'recommendations_data.csv'...")
df_recs.to_csv("recommendations_data.csv", index=False)
print("✅ [MODULE 2] Finished Product Recommendation Pipeline.\n")

print("-" * 50)

# =========================================================================
# MODULE 3: NLP SENTIMENT ANALYSIS 
# =========================================================================
print("💬 [MODULE 3] Running NLP Sentiment Rule-Based Analysis...")
df_marts_raw = con.execute("""
    SELECT 
        m.*, 
        COALESCE(r.review_score, 5) as review_score
    FROM main.marts m
    LEFT JOIN read_csv_auto('data/raw/olist_order_reviews_dataset.csv') r 
        ON m.order_id = r.order_id
""").df()
print(f"   ↳ Processing sentiment states for {len(df_marts_raw):,} e-commerce transactions.")

conds = [
    (df_marts_raw['review_score'] >= 4),
    (df_marts_raw['review_score'] == 3),
    (df_marts_raw['review_score'] <= 2)
]
choices = ['Positive', 'Neutral', 'Negative']
df_marts_raw['review_sentiment'] = np.select(conds, choices, default='Positive')

sentiment_counts = df_marts_raw['review_sentiment'].value_counts()
print("   ⭐ [INSIGHT] Customer Sentiment Structural Distribution:")
for sentiment, count in sentiment_counts.items():
    print(f"     ▪️ {sentiment}: {count:,} records ({count/len(df_marts_raw):.1%})")

# 📊 VISUALIZATION 3: Sentiment Distribution Pie Chart
print("   ↳ Generating Sentiment Breakdown visual...")
plt.figure(figsize=(6, 6))
colors = ['#5eead4', '#f87171', '#64748b'] # Màu đồng bộ với Dashboard của bạn
plt.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%', 
        startangle=140, colors=colors, explode=(0.05, 0.05, 0.05),
        textprops={'fontsize': 11, 'fontweight': 'bold'})
plt.title("NLP Order Review Sentiment Analysis Breakdown", fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig(f"{output_dir}/module3_sentiment_analysis.png", dpi=300)
plt.close()
print(f"   📸 [SAVED] Plot exported to '{output_dir}/module3_sentiment_analysis.png'")

print("   ↳ Overwriting analytical marts to 'marts_data.csv'...")
df_marts_raw.to_csv("marts_data.csv", index=False)
print("✅ [MODULE 3] Finished NLP Sentiment Pipeline.\n")

con.close()

print("="*70)
print("🎉 ALL AI DEPLOYMENT MODELS TRAINED, EXPORTED & VISUALIZED SUCCESSFULLY!")
print("="*70)