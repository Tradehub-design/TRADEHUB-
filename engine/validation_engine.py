import pandas as pd


class ValidationEngine:

    @staticmethod
    def dataframe(df):

        return isinstance(df, pd.DataFrame)

    @staticmethod
    def has_rows(df):

        return (
            isinstance(df, pd.DataFrame)
            and not df.empty
        )

    @staticmethod
    def has_column(df, column):

        return (
            ValidationEngine.has_rows(df)
            and column in df.columns
        )

    @staticmethod
    def safe_value(value, default="-"):

        if value is None:
            return default

        if value == "":
            return default

        try:
            if pd.isna(value):
                return default
        except Exception:
            pass

        return value
