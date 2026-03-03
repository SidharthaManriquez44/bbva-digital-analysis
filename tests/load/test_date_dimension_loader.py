from unittest.mock import patch, MagicMock
from src.load.date_dimension_loader import load_dim_date_from_staging


@patch("src.load.date_dimension_loader.get_engine")
def test_load_dim_date_from_staging(mock_get_engine):

    # Mock engine y connection
    fake_engine = MagicMock()
    fake_conn = MagicMock()

    mock_get_engine.return_value = fake_engine
    fake_engine.begin.return_value.__enter__.return_value = fake_conn

    # Run function
    load_dim_date_from_staging()

    # Validations
    assert mock_get_engine.called
    assert fake_engine.begin.called
    assert fake_conn.execute.called