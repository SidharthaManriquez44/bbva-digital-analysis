from src.config.logger_config import get_logger
from src.extract.bbva_manual_loader import extract_bbva_data
from src.load.raw_loader import load_raw
from src.load.staging_loader import load_staging
from src.load.date_dimension_loader import load_dim_date_from_staging
from src.load.bank_dimension_loader import load_dim_bank_from_staging
from src.load.channel_dimension_loader import load_dim_channel_default
from src.load.fact_loader import load_fact_from_staging
from src.load.mart_loader import MartLoader
from dotenv import load_dotenv
load_dotenv()


logger = get_logger("bank_pipeline")


def run_pipeline():
    logger.info("Starting pipeline...")

    df_raw = extract_bbva_data()
    logger.info(f"Extracted {len(df_raw)} rows")

    load_raw(df_raw)
    logger.info("Loaded RAW layer")
    load_staging()
    logger.info("Loaded staging layer")
    load_dim_date_from_staging()
    load_dim_bank_from_staging()
    load_dim_channel_default()
    logger.info("Dimensions upserted")
    load_fact_from_staging()
    logger.info("Fact table upserted")
    mart_loader = MartLoader()
    mart_loader.load_bank_financial_year()
    mart_loader.load_bank_digital_year()
    mart_loader.load_bank_efficiency_year()
    mart_loader.load_bank_growth_year()
    logger.info("Loaded Mart layer")
    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    run_pipeline()