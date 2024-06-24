from django.urls import path

from move_task.views import move_task_auth_user, move_personal_task, form

urlpatterns = [
    path("auth_user/", move_task_auth_user, name="auth_user"),
    path("personal/", move_personal_task, name="personal"),
    path("", form),
]
