from datetime import datetime as dt
import pandas as pd
from pathlib import Path


def save_file(products: list[dict[str, str]], file_path: Path) -> None:
    products_data = pd.DataFrame(products)
    products_data.to_excel(
        excel_writer=file_path,
        index=False,
        columns=["ID", "NAME", "CODE", "CATALOG_ID", "PRICE", "CURRENCY_ID"],
        header=["ID", "Наименование", "Код товара", "Номер католога", "Цена", "Валюта"],
    )
