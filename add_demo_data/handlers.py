from __future__ import annotations

import os
from typing import TYPE_CHECKING

import requests
from pathlib import Path

import settings
import add_demo_data.utils as u
from calls_registration.models.telephony_call_info import TelephonyCallInfo

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


def load_leads(data: dict, but: BitrixUserToken, *args, **kwargs) -> None:
    u.load_in_crm(crm_items=data, but=but, type_id=1)


def load_deals(data: dict, but: BitrixUserToken, *args, **kwargs) -> None:
    u.load_in_crm(crm_items=data, but=but, type_id=2)


def load_calls(data: dict, but: BitrixUserToken, *args, **kwargs) -> None:
    for call_item in data:
        # Загрузка звонка в БД
        call = TelephonyCallInfo(
            user_phone_inner=call_item["user_phone"],
            user_id=int(call_item["user_id"]),
            phone_number=call_item["phone_number"],
            call_date=call_item["call_date"],
            type=int(call_item["type"]),
            add_to_chat=int(call_item["add_to_chat"])
        )
        call.save()

        # Чтение файла звонка
        call_file = requests.get(
            url="https://drive.google.com/uc?id=" + call_item["file"].split("/")[-2] + "&export=download",
            allow_redirects=True,
        )

        file_path = os.path.join('rings/', str(call.id) + '.mp3')
        with open((Path(settings.MEDIA_ROOT) / file_path), 'wb') as file:
            file.write(call_file.content)

        call.file.name = file_path
        call.save()

        # Выгрузка звнока в Битрикс24
        call.telephony_externalcall_register(but)
        call.telephony_externalcall_finish(but)
        call.telephony_externalcall_attachrecord(but)


def load_companies(data: dict, but: BitrixUserToken, origin_id_prefix: float) -> None:
    company_data = u.add_origin_prefix(data, origin_id_prefix)
    u.load_in_crm(crm_items=company_data, but=but, type_id=4)

    companies_origin_id_dict = u.get_companies_origin_id(but=but, origin_id_prefix=origin_id_prefix)
    for d in company_data:
        # https://dev.1c-bitrix.ru/rest_help/crm/requisite/methods/crm_address_add.php
        but.call_api_method("crm.address.add", {"fields": {
            "TYPE_ID": "1",
            "ENTITY_TYPE_ID": "4",  # 4 - для Компаний
            "ENTITY_ID": companies_origin_id_dict[d['ORIGIN_ID']]['ID'],
            "CITY": d["ADDRESS_CITY"],
            "ADDRESS_1": d["ADDRESS"],
        }})


def load_contacts(data: dict, but: BitrixUserToken, origin_id_prefix: float) -> None:
    companies_origin_id_dict = u.get_companies_origin_id(but=but, origin_id_prefix=origin_id_prefix)

    contacts_data = u.add_origin_prefix(data, origin_id_prefix)
    contacts_data = u.make_links_from_origin(contacts_data,
                                             'COMPANY_ORIGIN_ID',
                                             'COMPANY_ID',
                                             companies_origin_id_dict,
                                             origin_id_prefix)
    for c in contacts_data:
        c["PHONE"] = [{"VALUE": str(c["PHONE"]), "VALUE_TYPE": "WORK"}]

    u.load_in_crm(crm_items=contacts_data, but=but, type_id=3)
