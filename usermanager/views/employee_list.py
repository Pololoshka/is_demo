from django.shortcuts import render
from ..utils.search_manager import search_manager
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def employee_list(request):
    but = request.bitrix_user_token
    user_dict = search_manager(but)

    user_info = None

    if request.GET.get('user_id'):
        user_id = request.GET.get('user_id')
        user_info = {
            'FULL_NAME': user_dict[user_id]['FULL_NAME'],
            'SUPERVISORS': user_dict[user_id]['SUPERVISORS']
        }

    return render(request, 'list.html', context={'users': user_dict, 'user_info': user_info})
