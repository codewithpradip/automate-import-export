import csv
from django.core.management import BaseCommand, CommandError
from django.apps import apps
import datetime


# Custom management command - python manage.py exportdata model_name
class Command(BaseCommand):
    help="Export data from database to a CSV file."

    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Name of the model')

    # Executed when the command Run
    def handle(self, *args, **kwargs):
        model_name = kwargs['model_name'].capitalize()

        model= None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break # Stop to search once model is found
            except LookupError:
                continue # Continue searching in next app, if model not found in this app
        
        if not model:
            raise CommandError(f'Model {model_name} not found in any app!')
        

        # Fetch the data form database
        data = model.objects.all()

        # generate timestap of the current Data/Time
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
        # Define the csv file name/path
        file_path = f'exported_{model_name}_data_{timestamp}.csv'

        # Open the csv file and write the data
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            
            # write the CSV header
            writer.writerow([ field.name for field in model._meta.fields])
            
            # write data row
            for dt in data:
                writer.writerow([getattr(dt, field.name) for field in model._meta.fields])

        self.stdout.write(self.style.SUCCESS('Data Exported successfully'))