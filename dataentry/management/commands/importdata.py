from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db.utils import DataError

# Custom management command - python manage.py importdata file_path model_name
class Command(BaseCommand):
    help="Import data from CSV file"

    # Accept file_path from terminal
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')
        parser.add_argument('model_name', type=str, help='Name of the model')

    # Executed when the command Run
    def handle(self, *args, **kwargs):
        file_path=kwargs['file_path']
        model_name=kwargs['model_name'].capitalize()

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
            

        with open(file_path, 'r') as file:
             # Reads CSV files and maps the information into a dictionary.
            reader = csv.DictReader(file)

            # Compare CSV header with table's field names       
            model_fields = [ field.name for field in model._meta.fields if field.name != 'id']
            csv_header = reader.fieldnames
            if csv_header != model_fields:
                raise DataError(f"CSV header doesn't match with the {model_name} table fields. ")

            for row in reader:
                model.objects.create(**row)
    
        # Print a success message after data insertion
        self.stdout.write(self.style.SUCCESS('Data Imported from CSV successfully !'))
