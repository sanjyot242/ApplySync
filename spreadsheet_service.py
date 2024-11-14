import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import os

CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/spreadsheets']

def add_job_to_sheet(job_data):
    creds = Credentials.from_service_account_file(CLIENT_SECRET_FILE,scopes = SCOPES)
    client = gspread.authorize(creds)
    sheet = client.create('Job Applications').sheet1

    # Append new row to the sheet
    sheet.append_row([
        job_data.get('date_applied', 'N/A'),
        job_data.get('company', 'N/A'),
        job_data.get('status', 'N/A')
    ])
