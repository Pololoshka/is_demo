from django.urls import path

from .views.send_message import send_message, send_message_form

urlpatterns = [
    path("send_message_form/", send_message_form),
    path("send_message/", send_message, name="send_message"),
]
