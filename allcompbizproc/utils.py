from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


def get_id_companies(but: BitrixUserToken) -> list[dict[str, str]]:
    return but.call_list_method("crm.company.list", {"select": ["ID"]})


def get_business_processes(but: BitrixUserToken) -> list[dict[str, str]]:
    return but.call_list_method(
        "bizproc.workflow.template.list",
        {
            "select": ["ID", "NAME"],
            "filter": {"DOCUMENT_TYPE": ["crm", "CCrmDocumentCompany", "COMPANY"]},
        },
    )


def run_business_processes(but: BitrixUserToken, process_id: str, company_id: str):
    but.call_api_method(
        "bizproc.workflow.start",
        {
            "TEMPLATE_ID": process_id,
            "DOCUMENT_ID": ["crm", "CCrmDocumentCompany", company_id],
        },
    )
