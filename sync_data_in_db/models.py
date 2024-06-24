from __future__ import annotations

import json

from django.db import models
from django.db.models import QuerySet

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


class CompanyManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def get_last(self) -> Company | None:
        return self.get_queryset().order_by("-id").first()

    def update_old_companies(self, but: BitrixUserToken) -> list[dict[str, str]]:
        last_company_in_db = self.get_last()
        id_last_company = "0" if not last_company_in_db else last_company_in_db.id
        companies_api_get = but.call_list_method(
                "crm.company.list", {"FILTER": {"<=ID": id_last_company}}
            )
        companies = {
            item["ID"]: item
            for item in companies_api_get
        }
        companies_obj = [
            Company(id=id_, data=json.dumps(data, ensure_ascii=False))
            for id_, data in companies.items()
        ]
        if companies_obj:
            self.bulk_update(companies_obj, ["data"])
        return companies_api_get

    def add_new_companies(self, but: BitrixUserToken) -> list[dict[str, str]]:
        last_company_in_db = self.get_last()
        id_last_company = "0" if not last_company_in_db else last_company_in_db.id
        companies_api_get = but.call_list_method(
                "crm.company.list", {"FILTER": {">ID": id_last_company}}
            )
        companies = {
            item["ID"]: item
            for item in companies_api_get
        }
        companies_obj = [
            Company(id=id_, data=json.dumps(data, ensure_ascii=False))
            for id_, data in companies.items()
        ]
        if companies_obj:
            self.bulk_create(companies_obj)
        return companies_api_get


class Company(models.Model):
    id = models.IntegerField(primary_key=True, null=False, unique=True)
    data = models.JSONField()

    custom_objects = CompanyManager()

    class Meta:
        db_table = "companies"
