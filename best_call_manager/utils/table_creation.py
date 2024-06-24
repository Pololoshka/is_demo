from prettytable import PrettyTable

from best_call_manager.utils.calls_handler import get_call_type
from best_call_manager.utils.datetime_utils import parse_date
from django.conf import settings
import pandas as pd


def create_pretty_table() -> PrettyTable:
    table = PrettyTable()
    table.field_names = ["№", "ID звонка", "Номер телефона",
                         "Дата и время звонка",
                         "Длительность звонка",
                         "Тип звонка"]
    return table


def add_row(table: PrettyTable, counter: int, row: pd.Series) -> None:
    """Позволяет добавить в таблицу строчку с нужными данными"""

    table.add_row([f'{counter}',
                   row.loc['CALL_ID'],
                   row.loc['PHONE_NUMBER'],
                   parse_date(row.loc['START_DATETIME']),
                   f"{row.loc['DURATION']} секунд",
                   get_call_type(row.loc['CALL_TYPE'])])


def get_html_row(call, calls, counter):
    """Создает строчку с данными о лучшем звонке менеджера"""

    row = f"""<tr>
                    <td>    {counter}   </td>
                    <td>    {calls[call['ID']]}  </td>
                    <td>    {call['ID']}    </td>
                    <td>    {call['PHONE_NUMBER']}  </td>
                    <td><a href='https://{settings.APP_SETTINGS.portal_domain}/disk/downloadFile/{call['RECORD_FILE_ID']}/'>Скачать</a></td>
                    <td>    {call['CALL_DURATION']} секунд  </td>
                    <td>    {parse_date(call['CALL_START_DATE'])}  </td>
                    <td>    {get_call_type(call['CALL_TYPE'])}  </td>
                </tr>\n"""

    return row


def get_html_table(rows):
    """Создает таблицу с данными о лучших звонках менеджеров"""

    html_table = f"""<table>
                    <tr>
                        <th>№</th>
                        <th>Менеджер</th>
                        <th>ID звонка</th>
                        <th>Номер</th>
                        <th>Запись звонка</th>
                        <th>Длительность</th>
                        <th>Дата</th>
                        <th>Тип</th>
                    </tr>
                    {rows}
                </table>"""

    return html_table
