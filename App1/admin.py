from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered

app_models = apps.get_models()

EXCLUDE_APPS = ['token_blacklist']  # apps to skip

for model in app_models:
    # skip models from excluded apps
    if model._meta.app_label in EXCLUDE_APPS:
        continue
    try:
        admin.site.register(model)
    except AlreadyRegistered:
        pass
