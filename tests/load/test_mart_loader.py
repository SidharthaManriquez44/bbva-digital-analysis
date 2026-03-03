from unittest.mock import patch, MagicMock
from src.load.mart_loader import MartLoader


@patch("src.load.mart_loader.get_engine")
def test_load_bank_financial_year(mock_get_engine):

    # Mock engine y connection
    fake_engine = MagicMock()
    fake_conn = MagicMock()

    mock_get_engine.return_value = fake_engine
    fake_engine.begin.return_value.__enter__.return_value = fake_conn

    # Run function
    loader =  MartLoader()
    loader.load_bank_financial_year()

    # Validations
    assert mock_get_engine.called
    assert fake_engine.begin.called
    assert fake_conn.execute.called

@patch("src.load.mart_loader.get_engine")
def test_load_bank_digital_year(mock_get_engine):

    # Mock engine y connection
    fake_engine = MagicMock()
    fake_conn = MagicMock()

    mock_get_engine.return_value = fake_engine
    fake_engine.begin.return_value.__enter__.return_value = fake_conn

    # Run function
    loader =  MartLoader()
    loader.load_bank_digital_year()

    # Validations
    assert mock_get_engine.called
    assert fake_engine.begin.called
    assert fake_conn.execute.called

@patch("src.load.mart_loader.get_engine")
def test_load_bank_efficiency_year(mock_get_engine):

    # Mock engine y connection
    fake_engine = MagicMock()
    fake_conn = MagicMock()

    mock_get_engine.return_value = fake_engine
    fake_engine.begin.return_value.__enter__.return_value = fake_conn

    # Run function
    loader =  MartLoader()
    loader.load_bank_efficiency_year()

    # Validations
    assert mock_get_engine.called
    assert fake_engine.begin.called
    assert fake_conn.execute.called

@patch("src.load.mart_loader.get_engine")
def test_load_bank_growth_year(mock_get_engine):

    # Mock engine y connection
    fake_engine = MagicMock()
    fake_conn = MagicMock()

    mock_get_engine.return_value = fake_engine
    fake_engine.begin.return_value.__enter__.return_value = fake_conn

    # Run function
    loader =  MartLoader()
    loader.load_bank_growth_year()

    # Validations
    assert mock_get_engine.called
    assert fake_engine.begin.called
    assert fake_conn.execute.called