import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report



# 1. Load dataset

DATA_PATH = "data/raw/complaints.csv"
MODEL_PATH = "models/category_model.pkl"

df = pd.read_csv(DATA_PATH)

print("Dataset loaded successfully!")
print(f"Total records: {len(df)}")


# 2. Split data

X = df["complaint"]
y = df["category"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


# 3. Create ML pipeline


model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# 4. Train

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training completed!")


# 5. Evaluate

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"Accuracy: {accuracy:.2%}")

print("\nClassification Report:")
print(classification_report(y_test, predictions))


# 6. Save model

Path("models").mkdir(exist_ok=True)

joblib.dump(model, MODEL_PATH)

print("\nModel saved successfully!")
print(f"Location: {MODEL_PATH}")


# 7. Test sample complaints

test_complaints = [
    "There has been no water in our area for three days",
    "The street lights are not working near my house",
    "There is a huge pothole on the main road",
    "Garbage has not been collected for a week",
    "The government hospital has no medicines"
]

print("\n==============================")
print("SAMPLE PREDICTIONS")
print("==============================")

for complaint in test_complaints:

    prediction = model.predict([complaint])[0]

    probabilities = model.predict_proba([complaint])[0]

    confidence = max(probabilities)

    print("\nComplaint:")
    print(complaint)

    print(f"Category: {prediction}")
    print(f"Confidence: {confidence:.2%}")