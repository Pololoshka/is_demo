import html
from django.shortcuts import render
from best_call_manager.utils.table_creation import get_html_row, get_html_table
import best_call_manager.utils.api_methods as api_methods
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def find_finish_task(request):
    """Позволяет собрать все результаты завершенных задач. Создает группу
    если она не существует, а если существует берет ее id. По результату
    задач находит нужный звонок и делает пост с таблицей лучших звонков
    каждого менеджера."""

    if request.method == "POST":
        but = request.bitrix_user_token

        # Получаем информацию о группе с названием "Лучший звонок за день"  
        group = but.call_api_method("sonet_group.get", {"FILTER": {"NAME": "Лучший звонок за день"}})
        if group["result"]:
            group_id = group["result"][0]["ID"]
        else:
            group_id = api_methods.create_app_group(but)

        # Получаем все ID задач, связанных с текущим приложением
        app_tasks_id = but.call_list_method("app.option.get", {"option": "tasks"})
        if not app_tasks_id or app_tasks_id[0] == '':
            return render(request, 'best_call_manager_temp.html')

        # Переносим выполненные задачи из app_tasks_id в completed_tasks
        completed_tasks = dict()
        for app_task in api_methods.get_app_tasks(but, app_tasks_id):
            if app_task["status"] == '5':
                app_tasks_id.remove(app_task["id"])
                completed_tasks[app_task["id"]] = app_task

        if not completed_tasks:
            return render(request, 'best_call_manager_temp.html')

        possible_calls = but.call_api_method("app.option.get", {"option": "possible_calls"})["result"]

        calls = dict()
        for task_id, task in completed_tasks.items():
            task_res_all = but.call_api_method("tasks.task.result.list", {"taskId": task_id})["result"]
            if not task_res_all:
                app_tasks_id.append(task_id)
                comment = "Оставьте комментарий помеченный как результат"
                api_methods.resume_task(but=but, task_id=task_id, task=task, comment=comment)
                continue
            task_res = task_res_all[0]

            if isinstance(possible_calls, dict) and possible_calls.get(task_id):
                if task_res["text"] not in possible_calls[task_id]:
                    app_tasks_id.append(task_id)

                    comment = "Укажите корректный id звонка"
                    api_methods.resume_task(but=but, task_id=task_id, task=task, comment=comment)
                    continue
                else:
                    del possible_calls[task_id]

            calls[task_res["text"]] = task["responsible"]["name"]

        # Добавить ID задач, звонки в опциии текущего приложения
        but.call_api_method("app.option.set", {"options": {"tasks": app_tasks_id}})
        but.call_api_method("app.option.set", {"options": {"possible_calls": possible_calls}})

        # Получить все звонки с портала с заданными ID
        app_calls = api_methods.get_app_calls(but, list(calls.keys()))

        rows = ""
        for counter, app_call in enumerate(app_calls, 1):
            row = get_html_row(app_call, calls, counter)
            rows += row

        html_table = get_html_table(rows)
        api_methods.add_post(but, f"{html.unescape(html_table)}", [f"SG{group_id}"])

    return render(request, "best_call_manager_temp.html")
