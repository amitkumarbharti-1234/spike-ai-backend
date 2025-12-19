from typing import Dict
import pandas as pd
class SEOMetaAnalyzer:
    def analyze(self, seo_df: pd.DataFrame) -> Dict[str, Dict]:
        if seo_df is None or seo_df.empty:
            return {}
        url_col = None
        meta_col = None
        for col in seo_df.columns:
            if col.lower() in ["address", "url"]:
                url_col = col
            if "meta description" in col.lower():
                meta_col = col
        if not url_col or not meta_col:
            return {}
        seo_df[meta_col] = seo_df[meta_col].fillna("").str.strip()

        duplicate_meta = seo_df[meta_col].duplicated(keep=False)

        meta_map = {}

        for _, row in seo_df.iterrows():
            url = str(row[url_col]).strip()
            meta_desc = row[meta_col]

            if not meta_desc:
                issue = "missing"
            elif duplicate_meta.loc[_]:
                issue = "duplicate"
            else:
                issue = "ok"

            meta_map[url] = {
                "meta_description": meta_desc if meta_desc else None,
                "meta_issue": issue
            }

        return meta_map
