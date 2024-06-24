from django.urls import path

from select_user.views import form, select_user

urlpatterns = [
    path("user/", form),
    path("info/", select_user, name="select_user"),
]
