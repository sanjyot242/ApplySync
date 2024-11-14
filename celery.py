from celery import Celery
from email_service import process_emails

# Configure Celery to use Redis as the broker and backend
app = Celery(
    'job_tracker',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Run check_for_new_emails every 45 seconds
    sender.add_periodic_task(45.0, check_for_new_emails.s(), name='Check for job emails every 45 seconds')

@app.task
def check_for_new_emails():
    # Task to process job application emails
    process_emails()
