import gspread
from google_auth_oauthlib.flow import InstalledAppFlow
from gspread.exceptions import SpreadsheetNotFound, APIError
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
    """
    Adds job application data to a Google Sheet.

    Args:
        job_data (dict): Dictionary containing job application details.
    """
    print("Job Data to Add:", job_data)
    
    # Authenticate user via OAuth
    try:
        creds = authenticate_user()  # Replace with your OAuth logic
        client = gspread.authorize(creds)
    except Exception as e:
        print(f"Error during authentication: {e}")
        return

    # Define the spreadsheet name
    spreadsheet_name = 'Job Application Staus'

    # Attempt to open or create the spreadsheet
    try:
        spreadsheet = client.open(spreadsheet_name)
        sheet = spreadsheet.sheet1
        print("Opened existing sheet.")
    except SpreadsheetNotFound:
        print(f"Spreadsheet '{spreadsheet_name}' not found. Creating a new one...")
        spreadsheet = client.create(spreadsheet_name)
        sheet = spreadsheet.sheet1

        # Add headers to the new sheet
        headers = ["Organization", "Date applied", "Status", "Position", "URLs"]
        sheet.append_row(headers)
        print("Added headers to new sheet.")

    # Prepare data for appending
    row = [
        job_data.get("Organization", "N/A"),
        job_data.get("Date applied", "N/A"),
        job_data.get("Status", "N/A"),
        job_data.get("Position", "N/A"),
        ", ".join(job_data.get("URLs", [])) if isinstance(job_data.get("URLs", []), list) else "N/A"
    ]

    # Append data to the sheet
    try:
        sheet.append_row(row)
        print("Data added to the sheet.")
    except APIError as e:
        print(f"Error while adding data to the sheet: {e}")
