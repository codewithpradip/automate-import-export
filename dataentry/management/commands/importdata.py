from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
import csv
from django.db.utils import DataError
from dataentry.utils import check_csv_error

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

        model = check_csv_error(file_path, model_name)
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                model.objects.create(**row)
    
        # Print a success message after data insertion
        self.stdout.write(self.style.SUCCESS('Data Imported from CSV successfully !'))
