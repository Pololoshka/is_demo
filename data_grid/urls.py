from django.urls import path

from data_grid.views import show_grid

urlpatterns = [
    path("form/", show_grid),
]
