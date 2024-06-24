from django.db import models
from django.db.models.query import QuerySet


class BPManager(models.Manager):
    def get_queryset(self) -> QuerySet:
        return super().get_queryset()

    def update_few(self, business_processes: dict) -> None:
        for process in business_processes:
            self.update_or_create(
                process_id=process["ID"], defaults={"process_name": process["NAME"]}
            )


class BusinessProcessModel(models.Model):
    process_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    objects = models.Manager()
    custom_objects = BPManager()

    class Meta:
        db_table = "business_processes"

    def __str__(self):
        return f"Бизнес процесс {self.id} - {self.name}"
