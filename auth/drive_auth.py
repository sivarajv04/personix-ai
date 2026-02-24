from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle
from pathlib import Path

SCOPES = ['https://www.googleapis.com/auth/drive']

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TOKEN_PATH = PROJECT_ROOT / "token.pickle"
CREDS_PATH = PROJECT_ROOT / "credentials.json"


def get_drive_service():
    creds = None

    if TOKEN_PATH.exists():
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDS_PATH, SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return build('drive', 'v3', credentials=creds)
