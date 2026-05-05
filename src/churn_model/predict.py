import json

import joblib
import pandas as pd
import torch

from churn_model.config import METADATA_PATH, MODEL_PATH, PREPROCESSOR_PATH
from churn_model.model import ChurnMLP


def load_metadata() -> dict:
    with open(METADATA_PATH, encoding="utf-8") as file:
        return json.load(file)


def load_preprocessor():
    return joblib.load(PREPROCESSOR_PATH)


def load_model(input_dim: int) -> ChurnMLP:
    model = ChurnMLP(input_dim=input_dim)
    state_dict = torch.load(MODEL_PATH, map_location="cpu")
    model.load_state_dict(state_dict)
    model.eval()
    return model


def predict_churn(input_data: dict) -> dict:
    metadata = load_metadata()
    preprocessor = load_preprocessor()

    df = pd.DataFrame([input_data])

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
    }