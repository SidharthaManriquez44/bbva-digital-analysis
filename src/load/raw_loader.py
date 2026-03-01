from src.config.db_config import get_engine

def load_raw(df):
    engine = get_engine()

    df.to_sql(
        name="bank_year_metrics_raw",
        schema="raw",
        con=engine,
        if_exists="append",
        index=False
    )