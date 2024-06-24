import locale


def sort_by_name(data: list[dict[str, str]]) -> list[dict[str, str]]:
    locale.setlocale(locale.LC_ALL, '')

    sorted_field_values = sorted(data, key=lambda x: locale.strxfrm(x['VALUE']))
    for index, value in enumerate(sorted_field_values.copy()):
        sorted_field_values[index]['SORT'] = index
    return sorted_field_values
