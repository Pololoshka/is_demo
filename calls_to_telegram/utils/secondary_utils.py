from integration_utils.bitrix24.exceptions import BitrixApiError
from django.conf import settings
from dateutil.parser import parse

CALLS_TYPES = {
    '1': 'Исходящий звонок',
    '2': 'Входящий звонок',
    '3': 'Входящий с перенаправлением (на мобильный или стационарный телефон)',
    '4': 'Обратный звонок',
    None: 'Нет данных'
}


# Возвращает id всех юзеров
def get_users(but):
    users = but.call_list_method('user.get', {'ADMIN_MODE': True})
    users = {user['ID']: user for user in users}
    return users



# генерирует сообщение для отправки в тг
def create_message(call, users):
    start = parse(call['CALL_START_DATE'])
    msg = f"{CALLS_TYPES[call['CALL_TYPE']]}\n" \
          f"{start.strftime('%d.%m.%Y %H:%M:%S')}\n" \
          f"Номер {call['PHONE_NUMBER']} \n" \
          f"Менеджер: {get_user_name(users, call['PORTAL_USER_ID'])}\n" \
          f"{call['CRM_ENTITY_TYPE'].capitalize() if call['CRM_ENTITY_TYPE'] else 'Нет данных'}: "
    return msg


# Возвращает имена пользователей по id.
def get_user_name(users, user_id):
    user = users[user_id]
    name = f"{user['LAST_NAME']} {user['NAME']}".strip()
    return f"{name}\n(https://{settings.APP_SETTINGS.portal_domain}/company/personal/user/{user_id}/)"