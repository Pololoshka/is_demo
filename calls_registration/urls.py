from django.urls import path

from .views import register_telephony_call

urlpatterns = [
    path('registration/', register_telephony_call, name='register_telephony_call'),
]
