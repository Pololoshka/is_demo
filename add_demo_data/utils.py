from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


def make_links_from_origin(data: dict, excel_field: str, b24_field: str, source_map: dict, prefix: float) -> dict:
    """
    Принимает список из листов excel
    заменяет excel_field=COMPANY_ORIGIN_ID на b24_field=COMPANY_ID, учитывая предыдущую замену при импорте демоданных
    для создания правльной адресации на только что созданные сущности
    """

    for d in data:
        # Добавляем префикс для ORIGIN_ID
        if d.get(excel_field):
            d[b24_field] = \
                source_map["{}_{}".format(prefix, d.get(excel_field))]['ID']
    return data


def add_origin_prefix(data: dict, prefix: float) -> dict:
    """
    В файле excel делаем связку между страницами по полю ORIGIN_ID, т.к при импорте в Б24 мы получим новые ID сущностей.
    Эта функция помогает делать уникальные ORIGIN_ID для единовремнного импорта демоданных
    для всех записей добавляет префикс (Мы его возьмем как текущее время с микросекундами)
    у все записей "10" стенет "1690205018.084936_10"
    :param data:
    :param prefix:
    :return:
    """
    for d in data:
        # Добавляем префикс для ORIGIN_ID
        if origin_id := d.get('ORIGIN_ID'):
            d['ORIGIN_ID'] = f"{prefix}_{origin_id}"
    return data


def load_in_crm(crm_items: dict, but: BitrixUserToken, type_id: int) -> None:
    methods = []
    for item in crm_items:
        methods.append(('crm.item.batchImport',
                        {"entityTypeId": str(type_id), "data": [item]}))
    but.batch_api_call(methods)


def get_companies_origin_id(but: BitrixUserToken, origin_id_prefix: float) -> dict[str, str]:
    companies = but.call_list_method('crm.company.list', {
        "SELECT": ["ORIGIN_ID", "ID"],
        "FILTER": {"%ORIGIN_ID": f"{origin_id_prefix}_"}})
    return {item['ORIGIN_ID']: item for item in
            companies}
