
class BankAnalysisService:

    def __init__(self, repository, analyzer_class):
        self.repository = repository
        self.analyzer_class = analyzer_class

    def execute(self, branch: str):

        df = self.repository.get_bank_kpis(branch)
        df_structural = self.repository.get_structural_model_data(branch)

        analyzer = self.analyzer_class(df)
        analyzer_structural = self.analyzer_class(df_structural)

        analyzer.validate_data()
        analyzer_structural.validate_data()

        corr = analyzer.correlation(
            "digital_penetration_pct",
            "profit_per_branch"
        )

        regression = analyzer.fit_regression(
            "digital_penetration_pct",
            "profit_per_branch"
        )

        projection = analyzer.project_future(
            base_year_col="year",
            target_col="digital_penetration_pct",
            future_years=[2025, 2026, 2027]
        )

        features = [
            "digital_penetration_pct",
            "branches",
            "atms"
        ]

        summary = analyzer_structural.fit_multivariable_regression(
            x_cols=features,
            y_col="profit_per_branch"
        )

        return {
            "correlation": corr,
            "regression": regression,
            "projection": projection,
            "summary": summary
        }