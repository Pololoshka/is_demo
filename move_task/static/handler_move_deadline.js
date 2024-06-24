function moveDeadline() {
    let current_task_id = document.getElementById("buttonJS").value;
    BX24.callMethod("tasks.task.get", {'taskId': current_task_id, 'fields': ["DEADLINE"]}, function (res) {
        let deadline = dayjs(res.answer.result.task['deadline']).add(1, 'day').format('DD.MM.YYYY HH:mm');
        BX24.callMethod("tasks.task.update", {'taskId': current_task_id, 'fields': {"DEADLINE": deadline.toString()}});
    })
}