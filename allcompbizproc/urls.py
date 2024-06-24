from django.urls import path

from allcompbizproc.views import run_business_process
from crmfields.views.reload import reload_start

urlpatterns = [
    path("run_business_process/", run_business_process, name="run"),
    path("", reload_start, name="reload_start"),
]
