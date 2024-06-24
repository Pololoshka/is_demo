from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken
    from prettytable import PrettyTable


def add_task(but: BitrixUserToken, manager_id: str, supervisor_id: str, table: PrettyTable, date: str) -> str:
    """Позволяет поставить задачу пользователю от вышестоящего руководителя"""

    task_id = but.call_api_method("tasks.task.add",
                                  {"fields": {
                                      "TITLE": f"Оценить свой лучший звонок "
                                               f"за {date}",
                                      "CREATED_BY": supervisor_id,
                                      "RESPONSIBLE_ID": manager_id,
                                      "DESCRIPTION":
                                          f"[FONT=monospace]{table}[/FONT]"
                                          f"\n\n\nВ качестве результата этой "
                                          f"задачи напишите, пожалуйста, "
                                          f"ID звонка.",
                                      "TASK_CONTROL": 'N'
                                  }})["result"]["task"]["id"]

    return task_id


def get_new_calls(but: BitrixUserToken, date: str, now_date: str) -> list[dict[str, str]]:
    """Поозволяет получить все новые звонки с портала"""

    return but.call_list_method("voximplant.statistic.get",
                                {"FILTER": {
                                    "<CALL_START_DATE": now_date,
                                    ">=CALL_START_DATE": date
                                }})


def get_old_calls(but: BitrixUserToken, date: str) -> list[dict[str, str]]:
    """Поозволяет получить все звонки с портала"""

    return but.call_list_method("voximplant.statistic.get",
                                {"FILTER": {
                                    "<CALL_START_DATE": date
                                }})


def get_app_calls(but: BitrixUserToken, calls_id):
    """Позволяет получить все звонки с портала с заданными ID"""

    return but.call_list_method("voximplant.statistic.get", {
        "filter": {"ID": calls_id},
        "select": ["ID", "PHONE_NUMBER", "CALL_DURATION", "RECORD_FILE_ID",
                   "CALL_START_DATE", "CALL_TYPE"]
    })


def create_app_group(but: BitrixUserToken):
    """Позволяет создать на портале группу с названием
    "Лучший звонок за день" """

    group_id = but.call_api_method("sonet_group.create", {
        "NAME": "Лучший звонок за день", "VISIBLE": "Y",
        "OPENED": "Y"})["result"]
    return group_id


def get_app_tasks(but: BitrixUserToken, app_tasks_id):
    """Позволяет получить с портала задачи с указанными ID"""

    app_tasks = but.call_list_method("tasks.task.list", {
        "filter": {"ID": app_tasks_id},
        "select": ["ID", "TITLE", "STATUS", "RESPONSIBLE_ID",
                   "CREATED_DATE", "CREATED_BY"]})["tasks"]
    return app_tasks


def add_post(but: BitrixUserToken, message, dest):
    """Создает новый пост в заданной группе с указанным сообщением"""

    but.call_list_method("log.blogpost.add",
                         {"POST_TITLE": "Новые лучшие звонки",
                          "POST_MESSAGE": message,
                          "DEST": dest})


def resume_task(but: BitrixUserToken, task_id: str, task: dict, comment: str) -> None:
    """ Возобновляет задачy с указанным комментарием """

    but.call_api_method("tasks.task.renew", {"taskId": task_id})
    but.call_api_method("task.commentitem.add", {
        "TASKID": task_id,
        "FIELDS": {
            "AUTHOR_ID": task["createdBy"],
            "POST_MESSAGE": comment
        }
    })
