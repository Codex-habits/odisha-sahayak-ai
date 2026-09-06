import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Prototype training data
data = {
    "rainfall": [20, 40, 60, 80, 100, 120, 150, 180, 220, 300],
    "humidity": [50, 55, 60, 65, 70, 75, 80, 82, 88, 92],
    "water_level": [1, 1, 2, 2, 3, 3, 4, 4, 5, 6],
    "flood": [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

X = df[["rainfall", "humidity", "water_level"]]
y = df["flood"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

with open("flood_risk_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Model trained successfully!")
