from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import torch
import torch.nn as nn
import re
import string
import os
from sklearn.feature_extraction.text import TfidfVectorizer

app = Flask(__name__)

# Allow only Vercel frontend access
CORS(app, resources={r"/*": {"origins": "https://fake-news-detection-b45jkom9y-aams-projects-1297b49c.vercel.app"}})

# 🔹 Verify files exist before loading
required_files = {
    "vectorizer": "vectorizer.pkl",
    "logistic_regression": "Logistic_Regression.pkl",
    "naive_bayes": "Naive_Bayes.pkl",
    "random_forest": "Random_Forest.pkl",
    "gradient_boosting": "Gradient_Boosting.pkl",
    "pytorch_model": "fake_news_model.pth"
}

for key, file in required_files.items():
    if not os.path.exists(file):
        raise FileNotFoundError(f"❌ Error: Required file '{file}' not found!")

# 🔹 Load Scikit-learn models
vectorizer = joblib.load(required_files["vectorizer"])
models = {
    "Logistic Regression": joblib.load(required_files["logistic_regression"]),
    "Naive Bayes": joblib.load(required_files["naive_bayes"]),
    "Random Forest": joblib.load(required_files["random_forest"]),
    "Gradient Boosting": joblib.load(required_files["gradient_boosting"])
}

# 🔹 Load PyTorch Model
class FakeNewsClassifier(nn.Module):
    def __init__(self, input_dim):
        super(FakeNewsClassifier, self).__init__()
        self.fc = nn.Linear(input_dim, 2)

    def forward(self, x):
        return self.fc(x)

input_dim = vectorizer.max_features
pytorch_model = FakeNewsClassifier(input_dim)

# Ensure the model is loaded for CPU (avoids GPU errors)
pytorch_model.load_state_dict(torch.load(required_files["pytorch_model"], map_location=torch.device("cpu")))
pytorch_model.eval()

# 🔹 Preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)  # Remove punctuation
    return text

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # Preprocess & vectorize text
    processed_text = preprocess_text(text)
    input_vec = vectorizer.transform([processed_text])

    # Predictions from Scikit-learn models
    predictions = {name: int(model.predict(input_vec)[0]) for name, model in models.items()}

    # # 🔹 PyTorch Prediction
    # input_tensor = torch.tensor(input_vec.toarray(), dtype=torch.float32)
    # output = pytorch_model(input_tensor)
    # pytorch_pred = torch.argmax(output, dim=1).item()
    # predictions["PyTorch Model"] = pytorch_pred

    # 🔹 Convert predictions to Real/Fake
    response = {name: "Real" if pred == 1 else "Fake" for name, pred in predictions.items()}
    
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
