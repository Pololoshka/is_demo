from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from duplicatefinder.models_data import MODELS_DATA

if TYPE_CHECKING:
    from integration_utils.bitrix24.models import BitrixUserToken


def find_duplicates(but: BitrixUserToken, selected_model: str) -> dict[str, int]:
    counter_value = defaultdict(int)
    objects = but.call_list_method(f'crm.{selected_model}.list')
    for obj in objects:
        counter_value[obj[MODELS_DATA[selected_model]['fields']]] += 1
    return {name: count for name, count in counter_value.items() if count > 1}
