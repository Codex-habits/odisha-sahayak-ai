import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Reproducible prototype dataset
np.random.seed(42)

N = 1000

rainfall = np.random.uniform(0, 400, N)
humidity = np.random.uniform(30, 100, N)
water_level = np.random.uniform(0, 10, N)

# Create a synthetic training target for the prototype.
# Higher rainfall, humidity and water level generally increase risk.
risk_score = (
    0.45 * (rainfall / 400)
    + 0.20 * (humidity / 100)
    + 0.35 * (water_level / 10)
)

# Add noise so the model does not become unrealistically certain.
risk_score += np.random.normal(0, 0.08, N)

flood = (risk_score > 0.62).astype(int)

data = pd.DataFrame({
    "rainfall": rainfall,
    "humidity": humidity,
    "water_level": water_level,
    "flood": flood
})

X = data[["rainfall", "humidity", "water_level"]]
y = data["flood"]

model = RandomForestClassifier(
    n_estimators=200,
    max_depth=8,
    min_samples_leaf=5,
    random_state=42
)

model.fit(X, y)

with open("flood_risk_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("Improved flood risk model trained successfully!")
