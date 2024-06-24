from django.urls import path

from .views import describe_company_model

urlpatterns = [
    path('fields/', describe_company_model),
]
