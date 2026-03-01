from sqlalchemy import text
from src.config.db_config import get_engine


def load_staging():
    engine = get_engine()

    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO staging.bank_year_metrics_clean (
                raw_id,
                bank_code,
                year,
                branches,
                atms,
                total_clients,
                digital_clients,
                total_loans,
                total_deposits,
                net_income,
                ingestion_timestamp
            )
            SELECT
                raw_id,
                bank_code,
                CAST(year AS SMALLINT),
                CAST(branches AS INT),
                CAST(atms AS INT),
                CAST(total_clients AS INT),
                CAST(digital_clients AS INT),
                CAST(total_loans AS BIGINT),
                CAST(total_deposits AS BIGINT),
                CAST(net_income AS BIGINT),
                ingestion_timestamp
            FROM raw.bank_year_metrics_raw
            ON CONFLICT (bank_code, year)
            DO NOTHING;
        """))