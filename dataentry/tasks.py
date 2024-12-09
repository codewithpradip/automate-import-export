
from automate_import_export_main.celery import app
import time
from django.core.management import call_command
from django.core.mail import EmailMessage
from django.conf import settings
from .utils import send_email_notification, generate_csv_file

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
    mail_subject='Import Data Completed'
    message='Your data import has been successful'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email)
    return 'Data imported successfully'

@app.task
def export_data_task(model_name):
    try:
        call_command('exportdata', model_name)
    except Exception as e:
        raise e
    # Send Email with attachment
    file_path = generate_csv_file(model_name)
    mail_subject = 'Export Data Completed'
    message = 'Your data export has been successful. Please find the attachment'
    to_email = settings.DEFAULT_TO_EMAIL
    send_email_notification(mail_subject,message,to_email,attachment=file_path)
    return 'Data exported successfully'
