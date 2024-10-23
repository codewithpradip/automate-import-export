
from automate_import_export_main.celery import app
import time

@app.task
def celery_test_task():
    time.sleep(5) 
    return 'Task Completed successfully.'