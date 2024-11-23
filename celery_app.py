# from celery import Celery
# from email_service import process_emails
# from dotenv import load_dotenv
# # Configure Celery to use Redis as the broker and backend
# app = Celery(
#     'job_tracker',
#     broker='amqp://guest:guest@localhost:5672//',    # RabbitMQ as broker
#     backend='rpc://'                                 # RabbitMQ as result backend
# )

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Run check_for_new_emails every 45 seconds
#     sender.add_periodic_task(45.0, check_for_new_emails.s(), name='Check for job emails every 45 seconds')

# @app.task
# def check_for_new_emails():
#     # Task to process job application emails
#     print("Working")
#     process_emails()

# # check_for_new_emails.delay()


from celery import Celery
from email_service import process_emails
from dotenv import load_dotenv
import os
import logging

load_dotenv()

# Configure Celery to use RabbitMQ as the broker and backend
app = Celery(
    'job_tracker',
    broker='amqp://guest:guest@localhost:5672//',  # RabbitMQ as broker
    backend='rpc://'                                # RabbitMQ as result backend
)

# Logging setup
logging.basicConfig(level=logging.DEBUG)

logging.getLogger("pymongo").setLevel(logging.WARNING)
# Define the task without scheduling it automatically
@app.task
def check_for_new_emails():
    # Task to process job application emails
    logging.warning("Task started: Checking for new emails...")
    try:
        process_emails()
        logging.info("Task completed successfully.")
    except Exception as e:
        logging.error(f"Error processing emails: {e}")

# No automatic periodic scheduling here; Beat schedule is set dynamically via Flask
app.conf.beat_schedule = {}  # Empty initially, will be set via Flask
app.conf.timezone = 'UTC'
