from __future__ import annotations

from pathlib import Path

from django.http import FileResponse
from django.shortcuts import render

from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth
from product_list_excel.utils import save_file

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpResponse, HttpRequest

@main_auth(on_cookies=True)
def product_in_excel(request: HttpRequest) -> FileResponse | HttpResponse:
    but = request.bitrix_user_token
    if request.method == 'POST':
        products = but.call_list_method('crm.product.list')
        file_path = Path(__file__).parent / 'files' / 'example.xlsx'
        save_file(products=products, file_path=file_path)
        return FileResponse(file_path.open(mode="rb"), as_attachment=True)

    return render(request, 'productexcellist.html', locals())
