from unittest.mock import patch, MagicMock
from src.data_access.bank_repository import BankRepository


@patch("src.data_access.bank_repository.get_engine")
def test_query_contains_expected_fields(mock_get_engine):

    mock_conn = MagicMock()
    mock_engine = MagicMock()
    mock_engine.connect.return_value.__enter__.return_value = mock_conn
    mock_get_engine.return_value = mock_engine

    with patch("pandas.read_sql") as mock_read_sql:

        repo = BankRepository()
        repo.get_bank_kpis("BBVA")

        # We verified that SQL read was called
        assert mock_read_sql.called

        # We extract the query that was passed
        args, kwargs = mock_read_sql.call_args
        query = str(args[0])

        assert "digital_penetration_pct" in query
        assert "profit_per_branch" in query
        assert "ORDER BY year" in query