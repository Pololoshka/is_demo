from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from integration_utils.bitrix24.models import BitrixUserToken
from move_task.utils import find_new_deadline_task, get_current_task_info

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def move_task_auth_user(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return render(request=request, template_name="placement_form.html")

    task_id = request.POST.get("task_id")
    but = BitrixUserToken.objects.filter(user__is_admin=True, is_active=True).first()
    current_task_info = get_current_task_info(task_id=task_id, but=but)
    new_deadline_str = find_new_deadline_task(current_task_info=current_task_info)

    if not new_deadline_str:
        return render(
            request=request,
            template_name="placement_form.html",
            context={"not_deadline": True, "task_id": task_id},
        )

    but.call_api_method(
        "tasks.task.update",
        {"taskId": task_id, "fields": {"DEADLINE": new_deadline_str}},
    )

    return render(request, "placement_form.html", {"task_id": task_id})
