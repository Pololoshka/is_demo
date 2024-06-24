from django.http import JsonResponse
from integration_utils.bitrix24.bitrix_user_auth.main_auth import main_auth


@main_auth(on_cookies=True)
def companies(request):
    """Возвращает JSON со списком компаний с известными адресами"""
    but = request.bitrix_user_token

    companies = {
        company["ID"]: company
        for company in but.call_list_method(
            "crm.company.list", {"select": ["ID", "TITLE"]}
        )
    }

    addresses = but.call_list_method(
        "crm.address.list",
        {
            "order": {"TYPE_ID": "ASC"},
            "select": ["ADDRESS_1", "CITY", "PROVINCE", "COUNTRY", "ANCHOR_ID"],
            "filter": {
                "ANCHOR_TYPE_ID": "4"  # 4  - значение для Компаний
            },
        },
    )

    if len(companies) == 0 or len(addresses) == 0:
        return JsonResponse({})

    companies_with_address = {}
    for address in addresses:
        comp_id = address["ANCHOR_ID"]
        if not companies.get(comp_id):
            continue

        comp = companies_with_address.setdefault(comp_id, {})
        comp.setdefault("addr", []).append(address)
        comp["title"] = companies[comp_id]["TITLE"]

    return JsonResponse(companies_with_address)
