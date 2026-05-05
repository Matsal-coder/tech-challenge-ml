from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODELS_DIR = PROJECT_ROOT / "models"

MODEL_PATH = MODELS_DIR / "mlp_churn_model.pt"
PREPROCESSOR_PATH = MODELS_DIR / "preprocessor.pkl"
METADATA_PATH = MODELS_DIR / "model_metadata.json"

RANDOM_STATE = 555
DEFAULT_THRESHOLD = 0.5