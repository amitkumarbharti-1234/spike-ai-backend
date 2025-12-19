import os
from google.oauth2 import service_account

GA4_SCOPES = [
    "https://www.googleapis.com/auth/analytics.readonly"
]

def load_ga4_credentials():
    """
    Loads GA4 service account credentials from credentials.json
    located at the project root.

    This file will be replaced by evaluators.
    """

    credentials_path = os.path.join(
        os.getcwd(),
        "credentials.json"
    )

    if not os.path.exists(credentials_path):
        raise FileNotFoundError(
            "credentials.json not found at project root"
        )

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path,
        scopes=GA4_SCOPES
    )

    return credentials
