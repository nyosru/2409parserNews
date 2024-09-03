import requests
from bs4 import BeautifulSoup
from datetime import datetime


def replace_month_with_number(date_str):
    """Заменяет название месяца на его номер в строке даты."""
    # Словарь для замены названий месяцев на их номера
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

    # Замена текстового названия месяца на его номер
    for month_name, month_number in months.items():
        if month_name in date_str:
            date_str = date_str.replace(month_name, month_number)
            break  # Прерываем цикл, так как замена уже выполнена

    return date_str


def parse_date(date_str):
    """Преобразует строку даты в формат YYYY-MM-DD HH:MM"""
    try:
        # Заменяем название месяца на номер
        date_str = replace_month_with_number(date_str)

        # Парсим дату и время из строки
        parsed_date = datetime.strptime(date_str, '%d %m %Y, %H:%M')

        # Возвращаем дату в формате 'YYYY-MM-DD HH:MM'
        return parsed_date.strftime('%Y-%m-%d %H:%M')
    except ValueError:
        # Если формат не совпадает, вернем исходную строку
        return date_str


def parse_news(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []

    # Ищем все элементы с классом 'section-video__item', содержащие информацию о новостях
    for item in soup.find_all('div', class_='section-video__item'):
        title_tag = item.find('a', class_='section-video__title')
        #content = item.find('div', class_='detail-card__text')  # Содержимое <div>

        img_tag = item.find('img', class_='section-video__img')

        category_tag = item.find('a', class_='section-video__category')
        date_tag = item.find('time', class_='section-video__item--date')

        # Извлекаем данные, если соответствующие теги найдены
        #content_text = content.get_text(strip=True) if content else 'no'
        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else ""
        image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
        category = category_tag.get_text(strip=True) if category_tag else ''
        category_link = category_tag['href'] if category_tag and 'href' in category_tag.attrs else ''
        date = date_tag.get_text(strip=True) if date_tag else ''

        date_to_db = parse_date(date)

        news_items.append({

            'title': title,
#             'content':'',

            'source': link,
            'image': image,

            'category': category,
            'category_link': category_link,

            'date': date_to_db,
            'date_origin': date

        })

    return news_items





def scrape_website(url, show_html=False):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем, успешен ли запрос (статус 200)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    html = response.text
    news_items = parse_news(html)

    # Текущее время для поля created_at
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Добавляем moderation_required = 1 ко всем элементам в news_items
    for news_item in news_items:
        news_item['moderation_required'] = 1
        news_item['created_at'] = current_time
        # Преобразуем дату для поля published_at
        news_item['published_at'] = parse_date(news_item['date'])

    result = {
        "url": url,
        "news": news_items
    }

    if show_html:
        result["html"] = html  # Добавляем полный HTML-код, если параметр show_html=True

    return result





def parse_news_item(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')

    # Находим блок с классом detail-card__entity
    entity_block = soup.find('div', class_='detail-card__entity')

    if not entity_block:
        return {
            'error': 'Блок с классом detail-card__entity не найден'
        }

    # Извлекаем заголовок внутри блока
    title_tag = entity_block.find('h1', class_='h2')
    title = title_tag.get_text(strip=True) if title_tag else None

    # Извлекаем дату внутри блока
    date_tag = entity_block.find('time', class_='prop-list__item detail-card-date')
    date = date_tag.get_text(strip=True) if date_tag else None

    # Извлекаем категорию внутри блока
    category_tag = entity_block.find('a', class_='prop-list__item colored')
    category = category_tag.get_text(strip=True) if category_tag else None

    # Извлекаем ссылку на изображение внутри блока
    image_tag = entity_block.find('img')
    image = urljoin(base_url, image_tag['src']) if image_tag else None

    # Извлекаем текст новости внутри блока
    text_tag = entity_block.find('div', class_='detail-card__text')
    text = text_tag.get_text(separator='\n', strip=True) if text_tag else None

    return {
        'title': title,
        'date': date,
        'category': category,
        'image': image,
        'text': text
    }
