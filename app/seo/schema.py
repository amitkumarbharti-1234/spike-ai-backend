class SEOSchema:
    URL_COLUMNS = ["Address", "URL"]
    TITLE_COLUMNS = ["Title 1", "Title"]
    INDEXABILITY_COLUMNS = ["Indexability"]
    STATUS_COLUMNS = ["Status Code"]
    @staticmethod
    def find_column(df, candidates):
        for col in candidates:
            if col in df.columns:
                return col
        return None
