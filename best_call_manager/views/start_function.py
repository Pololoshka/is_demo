from __future__ import annotations

from django.shortcuts import render

from best_call_manager.utils.datetime_utils import get_now_date
from best_call_manager.utils.calls_handler import find_current_calls
from best_call_manager.utils.setting_goals import setting_goals
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def start_find_all_call(request: HttpRequest) -> HttpResponse:
    """Позволяет получить все звонки, найти среди них подходящие по условию,
    и поставить пользователям задачу на выбор лучшего звонка за каждый день
    когда они были совершены, также пользователям в комментарии к задаче
    отправляется таблица с удобочитаемыми данными, чтобы пользователь смог
    проанализировать информацию и сделать выбор"""

    if request.method == "POST":
        but = request.bitrix_user_token  # type: ignore
        now_date = get_now_date()

        current_calls = find_current_calls(but=but, now_date=now_date)
        if not current_calls:
            return render(request, "best_call_manager_temp.html")

        possible_calls = setting_goals(but, current_calls)

        # Получаем все звонки в опциях текущего приложения
        app_possible_calls = but.call_api_method("app.option.get", {"option": "possible_calls"})["result"]
        if app_possible_calls and isinstance(app_possible_calls, dict):
            app_possible_calls.update(possible_calls)
        else:
            app_possible_calls = possible_calls

        # Получаем все ID задач, связанных с текущим приложением
        app_tasks_id = but.call_list_method("app.option.get", {"option": "tasks"})
        if app_tasks_id and app_tasks_id[0] != '':
            app_tasks_id.extend(possible_calls.keys())
        else:
            app_tasks_id = possible_calls.keys()

        # Добавить ID задач, звонки и обновить дату в опциях текущего приложения
        but.call_api_method("app.option.set", {"options": {"tasks": app_tasks_id}})
        but.call_api_method("app.option.set", {"options": {"possible_calls": app_possible_calls}})
        but.call_api_method("app.option.set", {"options": {"DATE_FROM_APP_BEST_CALL_MANAGER": now_date}})

    return render(request, "best_call_manager_temp.html")
