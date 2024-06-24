from django.urls import path

from add_demo_data.views.form_demo_data import form_demo_data
from add_demo_data.views.load import load_demo_data

urlpatterns = [
    path('load_form/', form_demo_data, name='form_demo_data'),
    path('load/', load_demo_data, name='load_demo_data'),
]
