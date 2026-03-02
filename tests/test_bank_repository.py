import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src.data_access.bank_repository import BankRepository


@patch("src.data_access.bank_repository.get_engine")
def test_get_bank_kpis(mock_get_engine):

    # Fake dataframe
    fake_df = pd.DataFrame({
        "year": [2020, 2021],
        "digital_penetration_pct": [72.5, 75.0],
        "profit_per_branch": [120000, 150000]
    })

    # Mock connection + pd.read_sql
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine

    with patch("pandas.read_sql", return_value=fake_df):

        repo = BankRepository()
        result = repo.get_bank_kpis("BBVA")

        assert isinstance(result, pd.DataFrame)
        assert not result.empty
        assert list(result.columns) == [
            "year",
            "digital_penetration_pct",
            "profit_per_branch"
        ]
        assert result.shape[0] == 2

@patch("src.data_access.bank_repository.get_engine")
def test_get_structural_model_data(mock_get_engine):

    fake_df = pd.DataFrame({
        "year": [2020],
        "digital_penetration_pct": [72.0],
        "branches": [1800],
        "atms": [12000],
        "total_clients": [55000000],
        "digital_clients": [40000000],
        "total_loans": [1500000000000],
        "total_deposits": [1550000000000],
        "net_income": [120000000000],
        "profit_per_branch": [66666]
    })

    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine

    with patch("pandas.read_sql", return_value=fake_df):

        repo = BankRepository()
        result = repo.get_structural_model_data("BBVA")

        assert "branches" in result.columns
        assert result["branches"].iloc[0] == 1800
        assert result.shape[0] == 1