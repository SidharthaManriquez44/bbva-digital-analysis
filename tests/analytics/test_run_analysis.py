from unittest.mock import patch, MagicMock
from src.load.mart_loader import MartLoader


@patch("src.load.mart_loader.get_engine")
def test_load_bank_financial_year(mock_get_engine):
    pass