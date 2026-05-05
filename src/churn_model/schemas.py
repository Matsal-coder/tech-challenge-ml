from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    features: dict = Field(
        ...,
        description="Raw customer features expected by the preprocessing pipeline.",
    )


class PredictionResponse(BaseModel):
    churn_probability: float = Field(..., ge=0.0, le=1.0)
    prediction: int = Field(..., ge=0, le=1)
    threshold: float = Field(..., ge=0.0, le=1.0)