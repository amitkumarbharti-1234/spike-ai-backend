from google.analytics.data_v1beta import BetaAnalyticsDataClient
from app.ga4.credential import load_ga4_credentials
def get_ga4_client():
    credentials = load_ga4_credentials()
    client = BetaAnalyticsDataClient(credentials=credentials)
    return client
