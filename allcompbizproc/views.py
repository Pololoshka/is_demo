from __future__ import annotations

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from allcompbizproc.forms import BusinessProcessForm
from allcompbizproc.models import BusinessProcessModel
from allcompbizproc.utils import (
    get_id_companies,
    get_business_processes,
    run_business_processes,
)
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest


@main_auth(on_cookies=True)
def run_business_process(request: HttpRequest) -> HttpResponse:
    but = request.bitrix_user_token
    companies_id = get_id_companies(but=but)
    business_processes = get_business_processes(but=but)
    BusinessProcessModel.custom_objects.update_few(
        business_processes=business_processes
    )
    if request.method == "POST":
        form = BusinessProcessForm(request.POST)
        if form.is_valid():
            cur_business_processes = form.cleaned_data["bp"]
            for company in companies_id:
                run_business_processes(
                    but=but,
                    company_id=str(company["ID"]),
                    process_id=cur_business_processes.process_id,
                )
            return HttpResponseRedirect(reverse("reload_start"))
    else:
        form = BusinessProcessForm()
    return render(request, "allcompbizproc.html", context={"form": form})
