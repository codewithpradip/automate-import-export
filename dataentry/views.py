from django.shortcuts import render,redirect
from  .utils import get_all_custom_model
from uploads.models import Upload
from django.conf import settings
from django.core.management import call_command
from django.contrib import messages

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

        # Trigger the importdata custom command
        try:
            call_command('importdata', file_path, model_name)
            messages.success(request, "Data imported successfully !")
        except Exception as e:
            messages.error(request, str(e))

        return redirect('import_data')
        

    else:
        all_models = get_all_custom_model()
        context = {
            'all_models' : all_models,
        }
    return render(request, 'dataentry/importdata.html', context)