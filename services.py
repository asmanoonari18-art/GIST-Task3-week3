import json
import math
from io import BytesIO
import pandas as pd

ALLOWED_EXTENSIONS = {".csv"}

def validate_csv(filename: str):
    if not filename:
        raise ValueError("A filename is required.")
    if not filename.lower().endswith(".csv"):
        raise ValueError("Only CSV files are supported.")

def analyze_csv(content: bytes) -> dict:
    try:
        df = pd.read_csv(BytesIO(content))
    except Exception as exc:
        raise ValueError(f"Could not read CSV: {exc}") from exc

    if df.empty:
        raise ValueError("The CSV file contains no rows.")

    missing_by_column = df.isna().sum().to_dict()
    dtypes = {col: str(dtype) for col, dtype in df.dtypes.items()}

    numeric_summary = {}
    numeric = df.select_dtypes(include="number")
    if not numeric.empty:
        desc = numeric.describe().round(3).replace({math.nan: None})
        numeric_summary = json.loads(desc.to_json())

    profile = {
        "shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "columns": list(df.columns),
        "dtypes": dtypes,
        "missing_by_column": {str(k): int(v) for k, v in missing_by_column.items()},
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_summary": numeric_summary,
    }
    return profile

def clean_csv(content: bytes) -> tuple[bytes, dict]:
    try:
        df = pd.read_csv(BytesIO(content))
    except Exception as exc:
        raise ValueError(f"Could not read CSV: {exc}") from exc

    before = len(df)
    df = df.drop_duplicates()
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
        else:
            mode = df[col].mode()
            if not mode.empty:
                df[col] = df[col].fillna(mode.iloc[0])

    output = df.to_csv(index=False).encode("utf-8")
    report = {
        "rows_before": before,
        "rows_after": len(df),
        "duplicates_removed": before - len(df),
        "missing_values_after": int(df.isna().sum().sum()),
    }
    return output, report
