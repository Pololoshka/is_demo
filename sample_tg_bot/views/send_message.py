from __future__ import annotations

from django.shortcuts import render

from integration_utils.vendors.telegram import Bot
import settings
from typing import TYPE_CHECKING

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from integration_utils.its_utils.app_get_params import get_params_from_sources
from integration_utils.its_utils.app_get_params.decorators import expect_param
from integration_utils.vendors.telegram.error import Unauthorized

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def send_message_form(request):
    return render(request, "msg_input.html", context={"result": None})


@main_auth(on_cookies=True)
@get_params_from_sources
@expect_param("chat_id", coerce=str)
@expect_param("message_text", coerce=str)
def send_message(
    request: HttpRequest,
    chat_id: str,
    message_text: str,
) -> HttpResponse:
    if request.method != "POST":
        return render(
            request=request,
            template_name="msg_input.html",
            context={"result": None, "error": None},
        )
    bot = Bot(token=settings.TELEGRAM_TOKEN)
    try:
        bot.send_message(text=message_text, chat_id=chat_id)
        return render(
            request=request,
            template_name="msg_input.html",
            context={
                "result": f"Бот {settings.TELEGRAM_BOT_NAME} отправил сообщение: '{message_text}' в чат {chat_id}",
                "error": None,
            },
        )
    except Unauthorized:
        return render(
            request=request,
            template_name="msg_input.html",
            context={
                "result": None,
                "error": "Не удалось найти чат. Проверьте правильность написания ID чата",
            },
        )
