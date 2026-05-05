import json
from pathlib import Path

import pandas as pd
import pytest
from pandera.errors import SchemaError, SchemaErrors

from churn_model.data_schema import get_expected_columns, validate_prediction_input


def test_get_expected_columns_returns_list():
    columns = get_expected_columns()

    assert isinstance(columns, list)
    assert len(columns) > 0


def test_validate_prediction_input_accepts_sample_payload():
    payload_path = Path("examples/sample_prediction_payload.json")

    with open(payload_path, encoding="utf-8") as file:
        payload = json.load(file)

    df = pd.DataFrame([payload["features"]])

    validated_df = validate_prediction_input(df)

    assert list(validated_df.columns) == get_expected_columns()


def test_validate_prediction_input_rejects_extra_column():
    payload_path = Path("examples/sample_prediction_payload.json")

    with open(payload_path, encoding="utf-8") as file:
        payload = json.load(file)

    features = payload["features"]
    features["unexpected_column"] = "invalid"

    df = pd.DataFrame([features])

    with pytest.raises((SchemaError, SchemaErrors)):
        validate_prediction_input(df)