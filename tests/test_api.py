import json
from pathlib import Path

from fastapi.testclient import TestClient

from churn_model.api import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "X-Latency-ms" in response.headers


def test_predict_endpoint():
    payload_path = Path("examples/sample_prediction_payload.json")

    with open(payload_path, encoding="utf-8") as file:
        payload = json.load(file)

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "churn_probability" in data
    assert "prediction" in data
    assert "threshold" in data
    assert 0 <= data["churn_probability"] <= 1
    assert data["prediction"] in [0, 1]
    assert "X-Latency-ms" in response.headers

def test_predict_rejects_invalid_payload():
    response = client.post("/predict", json={"wrong_key": {}})

    assert response.status_code == 422

def test_predict_rejects_extra_feature():
    payload = {
        "features": {
            "unexpected_column": "invalid",
        }
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid input data for prediction."