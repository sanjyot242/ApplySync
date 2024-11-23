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