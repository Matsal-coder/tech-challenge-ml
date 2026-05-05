from pydantic import ValidationError

from churn_model.schemas import PredictionRequest, PredictionResponse


def test_prediction_request_schema_accepts_features_dict():
    request = PredictionRequest(features={"Gender": "Male", "Monthly Charges": 70.0})

    assert request.features["Gender"] == "Male"


def test_prediction_response_schema_accepts_valid_prediction():
    response = PredictionResponse(
        churn_probability=0.73,
        prediction=1,
        threshold=0.5,
    )

    assert response.prediction == 1


def test_prediction_response_rejects_invalid_probability():
    try:
        PredictionResponse(
            churn_probability=1.5,
            prediction=1,
            threshold=0.5,
        )
    except ValidationError:
        assert True
    else:
        assert False