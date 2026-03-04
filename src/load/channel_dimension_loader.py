from sqlalchemy import text
from src.config.db_config import get_engine


def load_dim_channel_default(connection=None):

    query = text("""
            INSERT INTO core.dim_channel (
                channel_code,
                channel_name,
                channel_description,
                effective_from,
                is_current
            )
            VALUES (
                'TOTAL',
                'Total Banco',
                'Agregado total sin segmentación por canal',
                CURRENT_DATE,
                TRUE
            )
            ON CONFLICT (channel_code, effective_from)
            DO NOTHING;
        """)

    if connection:
        connection.execute(query)
    else:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(query)