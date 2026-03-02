from sqlalchemy import text
import pytest
from src.config.db_config import get_engine


def test_postgresql_connection():
    engine = get_engine()

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            value = result.scalar()

            assert value == 1

    except Exception as e:
        pytest.fail(f"The connection to the database failed: {e}")


