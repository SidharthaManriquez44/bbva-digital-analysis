import pytest
from src.extract.bbva_manual_loader import extract_bbva_data


def test_extract_bbva_columns():
    df = extract_bbva_data()

    expected_columns = [
        "bank_code", "year", "branches", "atms",
        "total_clients", "digital_clients",
        "total_loans", "total_deposits", "net_income",
        "source_file_name"
    ]

    assert list(df.columns) == expected_columns

def test_extract_bbva_types():
    df = extract_bbva_data()

    assert df["year"].dtype == "object"
    assert df["branches"].dtype == "object"
    assert df["atms"].dtype == "object"
    assert df["total_loans"].dtype == "object"