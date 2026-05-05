import json

import pandas as pd
import pandera.pandas as pa
from pandera.typing import DataFrame

from churn_model.config import METADATA_PATH


def get_expected_columns() -> list[str]:
    with open(METADATA_PATH, encoding="utf-8") as file:
        metadata = json.load(file)

    return metadata["features"]


def validate_prediction_input(df: pd.DataFrame) -> DataFrame:
    expected_columns = get_expected_columns()

    schema = pa.DataFrameSchema(
        {
            column: pa.Column(nullable=True, required=True)
            for column in expected_columns
        },
        strict=True,
    )

    return schema.validate(df)