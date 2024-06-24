from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.its_utils.app_get_params import get_params_from_sources
from integration_utils.its_utils.app_get_params.decorators import expect_param
from sort_field_values.utils import sort_by_name

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def form_sort_field_values(request: HttpRequest):
    return render(
        request=request,
        template_name="form_for_sort_field.html",
        context={"result": ""},
    )


@main_auth(on_cookies=True)
@get_params_from_sources
@expect_param("field_name", coerce=str)
def sort_field_values(request: HttpRequest, field_name: str) -> HttpResponse:
    if request.method != "POST":
        return render(
            request=request,
            template_name="form_for_sort_field.html",
            context={"result": ""},
        )
    but = request.bitrix_user_token  # type: ignore

    field_values = but.call_list_method(
        "crm.company.userfield.list", {"FILTER": {"FIELD_NAME": field_name}}
    )
    if not field_values:
        return render(
            request=request,
            template_name="form_for_sort_field.html",
            context={
                "result": "Поля с таким названием не существует. Проверьте правильность написания имени поля. Имя поля должна начинаться с UF_CRM_"
            },
        )

    field_values = field_values[0]

    but.call_list_method(
        "crm.company.userfield.update",
        {
            "ID": field_values["ID"],
            "FIELDS": {"LIST": sort_by_name(data=field_values["LIST"])},
        },
    )
    return render(
        request=request,
        template_name="form_for_sort_field.html",
        context={"result": f"Значения списочного поля {field_name} отсортированы."},
    )
