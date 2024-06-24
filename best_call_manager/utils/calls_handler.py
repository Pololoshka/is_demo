from __future__ import annotations

import pandas as pd

from best_call_manager.utils import api_methods
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken
    from pandas.core.groupby.generic import DataFrameGroupBy
def get_call_type(call):
    """Позволяет распарсить тип звонка и вернуть пользователя описание типа
    звонка в строчном формате"""

    call_types = {
        '1': 'Исходящий',
        '2': 'Входящий',
        '3': 'Входящий с перенаправлением',
        '4': 'Обратный звонок',
    }

    return call_types[call]

def find_current_calls(but: BitrixUserToken, now_date: str) -> list[dict[str, str]] | None:
    info_option = but.call_api_method("app.option.get")["result"]
    if app_date := info_option.get("DATE_FROM_APP_BEST_CALL_MANAGER"):
        if app_date == now_date:
            return None
        calls = api_methods.get_new_calls(but, app_date, now_date)
    else:
        calls = api_methods.get_old_calls(but, now_date)
    return calls


def create_df_calls(calls: list[dict[str, str]]) -> DataFrameGroupBy:
    call_info_df = pd.DataFrame(
        columns=["CALL_ID", "MANAGER_ID", "PHONE_NUMBER",
                 "START_DATE", "START_DATETIME", "DURATION", "CALL_TYPE"])

    for call in calls:
        call_info_df.loc[len(call_info_df.index)] = [
            call["ID"],
            call["PORTAL_USER_ID"],
            call["PHONE_NUMBER"],
            call["CALL_START_DATE"][:10],
            call["CALL_START_DATE"],
            call["CALL_DURATION"],
            call["CALL_TYPE"]
        ]

    call_info_df.sort_values(by="START_DATETIME", inplace=True)
    return call_info_df.groupby(["MANAGER_ID", "START_DATE"])
