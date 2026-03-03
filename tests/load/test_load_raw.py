from unittest.mock import patch, MagicMock
from src.load.raw_loader import load_raw
from tests.config.conftest import fake_data


@patch("src.load.raw_loader.get_engine")
@patch("pandas.DataFrame.to_sql")
def test_load_raw_append(mock_to_sql, mock_get_engine, fake_data):

    fake_engine = MagicMock()
    mock_get_engine.return_value = fake_engine

    load_raw(fake_data)

    # Create engine
    mock_get_engine.assert_called_once()

    # Call SQL once
    mock_to_sql.assert_called_once()

    # Validate critical args
    args, kwargs = mock_to_sql.call_args

    assert kwargs["con"] == fake_engine
    assert kwargs["if_exists"] == "append"
    assert kwargs["index"] is False