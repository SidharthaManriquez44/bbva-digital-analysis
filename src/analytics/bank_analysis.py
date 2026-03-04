import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from sklearn.preprocessing import StandardScaler


class BankAnalyzer:

    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.model = None

    # ----------------------------------------------------------
    #                   Validation
    # ----------------------------------------------------------

    def validate_data(self):
        if self.df.isnull().any().any():
            raise ValueError("Dataset contains null values.")

        if len(self.df) < 3:
            raise ValueError("Not enough data points for analysis.")

    # ----------------------------------------------------------
    #                   Correlation
    # ----------------------------------------------------------

    def correlation(self, x_col: str, y_col: str) -> float:
        return self.df[x_col].corr(self.df[y_col])

    # ----------------------------------------------------------
    #                   Linear Regression
    # ----------------------------------------------------------

    def fit_regression(self, x_col: str, y_col: str):

        X = self.df[[x_col]].copy()
        y = self.df[y_col]

        model = LinearRegression()
        model.fit(X, y)

        self.model = model

        return {
            "slope": model.coef_[0],
            "intercept": model.intercept_,
            "r_squared": model.score(X, y)
        }

    # ----------------------------------------------------------
    #                   Predictions
    # ----------------------------------------------------------

    def add_predictions(self, x_col: str) -> pd.DataFrame:

        if self.model is None:
            raise ValueError("Model not fitted yet.")

        X = self.df[[x_col]].copy()
        self.df["predicted_profit"] = self.model.predict(X)

        return self.df

    # ----------------------------------------------------------
    #                   Projection
    # ----------------------------------------------------------

    def project_future(
        self,
        base_year_col: str,
        target_col: str,
        future_years: list[int]
    ) -> pd.DataFrame:

        trend_model = LinearRegression()
        X_year = self.df[[base_year_col]]
        y_target = self.df[target_col]

        trend_model.fit(X_year, y_target)

        future_df = pd.DataFrame({base_year_col: future_years})
        future_values = trend_model.predict(future_df)

        return pd.DataFrame({
            "year": future_years,
            f"projected_{target_col}": future_values
        })
    # ----------------------------------------------------------
    #                   Standardization
    # ----------------------------------------------------------
    def normalize_features(self, columns: list[str]) -> pd.DataFrame:

        scaler = StandardScaler()
        self.df[columns] = scaler.fit_transform(self.df[columns])

        return self.df

    # ----------------------------------------------------------
    #            Professional Multivariable Regression
    # ----------------------------------------------------------
    def fit_multivariable_regression(self, x_cols: list[str], y_col: str):

        X = self.df[x_cols]
        X = sm.add_constant(X)
        y = self.df[y_col]

        model = sm.OLS(y, X).fit()

        self.model = model

        return model.summary()

    # ----------------------------------------------------------
    #            Extract key economic metrics
    # ----------------------------------------------------------
    def extract_key_metrics(self, x_cols: list[str]):

        if self.model is None:
            raise ValueError("Run regression first.")

        results = {}

        for col in x_cols:
            elasticity = (
                    self.model.params[col] *
                    (self.df[col].mean() / self.df[self.model.model.endog_names].mean())
            )

            results[col] = {
                "coef": self.model.params[col],
                "p_value": self.model.pvalues[col],
                "t_stat": self.model.tvalues[col],
                "elasticity": elasticity,
                "ci_lower": self.model.conf_int().loc[col][0],
                "ci_upper": self.model.conf_int().loc[col][1]
            }

        return results

    # ----------------------------------------------------------
    #            VIF — Multicollinearity
    # ----------------------------------------------------------

    def calculate_vif(self, x_cols: list[str]):

        X = self.df[x_cols]
        X = sm.add_constant(X)

        vif_data = pd.DataFrame()
        vif_data["feature"] = X.columns
        vif_data["VIF"] = [
            variance_inflation_factor(X.values, i)
            for i in range(X.shape[1])
        ]

        return vif_data

    # ----------------------------------------------------------
    #            Heteroskedasticity (Breusch–Pagan)
    # ----------------------------------------------------------
    def breusch_pagan_test(self):

        if self.model is None:
            raise ValueError("Run regression first.")

        residuals = self.model.resid
        exog = self.model.model.exog

        test = het_breuschpagan(residuals, exog)

        labels = [
            "LM Statistic",
            "LM-Test p-value",
            "F-Statistic",
            "F-Test p-value"
        ]

        return dict(zip(labels, test))