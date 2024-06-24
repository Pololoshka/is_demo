from __future__ import annotations

import time
from typing import TYPE_CHECKING

import pandas as pd

from django.shortcuts import render

import add_demo_data.handlers as h
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from integration_utils.its_utils.app_get_params import get_params_from_sources
from integration_utils.its_utils.app_get_params.decorators import expect_param

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest

ACTION_TYPES = {
    'Компании': h.load_companies,
    'Контакты': h.load_contacts,
    'Сделки': h.load_deals,
    'Лиды': h.load_leads,
    'Звонки': h.load_calls,
}


@main_auth(on_cookies=True)
# достает из GET, POST, json тела парметры
@get_params_from_sources
@expect_param('link', coerce=str)
def load_demo_data(request: HttpRequest, link: str) -> HttpResponse:
    but = request.bitrix_user_token
    origin_id_prefix: float = time.time()
    result = {}
    # Ожидаем что люди нам будут скармливать ссылки типа https://docs.google.com/spreadsheets/d/1ZuKXEK0hwJyxFwGxoi77G0PaOh4Qg4SDZBNkHDws2iU/edit#gid=1891471437
    # а нам нужно вместо edit, делать export
    export_link = "/".join(link.split("/")[0:-1]) + "/export"
    dict_df = pd.read_excel(export_link, sheet_name=None)
    for df_name, df in dict_df.items():
        data = df.to_dict('records')
        ACTION_TYPES[df_name](data=data, but=but, origin_id_prefix=origin_id_prefix)
        result[df_name] = len(data)

    return render(request, template_name='loaddemodata.html', context={'result': result})
