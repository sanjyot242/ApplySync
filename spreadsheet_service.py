import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_SECRET_FILE = os.getenv('OAUTH_CLIENT_SECRET_FILE')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/spreadsheets' , 'https://www.googleapis.com/auth/drive']

def authenticate_user():
    creds = None
    token_file = 'token.json'

    # Check if token.json exists and load the token
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    
    # If no valid token is available, request user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=5001)
        
        # Save the credentials for future use
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    return creds


def add_job_to_sheet(job_data):
    print(job_data)
    creds = authenticate_user()  # Authenticate user via OAuth
    client = gspread.authorize(creds)
    spreadsheet_name = 'Job Test'
    try:
        spreadsheet = client.open(spreadsheet_name)
        sheet = spreadsheet.sheet1
        print("Opened existing sheet.")
    except gspread.SpreadsheetNotFound:
        spreadsheet = client.create(spreadsheet_name)
        sheet = spreadsheet.sheet1
        print("Created new sheet.")

        # Set up headers for the new sheet if it was just created
        headers = list(job_data.keys())
        sheet.append_row(headers)
        print("Added headers to new sheet.")

    # Append job_data values as a row in the sheet
    row = [job_data.get(key, 'N/A') for key in job_data.keys()]
    sheet.append_row(row)
    print("Data added to the sheet.")
