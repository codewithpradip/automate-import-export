from django.shortcuts import render,redirect
from  .utils import get_all_custom_model, check_csv_error
from uploads.models import Upload
from django.conf import settings
from django.contrib import messages
from .tasks import import_data_task

# Create your views here.


def import_data(request):
    if request.method == 'POST':
        file_path = request.FILES.get('file_path')
        model_name = request.POST.get('model_name')

        # Stor file into the Upload model before Import
        upload = Upload.objects.create(file_path=file_path, model_name=model_name)

        #Construct the full path of the CSV file
        relative_path = str(upload.file_path.url)
        base_url = str(settings.BASE_DIR)
        file_path = base_url+relative_path

        # Check for the CSV error
        try:
            check_csv_error(file_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect('import_data')


        """
         Handel import Data Task and Trigger the importdata custome command
        """
        import_data_task.delay(file_path, model_name)
        messages.success(request, 'Your data is being imported, you will be notified once it is done !')
        return redirect('import_data')
        

    else:
        all_models = get_all_custom_model()
        context = {
            'all_models' : all_models,
        }
    return render(request, 'dataentry/importdata.html', context)