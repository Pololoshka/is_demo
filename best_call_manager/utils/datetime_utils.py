from datetime import datetime


def get_now_date() -> str:
    """Позволяет получить сегодняшнюю дату в iso-формате (дата динамическая,
    время всегда 00:00:00, для того, чтобы получать задачи всего дня)"""

    current_datetime = datetime.now().replace(
        hour=0, minute=0, second=0, microsecond=0,
    )
    return current_datetime.isoformat()


def parse_date(date_str: str) -> str:
    """Позволяет распарсить дату в удобочитаемом формате"""

    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%d %b %Y, %H:%M:%S")


def parse_date_in_dmy(date_str: str) -> str:
    """Позволяет преобразовать дату: в d/m/y"""

    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%d/%m/%Y")
