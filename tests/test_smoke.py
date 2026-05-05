def test_package_import():
    import churn_model

    assert churn_model is not None


def test_model_import():
    from churn_model.model import ChurnMLP

    assert ChurnMLP is not None


def test_predict_import():
    from churn_model.predict import predict_churn

    assert predict_churn is not None

def test_schema_import():
    from churn_model.schemas import PredictionRequest, PredictionResponse

    assert PredictionRequest is not None
    assert PredictionResponse is not None