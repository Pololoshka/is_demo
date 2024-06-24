from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from calls_to_telegram.utils.main_utils import is_export_calls_to_telegram


@main_auth(on_cookies=True)
def export_calls(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return render(request, "send_button_page.html")
    but = request.bitrix_user_token  # type: ignore

    bot_token = request.POST.get("bot_token")
    calls_chat_id = request.POST.get("calls_chat_id")

    if is_export_calls_to_telegram(but, bot_token, calls_chat_id):
        return HttpResponse("Calls exported successfully.")
    else:
        return HttpResponse("No calls to export.")

