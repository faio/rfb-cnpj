import re
from datetime import date


def parse_float(value):
    """
    Convert o valor para float
    :param value:
    :return:
    """
    try:
        return float(value.replace(',', '.'))
    except ValueError:
        return None


def parse_int(value):
    """
    Convert o valor para inteiro
    :param value:
    :return:
    """
    try:
        return int(value)
    except ValueError:
        return None


def parse_date(value):
    """
    Convert o valor para uma datetime.date
    :param value:
    :return:
    """
    if len(value) == 8:
        try:
            return date(
                year=int(value[0:4]),
                month=int(value[4:6]),
                day=int(value[6:8])
            )
        except ValueError:
            pass
    return None


def only_number(value):
    """
    Retorna apenas os números ou o valor None
    :param value:
    :return:
    """
    return re.compile(r'[^0-9]').sub('', str(value)) if value is not None else None
