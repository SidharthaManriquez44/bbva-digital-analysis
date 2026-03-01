import pandas as pd
from sqlalchemy import text
from src.config.db_config import get_engine


class BankRepository:

    def __init__(self):
        self.engine = get_engine()

    def get_bank_kpis(self, bank_code: str) -> pd.DataFrame:

        query = text("""
            SELECT 
                year,
                digital_penetration_pct,
                profit_per_branch
            FROM mart.bank_kpi_year
            WHERE bank_code = :bank_code
            ORDER BY year;
        """)

        with self.engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn,
                params={"bank_code": bank_code}
            )

        return df

    def get_structural_model_data(self, bank_code: str) -> pd.DataFrame:
        query = text("""
                     SELECT
                         year, 
                         digital_penetration_pct, 
                         branches, 
                         atms, 
                         total_clients, 
                         digital_clients, 
                         total_loans, 
                         total_deposits, 
                         net_income, 
                         profit_per_branch
                     FROM mart.bank_kpi_year
                     WHERE bank_code = :bank_code
                     ORDER BY year;
                     """)

        with self.engine.connect() as conn:
            df = pd.read_sql(
                query,
                conn,
                params={"bank_code": bank_code}
            )

        return df