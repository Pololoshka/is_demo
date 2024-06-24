from django.urls import path

from crmfields.views.reload import reload_start
from duplicatefinder.views import find_duplicates_for_models

urlpatterns = [
    path('finded_duplicates/', find_duplicates_for_models, name='find_duplicates'),
    path('', reload_start, name='reload_start'),
]
