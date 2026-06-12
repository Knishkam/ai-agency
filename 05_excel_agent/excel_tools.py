import pandas as pd
import os 
from pathlib import Path
import json
from typing import Optional
def read_excel(file_path) -> Optional[pd.DataFrame]:
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
        return df
    except Exception as e:
        return None
def get_summary(df: pd.DataFrame) -> dict:
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "sample": df.head(3).to_dict()
    }
def filter_data(df: pd.DataFrame, column: str, value: str) -> pd.DataFrame:
    try:
        filtered = df[df[column].astype(str).str.contains(value, case=False)]
        return filtered
    except:
        return df
def get_column_stats(df: pd.DataFrame, column: str) -> dict:
    try:
        if df[column].dtype in ['int64', 'float64']:
            return {
                "column": column,
                "mean": float(df[column].mean()),
                "max": float(df[column].max()),
                "min": float(df[column].min()),
                "sum": float(df[column].sum()),
                "count": int(df[column].count())
            }
        else:
            return {
                "column": column,
                "unique_values": df[column].nunique(),
                "most_common": df[column].value_counts().head(5).to_dict()
            }
    except:
        return {"error": f"column {column} not found"}
def search_data(df: pd.DataFrame, query: str) -> pd.DataFrame:
    try:
        mask = df.astype(str).apply(
            lambda x: x.str.contains(query, case=False)).any(axis=1)
        return df[mask]
    except:
        return pd.DataFrame()
def to_json_str(df: pd.DataFrame) -> str:
    try:
        return df.to_json(orient='records', indent=2)
    except:
        return "{}"