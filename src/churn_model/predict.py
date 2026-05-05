import json
from functools import lru_cache

import joblib
import pandas as pd
import torch

from churn_model.config import METADATA_PATH, MODEL_PATH, MODEL_VERSION, PREPROCESSOR_PATH
from churn_model.model import ChurnMLP
from churn_model.data_schema import validate_prediction_input

def load_metadata() -> dict:
    with open(METADATA_PATH, encoding="utf-8") as file:
        return json.load(file)


@lru_cache
def load_preprocessor():
    return joblib.load(PREPROCESSOR_PATH)


@lru_cache
def load_model(input_dim: int) -> ChurnMLP:
    model = ChurnMLP(input_dim=input_dim, version=MODEL_VERSION)
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model

def create_features(df):
    df = df.copy()

    tenure_safe = df["Tenure Months"].replace(0, 1)

    df["avg_charge_per_tenure"] = df["Total Charges"] / tenure_safe
    df["is_month_to_month"] = (df["Contract"] == "Month-to-month").astype(int)
    df["has_fiber"] = (df["Internet Service"] == "Fiber optic").astype(int)
    df["has_tech_support"] = (df["Tech Support"] == "Yes").astype(int)
    df["has_online_security"] = (df["Online Security"] == "Yes").astype(int)
    df["is_new_customer"] = (df["Tenure Months"] <= 6).astype(int)
    df["is_long_term_customer"] = (df["Tenure Months"] >= 24).astype(int)

    service_cols = [
        "Phone Service",
        "Multiple Lines",
        "Online Security",
        "Online Backup",
        "Device Protection",
        "Tech Support",
        "Streaming TV",
        "Streaming Movies",
    ]

    df["num_services"] = (
        df[service_cols]
        .apply(lambda col: col.astype(str).str.contains("Yes").astype(int))
        .sum(axis=1)
    )

    df["charge_per_service"] = df["Monthly Charges"] / df["num_services"].replace(0, 1)

    return df


def predict_churn(input_data: dict) -> dict:
    metadata = load_metadata()
    preprocessor = load_preprocessor()

    df = pd.DataFrame([input_data])

    if MODEL_VERSION == "v2":
        df = create_features(df)

    df = validate_prediction_input(df)

    X_processed = preprocessor.transform(df)
    input_dim = X_processed.shape[1]

    model = load_model(input_dim=input_dim)

    X_tensor = torch.tensor(X_processed, dtype=torch.float32)

    with torch.no_grad():
        logits = model(X_tensor)
        probability = torch.sigmoid(logits).item()

    threshold = metadata.get("threshold", 0.5)
    prediction = int(probability >= threshold)

    return {
        "churn_probability": probability,
        "prediction": prediction,
        "threshold": threshold,
        "model_version": MODEL_VERSION,
    }

