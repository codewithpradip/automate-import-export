from django.core.management.base import BaseCommand
from dataentry.models import Student

# Custom management command - python manage.py insertdata
class Command(BaseCommand):
    help = "It will insert CSV data into database"

    # The handle method is executed when the command is run
    def handle(self, *args, **kwargs):
        
        # Hardcoded dataset mimicking a CSV file structure
        dataset = [
            {'roll_no':1002, 'name':'sita', 'age':20},
            {'roll_no':1008, 'name':'ram', 'age':22},
            {'roll_no':10012, 'name':'kamal', 'age':25},
            {'roll_no':1025, 'name':'janak', 'age':27},
        ]

        for data in dataset:
            roll_no = data['roll_no']
            # Check if a student with the same roll number already exists
            existing_record = Student.objects.filter(roll_no=roll_no).exists()

            # If student doesn't exist, create a new record
            if not existing_record:
                Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])
            else:
                 # If the student already exists, print a warning message
                self.stdout.write(self.style.WARNING(f'Student with Roll No. {roll_no} already exist !'))

         # Print a success message after data insertion
        self.stdout.write(self.style.SUCCESS('Data inserted successfully !'))