from django.shortcuts import render,HttpResponse
from dataentry.tasks import celery_test_task
from django.conf import settings
from django.core.mail import EmailMessage

def home(request):
    return render(request, 'dashboard.html')

def celery_test(request):
# I want to execute a time consuming task here
    celery_test_task.delay()

    return HttpResponse('<h3>Function executed successfully</h3>')
