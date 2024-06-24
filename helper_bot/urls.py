from django.urls import path

from helper_bot.views import process_the_request

urlpatterns = [
    path('handler/', process_the_request),
]
