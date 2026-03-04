from src.data_access.bank_repository import BankRepository
from src.analytics.bank_analysis import BankAnalyzer
from src.domain.bank_analysis_service import BankAnalysisService
from dotenv import load_dotenv
load_dotenv()

def run(branch: str):

    repo = BankRepository()

    service = BankAnalysisService(
        repository=repo,
        analyzer_class=BankAnalyzer
    )

    return service.execute(branch)


if __name__ == "__main__":
    results = run("BBVA")
    print(results)