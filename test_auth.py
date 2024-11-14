from google_auth_oauthlib.flow import InstalledAppFlow
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')

# Define the scopes you need
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

def authenticate_user():
    # Initialize the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=5000)  # Starts local server for authentication
    print("Authenticated Successfully")
    return creds

if __name__ == '__main__':
    authenticate_user()
