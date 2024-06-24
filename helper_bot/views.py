from __future__ import annotations

import json

import requests

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from django.http import HttpResponse

APPLICATION_TOKEN = "55c8de1904717c54fbfc3526d6b0b4cf"

TYPE_ACTION = {
    "хочу умную мысль": 4,
    "расскажи анекдот": 1,
}


@main_auth(on_start=True, set_cookie=True)
def process_the_request(request):
    if request.method != "POST":
        return HttpResponse("Only POST request is processed")

    if request.POST.get("auth[application_token]") != APPLICATION_TOKEN:
        return HttpResponse("Invalid auth token")

    but = request.bitrix_user_token
    if request.POST.get("event") == "ONIMBOTMESSAGEADD":
        message = request.POST.get("data[PARAMS][MESSAGE]")
        dialog_id = request.POST.get("data[PARAMS][DIALOG_ID]")
        m = message.strip().lower()

        if m in TYPE_ACTION:
            response_message = requests.get(
                f"http://rzhunemogu.ru/RandJSON.aspx?CType={TYPE_ACTION[m]}"
            )
            r = response_message.text.replace("\r\n", " ")
            but.call_list_method(
                "imbot.message.add",
                {
                    "BOT_ID": "25",
                    "DIALOG_ID": dialog_id,
                    "MESSAGE": json.loads(r)["content"],
                },
            )
        else:
            but.call_list_method(
                "imbot.message.add",
                {"BOT_ID": "25", "DIALOG_ID": dialog_id, "MESSAGE": message},
            )

    return HttpResponse("OK")
