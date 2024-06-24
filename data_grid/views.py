from __future__ import annotations

import json
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest
COMPANY_FIELD = [
    "ADDRESS",
    "ADDRESS_2",
    "ADDRESS_CITY",
    "ADDRESS_COUNTRY",
    "ADDRESS_COUNTRY_CODE",
    "ADDRESS_LEGAL",
    "ADDRESS_POSTAL_CODE",
    "ADDRESS_PROVINCE",
    "ADDRESS_REGION",
    "ASSIGNED_BY_ID",
    "BANKING_DETAILS",
    "COMMENTS",
    "COMPANY_TYPE",
    "CREATED_BY_ID",
    "CURRENCY_ID",
    "DATE_CREATE",
    "DATE_MODIFY",
    "EMAIL",
    "EMPLOYESS",
    "HAS_EMAIL",
    "HAS_PHONE",
    "ID",
    "IM",
    "INDUSTRY",
    "IS_MY_COMPANY",
    "LEAD_ID",
    "LOGO",
    "MODIFY_BY_ID",
    "OPENED",
    "ORIGINATOR_ID",
    "ORIGIN_ID",
    "ORIGIN_VERSION",
    "PHONE",
    "REG_ADDRESS",
    "REG_ADDRESS_2",
    "REG_ADDRESS_CITY",
    "REG_ADDRESS_COUNTRY",
    "REG_ADDRESS_COUNTRY_CODE",
    "REG_ADDRESS_LEGAL",
    "REG_ADDRESS_POSTAL_CODE",
    "REG_ADDRESS_PROVINCE",
    "REG_ADDRESS_REGION",
    "REVENUE",
    "TITLE",
    "UTM_CAMPAIGN",
    "UTM_CONTENT",
    "UTM_MEDIUM",
    "UTM_SOURCE",
    "UTM_TERM",
    "WEB",
]


@main_auth(on_cookies=True)
def show_grid(request: HttpRequest) -> HttpResponse:
    """Позволяет вывести список компаний."""

    but = request.bitrix_user_token  # type: ignore
    companies = but.call_list_method("crm.company.list")

    users = but.call_list_method("user.get")
    users_dict = {user["ID"]: user for user in users}

    leads = but.call_list_method(
        "crm.lead.list", {"select": ["ID", "NAME", "LAST_NAME"]}
    )
    leads_dict = {lead["ID"]: lead for lead in leads}

    STATUS = {"Y": "Указано", "N": "Не указано"}

    for company in companies:
        # добавляем отсутствующие поля
        for key in COMPANY_FIELD:
            company.setdefault(key, "")

        # добавляем, с каким пользователем связано
        company.setdefault("ASSIGNED_BY", "")
        if assigned_id := company["ASSIGNED_BY_ID"]:
            name = users_dict[assigned_id]["NAME"]
            last_name = users_dict[assigned_id]["LAST_NAME"]
            company["ASSIGNED_BY"] = f"{name} {last_name}"

        # добавляем, кем создана компания
        company.setdefault("CREATED_BY", "")
        if created_id := company["CREATED_BY_ID"]:
            name = users_dict[created_id]["NAME"]
            last_name = users_dict[created_id]["LAST_NAME"]
            company["CREATED_BY"] = f"{name} {last_name}"

        # добавляем, кто последним изменял компанию
        company.setdefault("MODIFY_BY", "")
        if modify_id := company["MODIFY_BY_ID"]:
            name = users_dict[modify_id]["NAME"]
            last_name = users_dict[modify_id]["LAST_NAME"]
            company["MODIFY_BY"] = f"{name} {last_name}"
        # добавляем лида, связанного с компанией

        company.setdefault("LEAD_NAME", "")
        if lead_id := company["LEAD_ID"]:
            name = leads_dict[lead_id]["NAME"]
            last_name = leads_dict[lead_id]["LAST_NAME"]
            company["LEAD_NAME"] = f"{name} {last_name}"

        # добавляем полный адрес
        company.setdefault("FULL_ADDRESS", "")
        if address_city := company["ADDRESS_CITY"]:
            company["FULL_ADDRESS"] += f"{address_city}, "
        if address := company["ADDRESS"]:
            company["FULL_ADDRESS"] += f"{address}"

        # форматируем дату создания компании
        if date_create := company["DATE_CREATE"]:
            company["DATE_CREATE"] = datetime.fromisoformat(date_create).strftime(
                "%d.%m.%Y"
            )
        # форматируем дату изменения компании
        if date_modify := company["DATE_MODIFY"]:
            company["DATE_MODIFY"] = datetime.fromisoformat(date_modify).strftime(
                "%d.%m.%Y"
            )

        # добавляем статусы
        company["HAS_EMAIL"] = STATUS[company["HAS_EMAIL"]]
        company["HAS_PHONE"] = STATUS[company["HAS_PHONE"]]

    json_company_list = json.dumps(companies, cls=DjangoJSONEncoder)

    return render(
        request,
        "gridform.html",
        context={
            "json_company_list": json_company_list,
        },
    )
