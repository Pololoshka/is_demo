from usermanager.utils.handlers import get_users, get_departments, add_supervisors_to_user


def search_manager(but):
    """Осуществляет поиск начальника для пользователя."""

    users = get_users(but=but)
    departments = get_departments(but=but)

    # Проходимся по всем юзерам, для каждого ищем руководителей.

    add_supervisors_to_user(users=users, departments=departments)

    return users
