from flask import Flask, request, jsonify
from email_service import authenticate_google_user, process_emails
from spreadsheet_service import add_job_to_sheet
from celery_app import app as celery_app, check_for_new_emails
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# OAuth Route for Google Authentication
@app.route('/api/oauth/google', methods=['GET'])
def google_oauth():
    try:
        # OAuth flow to authenticate a user
        user_email = request.args.get('email', 'default_user@example.com')
        service = authenticate_google_user(user_email)
        if service:
            return jsonify({"message": "OAuth login successful"}), 200
        else:
            return jsonify({"error": "OAuth login failed"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to start service
@app.route('/api/service/start', methods=['POST'])
def start_service():
    try:
        # Add the periodic task to Celery Beat
        celery_app.conf.beat_schedule = {
            'check-emails-every-45-seconds': {
                'task': 'celery_app.check_for_new_emails',
                'schedule': 45.0,  # Every 45 seconds
            },
        }
        celery_app.conf.timezone = 'UTC'

        return jsonify({"message": "Service scheduled successfully to run every 45 seconds"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to stop service
@app.route('/api/service/stop', methods=['POST'])
def stop_service():
    try:
        # Clear the Celery Beat schedule to stop the periodic tasks
        celery_app.conf.beat_schedule = {}  # Clear the schedule
        return jsonify({"message": "Service stopped successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to get spreadsheet status
@app.route('/api/spreadsheet/status', methods=['GET'])
def spreadsheet_status():
    try:
        # Retrieve data from the Google Spreadsheet using existing logic
        dummy_data = {
            "organization": "Example Org",
            "date_applied": "2024-11-22",
            "status": "Under Review",
            "position": "Software Developer",
            "urls": ["http://example.com"]
        }
        return jsonify(dummy_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)
