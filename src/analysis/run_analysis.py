from src.data_access.bank_repository import BankRepository
from src.analytics.bank_analyzer import BankAnalyzer
from dotenv import load_dotenv
load_dotenv()

branch = "BBVA"

if __name__ == "__main__":

    repo = BankRepository()
    df = repo.get_bank_kpis(branch)
    df_structural = repo.get_structural_model_data(branch)
    analyzer = BankAnalyzer(df)
    analyzer_structural = BankAnalyzer(df_structural)
    analyzer.validate_data()
    analyzer_structural.validate_data()

    print("\nDescriptive Stats\n")
    print(df.describe())

    # Correlation
    corr = analyzer.correlation(
        "digital_penetration_pct",
        "profit_per_branch"
    )

    print(f"\nPearson Correlation: {corr:.4f}")

    # Regression
    results = analyzer.fit_regression(
        "digital_penetration_pct",
        "profit_per_branch"
    )

    print("\nRegression Results:")
    print(results)

    # Add predictions
    df_with_pred = analyzer.add_predictions("digital_penetration_pct")

    print("\nWith Predictions:\n")
    print(df_with_pred)

    # Future projection
    projection = analyzer.project_future(
        base_year_col="year",
        target_col="digital_penetration_pct",
        future_years=[2025, 2026, 2027]
    )

    print("\nProjection:\n")
    print(projection)


    # Variables multivariable
    features = [
        "digital_penetration_pct",
        "branches",
        "atms"
    ]

    summary = analyzer_structural.fit_multivariable_regression(
        x_cols=features,
        y_col="profit_per_branch"
    )

    print(summary)

    print("\nKey Metrics:")
    print(analyzer_structural.extract_key_metrics(features))

    print("\nVIF:")
    print(analyzer_structural.calculate_vif(features))

    print("\nBreusch-Pagan Test:")
    print(analyzer_structural.breusch_pagan_test())
