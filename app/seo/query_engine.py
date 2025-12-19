import pandas as pd
from app.seo.schema import SEOSchema


class SEOQueryEngine:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    def non_https_and_long_titles(self, title_length: int = 60):
        url_col = SEOSchema.find_column(self.df, SEOSchema.URL_COLUMNS)
        title_col = SEOSchema.find_column(self.df, SEOSchema.TITLE_COLUMNS)
        if not url_col or not title_col:
            return []
        filtered = self.df[
            (~self.df[url_col].str.startswith("https")) &
            (self.df[title_col].fillna("").str.len() > title_length)
        ]
        return filtered[url_col].tolist()
    def indexability_overview(self):
        index_col = SEOSchema.find_column(self.df, SEOSchema.INDEXABILITY_COLUMNS)
        if not index_col:
            return {}
        return self.df[index_col].value_counts().to_dict()
    def indexable_percentage(self):
        index_col = SEOSchema.find_column(self.df, SEOSchema.INDEXABILITY_COLUMNS)
        if not index_col:
            return 0.0
        total = len(self.df)
        indexable = len(self.df[self.df[index_col] == "Indexable"])
        if total == 0:
            return 0.0
        return round((indexable / total) * 100, 2)
