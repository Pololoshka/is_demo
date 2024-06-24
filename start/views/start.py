from django.shortcuts import render
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from django.conf import settings

from integration_utils.its_utils.app_get_params import get_params_from_sources


@main_auth(on_start=True, set_cookie=True)
@get_params_from_sources
def start(request):
    app_settings = settings.APP_SETTINGS
    return render(request, 'start_page.html', locals())
