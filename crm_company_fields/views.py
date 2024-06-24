from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def describe_company_model(request: HttpRequest) -> HttpResponse:
    but: BitrixUserToken = request.bitrix_user_token  # type: ignore
    company_fields: dict = but.call_list_method("crm.company.fields")  # type: ignore

    return render(request=request, template_name='describecompanymodel.html', context={"company_fields": company_fields},)
