from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from datetime import datetime
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from integration_utils.its_utils.app_get_params import get_params_from_sources
from integration_utils.its_utils.app_get_params.decorators import expect_param

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def form(request: HttpRequest) -> HttpResponse:
    return render(request=request, template_name="form_select.html")


@main_auth(on_cookies=True)
@get_params_from_sources
@expect_param("user_id", coerce=str)
def select_user(request: HttpRequest, user_id: str) -> HttpResponse:
    if request.method != "POST":
        return render(request=request, template_name="form_select.html")
    but = request.bitrix_user_token  # type: ignore
    user_info = but.call_api_method("user.get", {"ID": user_id})["result"][0]

    user_info["DATE_REGISTER"] = datetime.fromisoformat(
        user_info["DATE_REGISTER"]
    ).strftime("%d.%m.%Y")
    if dr := user_info["PERSONAL_BIRTHDAY"]:
        user_info["PERSONAL_BIRTHDAY"] = datetime.fromisoformat(dr).strftime("%d.%m.%Y")

    return render(
        request=request,
        template_name="form_select.html",
        context={"user_info": user_info},
    )
