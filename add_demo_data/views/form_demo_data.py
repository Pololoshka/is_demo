from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def form_demo_data(request):
    return render(request, 'loaddemodata.html', locals())
