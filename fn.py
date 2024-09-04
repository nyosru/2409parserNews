from datetime import datetime

def replace_month_with_number(date_str):
    """Заменяет название месяца на его номер в строке даты."""
    months = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12'
    }

    for month_name, month_number in months.items():
        if month_name in date_str:
            date_str = date_str.replace(month_name, month_number)
            break

    return date_str


def parse_date(date_str):
    """Преобразует строку даты в формат YYYY-MM-DD HH:MM"""
    try:
        date_str = replace_month_with_number(date_str)
        parsed_date = datetime.strptime(date_str, '%d %m %Y, %H:%M')
        return parsed_date.strftime('%Y-%m-%d %H:%M')
    except ValueError:
        return date_str
