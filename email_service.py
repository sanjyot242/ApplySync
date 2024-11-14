from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import spacy
from spreadsheet_service import add_job_to_sheet


from dotenv import load_dotenv
import os

CLIENT_SECRET_FILE = os.getenv('CLIENT_SECRET_FILE')
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/spreadsheets']
nlp = spacy.load("en_core_web_sm")

def authenticate_user():
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=5000)
    service = build('gmail', 'v1', credentials=creds)
    return service


def fetch_job_details(service):
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages',[])
    job_emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me',id=msg['id']).execute()
        email_subject = msg_data['payload']['headers'][0]['value']
        email_body = msg_data['snippet']
        job_emails.append(email_body)
        # if 'job application' in email_subject.lower() or 'interview' in email_body.lower():
            
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


def extract_job_info(email_body):
    doc = nlp(email_body)
    job_info = {}

    for ent in doc.ents:
        if ent.label_ == "ORG":
            job_info['company'] = ent.text
        elif ent.label_ == "DATE":
            job_info['date_applied'] = ent.text

    job_info['status'] = classify_email_status(email_body)

    return job_info


def process_emails():
    service = authenticate_user()

    job_emails = fetch_job_details(service)


    for email_body in job_emails:
       job_info =  extract_job_info(email_body)
       add_job_to_sheet(job_info)



























        