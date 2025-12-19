import os
from typing import Dict
import pandas as pd

from app.seo.sheets_client import ScreamingFrogSheetsClient
from app.seo.query_engine import SEOQueryEngine


class SEOAgent:
    def __init__(self):
        self.sheet_url = os.getenv("SCREAMING_FROG_SHEET_URL")

        # SAFE MODE (no crash)
        if not self.sheet_url:
            self.enabled = False
            self.error = "SCREAMING_FROG_SHEET_URL is not configured"
            return

        self.enabled = True

    def run(self, query: str) -> Dict:
        if not self.enabled:
            return {
                "agent": "SEO",
                "status": "disabled",
                "reason": self.error
            }

        try:
            df = self.get_dataframe()
            engine = SEOQueryEngine(df)
            q = query.lower()

            if "https" in q and "title" in q:
                urls = engine.non_https_and_long_titles()
                return {
                    "agent": "SEO",
                    "count": len(urls),
                    "urls": urls
                }

            if "indexability" in q or "indexable" in q:
                overview = engine.indexability_overview()
                percentage = engine.indexable_percentage()
                return {
                    "agent": "SEO",
                    "indexability_breakdown": overview,
                    "indexable_percentage": percentage
                }

            return {
                "agent": "SEO",
                "message": "Query not supported yet"
            }

        except Exception as e:
            return {
                "agent": "SEO",
                "error": str(e)
            }

    def get_dataframe(self) -> pd.DataFrame:
        client = ScreamingFrogSheetsClient(self.sheet_url)
        return client.load()
