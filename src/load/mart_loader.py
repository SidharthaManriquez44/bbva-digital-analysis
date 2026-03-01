from sqlalchemy import text
from src.config.db_config import get_engine
from src.config.logger_config import get_logger


class MartLoader:

    def __init__(self):
        self.engine = get_engine()
        self.logger = get_logger(__name__)

    def load_bank_financial_year(self):

        self.logger.info("Loading mart.bank_financial_year...")

        truncate_sql = text("TRUNCATE mart.bank_financial_year;")

        insert_sql = text("""
            INSERT INTO mart.bank_financial_year (
                bank_code,
                year,
                total_loans,
                total_deposits,
                net_income
            )
            SELECT
                b.bank_code,
                d.year,
                SUM(f.total_loans),
                SUM(f.total_deposits),
                SUM(f.net_income)
            FROM core.fact_bank_metrics f
            JOIN core.dim_bank b
            ON f.bank_key = b.bank_key
            JOIN core.dim_date d
            ON f.date_key = d.date_key
            GROUP BY b.bank_code, d.year;
        """)

        with self.engine.begin() as conn:
            conn.execute(truncate_sql)
            conn.execute(insert_sql)

        self.logger.info("bank_financial_year loaded successfully.")

    def load_bank_digital_year(self):
        self.logger.info("Loading mart.bank_digital_year...")

        truncate_sql = text("TRUNCATE mart.bank_digital_year;")

        insert_sql = text("""
                          INSERT INTO mart.bank_digital_year (bank_code,
                                                              year,
                                                              digital_clients,
                                                              total_clients,
                                                              digital_penetration_pct)
                          SELECT f.bank_key,
                                 d.year,
                                 SUM(f.digital_clients),
                                 SUM(f.total_clients),
                                 ROUND(
                                         (SUM(f.digital_clients)::numeric 
                     / NULLIF(SUM(f.total_clients),0)) * 100,
                                         2
                                 )
                          FROM core.fact_bank_metrics f
                                   JOIN core.dim_date d
                                        ON f.date_key = d.date_key
                          GROUP BY f.bank_key, d.year;
                          """)

        with self.engine.begin() as conn:
            conn.execute(truncate_sql)
            conn.execute(insert_sql)

        self.logger.info("bank_digital_year loaded successfully.")

    def load_bank_efficiency_year(self):
        self.logger.info("Loading mart.bank_efficiency_year...")

        truncate_sql = text("TRUNCATE mart.bank_efficiency_year;")

        insert_sql = text("""
                          INSERT INTO mart.bank_efficiency_year (
                                bank_code,
                                year,
                                branches,
                                atms,
                                clients_per_branch,
                                loans_per_branch,
                                deposits_per_branch,
                                profit_per_branch
                                )
                                SELECT
                                b.bank_code,
                                d.year,
                                
                                MAX(f.branches) AS branches,
                                MAX(f.atms) AS atms,
                                
                                ROUND(SUM(f.total_clients)::numeric 
                                      / NULLIF(MAX(f.branches),0), 2),
                                
                                ROUND(SUM(f.total_loans) 
                                      / NULLIF(MAX(f.branches),0), 2),
                                
                                ROUND(SUM(f.total_deposits) 
                                      / NULLIF(MAX(f.branches),0), 2),
                                
                                ROUND(SUM(f.net_income) 
                                      / NULLIF(MAX(f.branches),0), 2)
                                
                                FROM core.fact_bank_metrics f
                                JOIN core.dim_bank b
                                ON f.bank_key = b.bank_key
                                JOIN core.dim_date d
                                ON f.date_key = d.date_key
                                
                                GROUP BY b.bank_code, d.year;
                          """)

        with self.engine.begin() as conn:
            conn.execute(truncate_sql)
            conn.execute(insert_sql)

        self.logger.info("bank_efficiency_year loaded successfully.")

    def load_bank_growth_year(self):
        self.logger.info("Loading mart.bank_growth_year...")

        truncate_sql = text("TRUNCATE mart.bank_growth_year;")

        insert_sql = text("""
                          INSERT INTO mart.bank_growth_year (bank_code,
                                                             year,
                                                             loans_yoy_pct,
                                                             deposits_yoy_pct,
                                                             net_income_yoy_pct)
                          SELECT bank_code, year, ROUND(
                              (total_loans
                              - LAG(total_loans) OVER w)
                              / NULLIF (LAG(total_loans) OVER w, 0)
                              * 100, 2
                              ), ROUND(
                              (total_deposits
                              - LAG(total_deposits) OVER w)
                              / NULLIF (LAG(total_deposits) OVER w, 0)
                              * 100, 2
                              ), ROUND(
                              (net_income
                              - LAG(net_income) OVER w)
                              / NULLIF (LAG(net_income) OVER w, 0)
                              * 100, 2
                              )

                          FROM mart.bank_financial_year
                              WINDOW w AS (
                              PARTITION BY bank_code
                              ORDER BY year
                              );
                          """)

        with self.engine.begin() as conn:
            conn.execute(truncate_sql)
            conn.execute(insert_sql)

        self.logger.info("bank_growth_year loaded successfully.")