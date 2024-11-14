from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import spacy
from spreadsheet_service import add_job_to_sheet
import time
from datetime import datetime
from openai import OpenAI


from dotenv import load_dotenv
import os

load_dotenv()



CLIENT_SECRET_FILE = os.getenv('OAUTH_CLIENT_SECRET_FILE')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/spreadsheets' , 'https://www.googleapis.com/auth/drive']
OPENAIKEY = os.getenv('OPENAIKEY')
nlp = spacy.load("en_core_web_sm")
client = OpenAI(api_key=OPENAIKEY)

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
    
    service = build('gmail', 'v1', credentials=creds)
    return service


# def get_start_date():
#     # Define the file path for storing the start date
#     start_date_file = 'start_date.txt'
    
#     # Check if start_date.txt already exists
#     if os.path.exists(start_date_file):
#         # Read the stored start date from the file
#         with open(start_date_file, 'r') as file:
#             start_date = int(file.read().strip())
#     else:
#         # If it doesn't exist, set start_date to the current timestamp
#         start_date = int(time.time())
#         # Save this start date to start_date.txt for future runs
#         with open(start_date_file, 'w') as file:
#             file.write(str(start_date))
    
#     return start_date

def get_last_run_time():
    # Define the file path for storing the last run time
    last_run_file = 'last_run_time.txt'
    
    # Check if last_run_time.txt exists and read the timestamp
    if os.path.exists(last_run_file):
        with open(last_run_file, 'r') as file:
            last_run_time = int(file.read().strip())
    else:
        # If it doesn't exist, set last_run_time to a recent past date
        last_run_time = int(time.time()) - 60  # Set to 1 minute in the past as a safety buffer
    
    return last_run_time

def update_last_run_time():
    # Update last_run_time.txt with the current timestamp
    last_run_time = int(time.time())
    with open('last_run_time.txt', 'w') as file:
        file.write(str(last_run_time))

def fetch_job_details(service):
    start_date = get_last_run_time()
    
    # Use 'after' filter in the query to only fetch emails after the specified start date
    query = f"after:{start_date}"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages',[])
    print(messages)
    job_emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me',id=msg['id']).execute()
        email_subject = msg_data['payload']['headers'][0]['value']
        email_body = msg_data['snippet']
        email_data = {
            'body': email_body,
            'internalDate': msg_data.get('internalDate')
        }
        
        # job_info = extract_job_info(email_data)
        job_emails.append(email_data)
        # job_emails.append(email_body)
        # if 'Thank you for your interest' in email_subject.lower() or 'interview' in email_body.lower():
            
    update_last_run_time()
    return job_emails



def classify_email_status(email_body):
    # Convert the email body to lowercase for case-insensitive matching
    email_body = email_body.lower()
    
    # Check for "Online Assessment (OA)"
    if "online assessment" in email_body or "hackerank" in email_body or "take part in our assessment" in email_body:
        return "Online Assessment (OA)"
    
    # Check for "Rejected"
    elif ("unfortunately" in email_body and "won’t be moving it forward" in email_body) or \
         ("we appreciate" in email_body and "at this time" in email_body and "not moving forward" in email_body) or \
         ("not moving forward" in email_body) or \
         ("not selected" in email_body) or \
         ("another opportunity arises" in email_body):
        return "Rejected"
    
    # Check for "Applied"
    elif "thank you for applying" in email_body or \
         "we have received your application" in email_body or \
         "thank you for your interest" in email_body or \
         "our hiring team is reviewing" in email_body or \
         "if your application seems like a good fit" in email_body or \
         "we will contact you soon" in email_body:
        return "Applied"
    
    # Check for "Offer Received"
    elif "offer" in email_body and ("congratulations" in email_body or "pleased to offer" in email_body):
        return "Offer Received"
    
    # If none of the conditions matched, return "Unknown"
    else:
        return "Unknown"
        


def extract_job_info(email_data):
    doc = nlp(email_data['body'])
    job_info = {}

    for ent in doc.ents:
        if ent.label_ == "ORG":
            job_info['company'] = ent.text
    
    if 'internalDate' in email_data:
        timestamp = int(email_data['internalDate']) / 1000  # Convert milliseconds to seconds
        job_info['date_applied'] = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    else:
        job_info['date_applied'] = 'Unknown'

    job_info['status'] = classify_email_status(email_data['body'])

    return job_info

'''def classify_and_extract_openai(email_data):
    email_body = email_data['body']
    
    # Convert internalDate to a readable format if provided
    if email_data.get('internalDate'):
        date_received = datetime.fromtimestamp(int(email_data['internalDate']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
    else:
        date_received = "Unknown"
    
    # Define the messages for classification and entity extraction
    messages = [
        {"role": "system", "content": (
            "You are an assistant that extracts information from job application emails. "
            "Extract the following information as JSON with these fields: "
            "\"Organization\", \"Date applied\", \"Status\", \"Position\", and \"URLs\"."
        )},
        {"role": "user", "content": (
            f"Analyze the following email and extract:\n\n"
            f"Email received date: {date_received}\n\n"
            f"Email body:\n{email_body}\n\n"
            f"Provide the extracted information in JSON format with fields: "
            f"\"Organization\", \"Date applied\", \"Status\", \"Position\", and \"URLs\"."
        )}
    ]

    # Call the OpenAI API with the new chat completion method
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Use "gpt-4" if available; otherwise, use "gpt-3.5-turbo" or another model
        messages=messages,
        max_tokens=200,
        temperature=0
    )

    # Extract and return the JSON result from the model's response
    result = completion.choices[0].message['content'].strip()
    return result'''


def process_emails():
    service = authenticate_user()

    job_emails = fetch_job_details(service)


    for email_data in job_emails:
       job_info =  extract_job_info(email_data)
       add_job_to_sheet(job_info)




























        