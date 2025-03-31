# Importing necessary libraries
import pandas as pd
import numpy as np
import re
import string
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

# Load datasets
fake_path = 'data/Fake.csv'
true_path = 'data/True.csv'

# Step 1: Load Dataset
data_fake = pd.read_csv(fake_path)
data_true = pd.read_csv(true_path)

# Step 2: Labeling the data
data_fake["class"] = 0  # Fake news
data_true["class"] = 1  # Real news

# Dropping unnecessary rows (last 10 rows for manual testing)
data_fake_manual_testing = data_fake.tail(10)
data_true_manual_testing = data_true.tail(10)
data_fake.drop(data_fake.index[-10:], inplace=True)
data_true.drop(data_true.index[-10:], inplace=True)

# Merge and shuffle the datasets
data_merge = pd.concat([data_fake, data_true], axis=0)
data_merge = data_merge.sample(frac=1).reset_index(drop=True)

# Dropping irrelevant columns
data = data_merge.drop(['title', 'subject', 'date'], axis=1)

# Check for missing values
print("Missing values per column:\n", data.isnull().sum())

# Step 3: Preprocessing the text
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r"https?://\S+|www\.\S+", '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

data['text'] = data['text'].apply(preprocess_text)

# Splitting the data into training and test sets
X = data['text']
y = data['class']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Step 4: Text vectorization using TF-IDF
vectorizer = TfidfVectorizer(stop_words=stopwords.words('english'), max_df=0.95, min_df=2)
X_train_vect = vectorizer.fit_transform(X_train)
X_test_vect = vectorizer.transform(X_test)

# Step 5: Model definitions
models = {
    "Logistic Regression": LogisticRegression(),
    "Naive Bayes": MultinomialNB(),
    "Random Forest": RandomForestClassifier(random_state=42),
    "Gradient Boosting": GradientBoostingClassifier(random_state=42)
}

# Initialize a dataframe to store metrics
metrics_df = pd.DataFrame(columns=['Model', 'Accuracy', 'Precision (Class 0)', 'Recall (Class 0)', 'F1-Score (Class 0)',
                                   'Precision (Class 1)', 'Recall (Class 1)', 'F1-Score (Class 1)'])

# Train, predict and evaluate models
for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train_vect, y_train)
    y_pred = model.predict(X_test_vect)

    acc = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, output_dict=True)

    new_row = pd.DataFrame([{
        'Model': name,
        'Accuracy': acc,
        'Precision (Class 0)': report['0']['precision'],
        'Recall (Class 0)': report['0']['recall'],
        'F1-Score (Class 0)': report['0']['f1-score'],
        'Precision (Class 1)': report.get('1', {}).get('precision', np.nan),
        'Recall (Class 1)': report.get('1', {}).get('recall', np.nan),
        'F1-Score (Class 1)': report.get('1', {}).get('f1-score', np.nan)
    }])

    metrics_df = pd.concat([metrics_df, new_row], ignore_index=True)

# Display the metrics in a tabular format
print("\nModel Performance Summary:")
print(metrics_df)

# Plotting the accuracy comparison with three decimal places
plt.figure(figsize=(10, 6))
barplot = sns.barplot(x='Accuracy', y='Model', data=metrics_df, palette='viridis')
plt.title('Model Accuracy Comparison')
plt.xlabel('Accuracy')
plt.ylabel('Model')
plt.xlim(0.95, 1.0)

# Adding accuracy values to the bars
for p in barplot.patches:
    barplot.annotate(format(p.get_width(), '.3f'), 
                     (p.get_width(), p.get_y() + p.get_height() / 2), 
                     ha='left', va='center', 
                     xytext=(5, 0), 
                     textcoords='offset points')

plt.show()

# Manual Testing Function with enhancements
def output_label(prediction):
    return "Fake News" if prediction == 0 else "Real News"

def manual_testing(news_text):
    processed_text = preprocess_text(news_text)
    vectorized_text = vectorizer.transform([processed_text])

    results = []
    print("\n--- Manual Testing Results ---")
    for model_name, model in models.items():
        prediction = model.predict(vectorized_text)[0]
        confidence = model.predict_proba(vectorized_text).max()  # Confidence score
        result = output_label(prediction)
        results.append(f"{model_name}: {result} (Confidence: {confidence:.2f})")
        print(f"{model_name}: {result} (Confidence: {confidence:.2f})")
    print("------------------------------")

    # Save results to a file
    with open("manual_test_results.txt", "a") as file:
        file.write(f"News: {news_text}\n")
        file.write("\n".join(results))
        file.write("\n" + "-"*30 + "\n")
    print("Results saved to manual_test_results.txt")

# Interactive session for continuous testing
if __name__ == "__main__":
    print("\nFake News Detection System (Type 'exit' to quit)")
    while True:
        user_input = input("\nEnter the news text for evaluation: ")
        if user_input.lower() == 'exit':
            print("Exiting the Fake News Detection System. Goodbye!")
            break
        manual_testing(user_input)
