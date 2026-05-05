from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = PROJECT_ROOT / "models"

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1")

if MODEL_VERSION == "v2":
    MODEL_PATH = MODELS_DIR / "mlp_churn_model_v2.pt"
    PREPROCESSOR_PATH = MODELS_DIR / "preprocessor_v2.pkl"
    METADATA_PATH = MODELS_DIR / "model_metadata_v2.json"
else:
    MODEL_PATH = MODELS_DIR / "mlp_churn_model.pt"
    PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"
    METADATA_PATH = MODELS_DIR / "model_metadata.json"