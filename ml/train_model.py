import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

DATA_DIR = "collected_data"
MODEL_DIR = "models"

os.makedirs(MODEL_DIR, exist_ok=True)

X = []
y = []

# Load all CSV files
for file in os.listdir(DATA_DIR):
    if file.endswith(".csv"):
        label = file.replace(".csv", "")
        df = pd.read_csv(os.path.join(DATA_DIR, file))
        X.append(df.values)
        y += [label] * len(df)

X = np.vstack(X)
y = np.array(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Train model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    random_state=42
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n🎯 Model Accuracy: {accuracy * 100:.2f}%")

# Save model
joblib.dump(model, os.path.join(MODEL_DIR, "sign_model.pkl"))
print("✅ Model saved as sign_model.pkl")
