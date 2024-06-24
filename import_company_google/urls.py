from django.urls import path

from import_company_google.views import import_company_google

urlpatterns = [
    path('import/', import_company_google, name="import_company_google"),
]
