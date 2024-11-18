import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

import json 
import os
load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_KEY")
)

email_body="""Hi Sanjyot,

Thank you for your interest in USAA and the Software Engineer - Early Careers role. After careful consideration, we have decided to pursue other candidates for this position.

We will retain your candidate profile in our database and may inform you of other job openings that match your profile.

We wish you the very best in your job search and encourage you to join our Talent Community at usaajobs.com to be alerted for future roles that you feel are a good match with your skills and experience. You will then receive notifications directly to your inbox for other opportunities based on your preferences.

Thank you for taking time to explore career opportunities at USAA.

Sincerely,
USAA Talent Acquisition"""

email_data = {
            'body': email_body,
        }



def classify_and_extract_email_informartion(email_data):
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
            "\"Organization\", \"Date applied\", \"Status\", \"Position\", and \"URLs\". "
            "The `Status` must only be one of the following values: \"Applied\", \"Under Review\", "
            "\"Online Assessment\", \"Interview\", or \"Rejected\". If the email does not explicitly "
            "state the status, infer it based on the email's content."
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
    )

    # Extract and return the JSON result from the model's response
    result = json.loads(completion.choices[0].message.content or "{}")
    print(result)
    return result


classify_and_extract_email_informartion(email_data)
