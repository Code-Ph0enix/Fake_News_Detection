import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Model performance data over 5 days
model_performance_data = [
    { 'name': 'Day 1', 'Logistic Regression': 94, 'Naive Bayes': 90, 'Random Forest': 98, 'Gradient Boosting': 95 },
    { 'name': 'Day 2', 'Logistic Regression': 95, 'Naive Bayes': 91, 'Random Forest': 99, 'Gradient Boosting': 96 },
    { 'name': 'Day 3', 'Logistic Regression': 96, 'Naive Bayes': 92, 'Random Forest': 99, 'Gradient Boosting': 97 },
    { 'name': 'Day 4', 'Logistic Regression': 97, 'Naive Bayes': 93, 'Random Forest': 100, 'Gradient Boosting': 98 },
    { 'name': 'Day 5', 'Logistic Regression': 99, 'Naive Bayes': 94, 'Random Forest': 100, 'Gradient Boosting': 99 },
]

# Model metrics comparison
model_metrics = [
    { 'name': 'Precision', 'Logistic Regression': 93, 'Naive Bayes': 92, 'Random Forest': 98, 'Gradient Boosting': 94 },
    { 'name': 'Recall', 'Logistic Regression': 94, 'Naive Bayes': 93, 'Random Forest': 98, 'Gradient Boosting': 95 },
    { 'name': 'F1 Score', 'Logistic Regression': 94, 'Naive Bayes': 92, 'Random Forest': 98, 'Gradient Boosting': 95 },
]

# Convert to DataFrame
df_performance = pd.DataFrame(model_performance_data)
df_metrics = pd.DataFrame(model_metrics)

# ---------------- Line Chart: Model Performance Over Time ---------------- #
plt.figure(figsize=(10, 6))
for model in ['Logistic Regression', 'Naive Bayes', 'Random Forest', 'Gradient Boosting']:
    plt.plot(df_performance['name'], df_performance[model], marker='o', label=model)

plt.title('Model Performance Over Time')
plt.xlabel('Days')
plt.ylabel('Accuracy (%)')
plt.ylim(88, 102)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()

# ---------------- Bar Chart: Model Metrics Comparison ---------------- #
# Melt data for seaborn
df_metrics_melted = df_metrics.melt(id_vars='name', var_name='Model', value_name='Score')

plt.figure(figsize=(10, 6))
sns.barplot(data=df_metrics_melted, x='name', y='Score', hue='Model')

plt.title('Model Metrics Comparison')
plt.xlabel('Metric')
plt.ylabel('Score (%)')
plt.ylim(85, 100)
plt.grid(True, linestyle='--', axis='y', alpha=0.7)
plt.legend(title='Model')
plt.tight_layout()
plt.show()
