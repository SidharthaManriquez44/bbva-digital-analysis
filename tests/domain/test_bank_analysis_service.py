import pandas as pd

class FakeRepository:
    def get_bank_kpis(self, branch):
        return pd.DataFrame({
            "year": [2020],
            "digital_penetration_pct": [50],
            "profit_per_branch": [100],
            "branches": [10],
            "atms": [100]
        })

    def get_structural_model_data(self, branch):
        return self.get_bank_kpis(branch)


class FakeAnalyzer:

    def __init__(self, df):
        self.df = df

    def validate_data(self):
        pass

    def correlation(self, x, y):
        return 0.9

    def fit_regression(self, x, y):
        return "regression"

    def project_future(self, **kwargs):
        return "projection"

    def fit_multivariable_regression(self, x_cols, y_col):
        return "summary"


def test_execute_bank_analysis():

    from src.domain.bank_analysis_service import BankAnalysisService

    service = BankAnalysisService(
        repository=FakeRepository(),
        analyzer_class=FakeAnalyzer
    )

    result = service.execute("BBVA")

    assert result["correlation"] == 0.9
    assert result["regression"] == "regression"
    assert result["summary"] == "summary"