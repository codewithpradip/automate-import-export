from django.apps import apps

def get_all_custom_model():
    exclude_model = ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'Upload']
    include_model = []
    for model in apps.get_models():
        if model.__name__ not in exclude_model:
            include_model.append(model.__name__)
    return include_model