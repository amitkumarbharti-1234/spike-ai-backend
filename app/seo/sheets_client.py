import pandas as pd
import os
class ScreamingFrogSheetsClient:
    def __init__(self, sheet_url: str):
        self.sheet_url = sheet_url
    def load(self) -> pd.DataFrame:        
        try:
            csv_url = self.sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")
            df = pd.read_csv(csv_url)
            return df
        except Exception as e:
            raise RuntimeError(f"Failed to load Google Sheet: {e}")
