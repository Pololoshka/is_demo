from __future__ import annotations

from best_call_manager.utils.calls_handler import create_df_calls
from best_call_manager.utils.table_creation import add_row, create_pretty_table
from best_call_manager.utils.api_methods import add_task
from best_call_manager.utils.datetime_utils import parse_date_in_dmy
from usermanager.utils.search_manager import search_manager

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


def setting_goals(but: BitrixUserToken, calls: list[dict[str, str]]):
    """Позволяет поставить задачи по выбору лучшего звонка пользователям."""

    users: dict = search_manager(but=but)
    managers: dict = dict()

    for manager_id, user in users.items():
        if user["SUPERVISORS"] == dict():
            managers[manager_id] = manager_id
        else:
            managers[manager_id] = next(iter(user["SUPERVISORS"]))[0]

    call_info_df = create_df_calls(calls=calls)

    table = create_pretty_table()
    possible_calls: dict = dict()

    for group, call_df in call_info_df:
        call_df.reset_index(drop=True, inplace=True)
        table.clear_rows()

        calls_for_task = []

        for index, row in call_df.iterrows():
            add_row(table=table, counter=index.__hash__() + 1, row=row)

            calls_for_task.append(row["CALL_ID"])

        task_id = add_task(but, group[0], managers[group[0]], table,
                           parse_date_in_dmy(group[1]))

        possible_calls[task_id] = calls_for_task

    return possible_calls
