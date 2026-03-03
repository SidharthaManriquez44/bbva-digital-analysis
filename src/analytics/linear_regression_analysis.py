import pandas as pd
from src.config.db_config import get_engine
from sklearn.linear_model import LinearRegression
from dotenv import load_dotenv
load_dotenv()

# ----------------------------------------------------------
#               Load BBVA data from DW
# ----------------------------------------------------------

def load_data():
    engine = get_engine()
    query = """
        SELECT 
            year,
            digital_penetration_pct,
            profit_per_branch
        FROM mart.bank_kpi_year
        WHERE bank_code = 'BBVA'
        ORDER BY year;
    """

    df = pd.read_sql(query, engine)

    return df


if __name__ == "__main__":
    df = load_data()

    print("\nRaw Data:\n")
    print(df)
    # Basic validation
    print("\nNull check:\n")
    print(df.isnull().sum())

    print("\nDescriptive stats:\n")
    print(df.describe())
    # Formal correlation
    correlation = df["digital_penetration_pct"].corr(df["profit_per_branch"])

    print(f"\nPearson Correlation: {correlation:.4f}")
    # ----------------------------------------------------------
    #               Linear Regression
    # ----------------------------------------------------------

    X = df[["digital_penetration_pct"]].copy()
    y = df["profit_per_branch"]

    model = LinearRegression()
    model.fit(X, y)

    slope = model.coef_[0]
    intercept = model.intercept_
    r_squared = model.score(X, y)

    print("\n--- Linear Regression Results ---")
    print(f"Slope (β1): {slope:,.2f}")
    print(f"Intercept (β0): {intercept:,.2f}")
    print(f"R-squared: {r_squared:.4f}")

    # Prepare data for Dashboard
    df["predicted_profit"] = model.predict(X)

    print("\nWith Predictions:\n")
    print(df)

    # Simple projection
    X_year = df[["year"]]
    y_pen = df["digital_penetration_pct"]

    trend_model = LinearRegression()
    trend_model.fit(X_year, y_pen)

    future_years = pd.DataFrame({"year": [2025, 2026, 2027]})

    future_penetration = trend_model.predict(future_years)

    future_pen_df = pd.DataFrame(
        future_penetration,
        columns=["digital_penetration_pct"]
    )

    future_profit = model.predict(future_pen_df)

    projection = pd.DataFrame({
        "year": future_years["year"],
        "projected_penetration": future_penetration,
        "projected_profit_per_branch": future_profit
    })

    print("\nProjection 2025–2027:\n")
    print(projection)