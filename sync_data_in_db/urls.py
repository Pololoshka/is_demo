from django.urls import path

from sync_data_in_db.views import form, update_data, create_data

urlpatterns = [
    path('form/', form),
    path('update_data/', update_data, name='update_data'),
    path('create_data/', create_data, name='create_data'),
]
