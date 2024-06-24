from __future__ import annotations
from .forms import CallInfoForm

from typing import TYPE_CHECKING

from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def register_telephony_call(request: HttpRequest) -> HttpResponse:
    but = request.bitrix_user_token
    if request.method == 'POST':
        form = CallInfoForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            model.telephony_externalcall_register(but)
            model.telephony_externalcall_finish(but)
            model.telephony_externalcall_attachrecord(but)
    form = CallInfoForm()
    return render(request=request, template_name='registrationcall.html', context={'form': form})
