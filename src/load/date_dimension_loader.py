from sqlalchemy import text
from src.config.db_config import get_engine


def load_dim_date_from_staging():
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO core.dim_date (
                date_key,
                date,
                year,
                quarter,
                month,
                is_year_end
            )
            SELECT DISTINCT
                (year * 10000) + 1231 AS date_key,
                MAKE_DATE(year, 12, 31) AS date,
                year,
                4 AS quarter,
                12 AS month,
                TRUE AS is_year_end
            FROM staging.bank_year_metrics_clean
            ON CONFLICT (date_key)
            DO NOTHING;
        """))