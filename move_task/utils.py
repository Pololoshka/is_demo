from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import datetime, timedelta

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


def get_current_task_info(but: BitrixUserToken, task_id: int) -> dict[str, str]:
    return but.call_api_method(
        "tasks.task.get", {"taskId": task_id, "select": ["CREATED_BY", "DEADLINE"]}
    )["result"]["task"]


def find_new_deadline_task(current_task_info: dict[str, str]) -> str | None:
    current_deadline = current_task_info["deadline"]
    if current_deadline is None:
        return None

    new_deadline = datetime.fromisoformat(current_deadline) + timedelta(days=1)
    return datetime.isoformat(new_deadline)
