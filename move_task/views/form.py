from __future__ import annotations

import json
from typing import TYPE_CHECKING

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_start=True, set_cookie=True)
def form(request: HttpRequest) -> HttpResponse:
    task_id = int(json.loads(request.POST["PLACEMENT_OPTIONS"])["taskId"])
    return render(
        request=request,
        template_name="placement_form.html",
        context={"task_id": task_id},
    )
