import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


def get_credentials_path():
    """Return the path to credentials.json"""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'credentials.json')


def is_authenticated():
    """Check if user is authenticated (credentials.json exists and is valid)"""
    creds_path = get_credentials_path()
    return os.path.exists(creds_path)


def load_credentials():
    """Load credentials from credentials.json if it exists"""
    creds_path = get_credentials_path()
    if not os.path.exists(creds_path):
        return None

    with open(creds_path, 'r') as f:
        creds_data = json.load(f)

    creds = Credentials.from_authorized_user_info(creds_data, scopes=[
        'https://www.googleapis.com/auth/gmail.readonly'
    ])

    return creds


def save_credentials(creds):
    """Save credentials to credentials.json"""
    creds_path = get_credentials_path()
    creds_data = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

    with open(creds_path, 'w') as f:
        json.dump(creds_data, f, indent=2)


def refresh_token_if_needed(creds):
    """Refresh access token if expired"""
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        save_credentials(creds)
    return creds


def get_gmail_service():
    """Get authenticated Gmail API service client"""
    from googleapiclient.discovery import build

    creds = load_credentials()
    if not creds:
        return None

    creds = refresh_token_if_needed(creds)
    service = build('gmail', 'v1', credentials=creds)

    return service


def start_oauth_flow(client_secrets_file='client_secret.json'):
    """
    Start OAuth 2.0 flow. User must have downloaded client_secret.json from Google Cloud Console.
    Returns the authorization URL.
    """
    if not os.path.exists(client_secrets_file):
        raise FileNotFoundError(
            f"{client_secrets_file} not found. Download from Google Cloud Console OAuth 2.0 credentials."
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_file,
        scopes=['https://www.googleapis.com/auth/gmail.readonly']
    )

    creds = flow.run_local_server(port=0)
    save_credentials(creds)

    return creds


def logout():
    """Delete credentials.json to log out"""
    creds_path = get_credentials_path()
    if os.path.exists(creds_path):
        os.remove(creds_path)
