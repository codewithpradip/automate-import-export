
from automate_import_export_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification

@app.task
def celery_test_task():
    time.sleep(2) 
    # Send Email
    mail_subjest = 'this is test subject !'
    message = 'this is test message'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subjest,message,to_email)
    return 'Email Send successfully.'


@app.task
def import_data_task(file_path, model_name):
    try:
        call_command('importdata', file_path, model_name)
    except Exception as e:
        raise e

    # Notify the user by email
    mail_subjest='Import Data Completed'
    message='You data import has been successful'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subjest,message,to_email)
    return 'Data imported successfully'