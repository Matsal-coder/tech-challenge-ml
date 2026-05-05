import logging
import time

from fastapi import FastAPI, HTTPException, Request
from pandera.errors import SchemaError, SchemaErrors

from churn_model.logging_config import configure_logging
from churn_model.predict import predict_churn
from churn_model.schemas import PredictionRequest, PredictionResponse

configure_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Churn Prediction API",
    description="API for customer churn prediction using a PyTorch MLP model.",
    version="0.1.0",
)


@app.middleware("http")
async def log_request_latency(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    latency_ms = (time.perf_counter() - start_time) * 1000

    logger.info(
        "request_completed method=%s path=%s status_code=%s latency_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        latency_ms,
    )

    response.headers["X-Latency-ms"] = f"{latency_ms:.2f}"

    return response


@app.get("/health")
def health_check() -> dict:
    logger.info("health_check_requested")
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> dict:
    logger.info("prediction_requested")

    try:
        result = predict_churn(request.features)

    except (SchemaError, SchemaErrors) as error:
        logger.warning("prediction_validation_error error=%s", str(error))
        raise HTTPException(
            status_code=400,
            detail="Invalid input data for prediction.",
        ) from error

    except Exception as error:
        logger.exception("prediction_internal_error")
        raise HTTPException(
            status_code=500,
            detail="Internal prediction error.",
        ) from error

    logger.info(
        "prediction_completed prediction=%s probability=%.4f",
        result["prediction"],
        result["churn_probability"],
    )

    return result