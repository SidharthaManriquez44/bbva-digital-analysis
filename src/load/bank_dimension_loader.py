from sqlalchemy import text
from src.config.db_config import get_engine


def load_dim_bank_from_staging():
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO core.dim_bank (
                bank_code,
                bank_name,
                country
            )
            SELECT DISTINCT
                bank_code,
                CASE 
                    WHEN bank_code = 'BBVA' THEN 'BBVA México'
                    ELSE bank_code
                END AS bank_name,
                'México' AS country
            FROM staging.bank_year_metrics_clean
            ON CONFLICT (bank_code)
            DO NOTHING;
        """))