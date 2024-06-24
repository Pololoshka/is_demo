from __future__ import annotations

from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from typing import TYPE_CHECKING

from sync_data_in_db.handlers import handler_companies
from sync_data_in_db.models import Company

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def form(request):
    return render(request, "sync_data_app.html")


@main_auth(on_cookies=True)
def create_data(request: HttpRequest) -> HttpResponse:
    but = request.bitrix_user_token  # type: ignore
    result = Company.custom_objects.add_new_companies(but=but)
    json_companies = handler_companies(but=but, companies=result)

    return render(
        request, template_name="sync_data_app.html", context={"create": len(result), "json_company_list": json_companies}
    )


@main_auth(on_cookies=True)
def update_data(request: HttpRequest) -> HttpResponse:
    but = request.bitrix_user_token  # type: ignore
    result = Company.custom_objects.update_old_companies(but=but)
    json_companies = handler_companies(but=but, companies=result)
    return render(
        request, template_name="sync_data_app.html", context={"update": len(result), "json_company_list": json_companies}
    )
