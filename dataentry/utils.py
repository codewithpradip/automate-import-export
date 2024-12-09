from django.apps import apps
from django.core.management.base import CommandError
import csv
from django.db.utils import DataError
from django.core.mail import EmailMessage
from django.conf import settings
import datetime, os

def get_all_custom_model():
    exclude_model = ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'Upload']
    include_model = []
    for model in apps.get_models():
        if model.__name__ not in exclude_model:
            include_model.append(model.__name__)
    return include_model

def check_csv_error(file_path, model_name):
    model = None
        #search for the model acroll all installed apps
    for app_config in apps.get_app_configs():
        # try to search for the model
        try:
            model = apps.get_model(app_config.label, model_name)
            break # Stop to search once model is found
        except LookupError: 
            continue # Continue searching in next app, if model not found in this app
    
    if not model:
        raise CommandError(f'Model "{model_name}" not found in any apps !')
        
    try:
        with open(file_path, 'r') as file:
                # Reads CSV files and maps the information into a dictionary.
            reader = csv.DictReader(file)

            # Compare CSV header with table's field names       
            model_fields = [ field.name for field in model._meta.fields if field.name != 'id']
            csv_header = reader.fieldnames
            if csv_header != model_fields:
                raise DataError(f"CSV header doesn't match with the {model_name} table fields. ")
    except Exception as e:
        raise e

    return model


def send_email_notification(mail_subjest, message, to_email, attachment=None):
    """ Send email notification to the user. """
    try:
        from_email = settings.DEFAULT_FROM_EMAIL
        mail = EmailMessage(mail_subjest, message, from_email, to=[to_email])
        if attachment is not None:
            mail.attach_file(attachment)
        mail.send()
    except Exception as e:
        raise e

def generate_csv_file(model_name):
     # generate timestap of the current Data/Time
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    # Define the csv file name/path
    export_dir = 'exported_data'
    file_name = f'exported_{model_name}_data_{timestamp}.csv'
    file_path = os.path.join(settings.MEDIA_ROOT, export_dir, file_name)
    return file_path
