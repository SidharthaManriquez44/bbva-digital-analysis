import pytest
import pandas as pd
from src.extract.bbva_manual_loader import extract_bbva_data

# -------------------------------------------------
# BASIC STRUCTURAL VALIDATIONS
# -------------------------------------------------
def test_extract_bbva_columns():
    df = extract_bbva_data()

    expected_columns = [
        "bank_code", "year", "branches", "atms",
        "total_clients", "digital_clients",
        "total_loans", "total_deposits", "net_income",
        "source_file_name"
    ]

    assert list(df.columns) == expected_columns

def test_extract_bbva_row_count():
    df = extract_bbva_data()
    assert len(df) == 6

# -------------------------------------------------
# DATA QUALITY VALIDATIONS
# -------------------------------------------------

def test_no_nulls_in_critical_columns():
    df = extract_bbva_data()

    critical_columns = [
        "bank_code",
        "year",
        "total_clients",
        "net_income"
    ]

    for col in critical_columns:
        assert df[col].isna().sum() == 0


def test_unique_year_per_bank():
    df = extract_bbva_data()

    duplicated = df.duplicated(subset=["bank_code", "year"])
    assert duplicated.sum() == 0


def test_extract_bbva_types():
    df = extract_bbva_data()
    object_columns = [
        "year",
        "branches",
        "atms",
        "total_clients",
        "digital_clients",
        "total_loans",
        "total_deposits",
        "net_income"
    ]
    for col in object_columns:
        assert pd.api.types.is_object_dtype(df[col]), f"{col} is not numeric"
