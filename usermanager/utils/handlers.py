from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


def get_users(but: BitrixUserToken) -> dict[str, dict[str, Any]]:
    users = but.call_list_method("user.get")
    user_fields = ["NAME", "LAST_NAME", "SECOND_NAME", "UF_DEPARTMENT"]
    user_dict = {}
    for user in users:
        user_dict.update({user["ID"]: {}})
        for field in user_fields:
            try:
                user_dict[user["ID"]].update({field: user[field]})
            except KeyError:
                pass
        user_dict[user["ID"]].update({"SUPERVISORS": dict()})
    for user_id, user_ in user_dict.items():
        conj_str = ""
        for key in ["LAST_NAME", "NAME", "SECOND_NAME"]:
            try:
                conj_str += f"{user_[key]} "
            except KeyError:
                pass
        conj_str += f"| ID: {user_id}"
        user_.update({"FULL_NAME": conj_str})
    return user_dict


def get_departments(but: BitrixUserToken) -> dict[str, dict[str, Any]]:
    departments = but.call_list_method('department.get')
    departments_dict = {}
    for element in departments:
        departments_dict.update({element['ID']: element})
        departments_dict[element['ID']].pop('ID')
    return departments_dict




def add_supervisors_to_user(users: dict[str, dict[str, Any]], departments: dict[str, dict[str, Any]]) -> None:
    for user_id, user in users.items():

        for department_id, department in departments.items():
            #  Смотрим, состоит ли человек в текущем подразделении.
            #  Если состоит, то в качестве кого?
            if department.get('UF_HEAD') == user_id:
                supervisor_id, order = None, None
                if "PARENT" in department:
                    senior_department_id = department['PARENT']
                    supervisor_id, order = find_supervisor(departments_dict=departments, current_dep=senior_department_id, order=1)

            else:
                if int(department_id) not in user['UF_DEPARTMENT']:
                    continue
                current_department_id = department_id
                supervisor_id, order = find_supervisor(departments, current_department_id)

            #  В функцию поиска передается родительское подразделение, если в текущем
            #   юзер является руководителем. В ином случае передается текущее.

            if supervisor_id:
                supervisor = users[supervisor_id]
                conj_str = ""
                for key in ['LAST_NAME', 'NAME', 'SECOND_NAME']:
                    try:
                        conj_str += f'{supervisor[key]} '
                    except KeyError:
                        pass
                conj_str += f"| ID: {supervisor_id} | Порядок: {order}"
                user['SUPERVISORS'].setdefault(department['NAME'], (supervisor_id, conj_str))


def find_supervisor(departments_dict: dict[str, dict[str, Any]], current_dep: str = '1', order: int = 0) -> tuple[str, int]:
    """Рекурсивая функция, осуществляющая поиск начальника, если в настоящем
    подразделении он не был найден."""

    department = departments_dict[current_dep]
    parent_exists = ('PARENT' in department)
    supervisor = department.get('UF_HEAD')
    supervisor_exists = (supervisor and (supervisor != '0'))

    if supervisor_exists:
        return department['UF_HEAD'], order
    else:
        if not parent_exists:
            return "None", order
        return find_supervisor(departments_dict, department['PARENT'], order + 1)
