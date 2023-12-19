from django.apps import apps
from django.contrib import admin


def register_all_models(app_name: str):
    app_models = apps.get_models(app_name)

    for model in app_models:
        try:
            admin.site.register(model)
        except admin.sites.AlreadyRegistered:
            pass
