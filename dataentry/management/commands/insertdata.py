from django.core.management.base import BaseCommand
from dataentry.models import Student

class Command(BaseCommand):
    help = "It will insert CSV data into database"

    def handle(self, *args, **kwargs):

        dataset = [
            {'roll_no':1002, 'name':'sita', 'age':20},
            {'roll_no':1003, 'name':'ram', 'age':22},
            {'roll_no':1004, 'name':'kamal', 'age':25},
            {'roll_no':1005, 'name':'janak', 'age':27},
        ]

        for data in dataset:
            Student.objects.create(roll_no=data['roll_no'], name=data['name'], age=data['age'])

        self.stdout.write(self.style.SUCCESS('Data inserted successfully !'))