import requests
from fn import replace_month_with_number, parse_date
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from db_utils import add_news_to_db
import idna

def parse_news_tyumen_oblast(html):
    """Парсит новости из HTML-страницы для домена тюменскаяобласть.рф"""
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []

    for item in soup.find_all('div', class_='section-video__item'):
        title_tag = item.find('a', class_='section-video__title')
        img_tag = item.find('img', class_='section-video__img')
        category_tag = item.find('a', class_='section-video__category')
        date_tag = item.find('time', class_='section-video__item--date')

        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else ""
        image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
        category = category_tag.get_text(strip=True) if category_tag else ''
        category_link = category_tag['href'] if category_tag and 'href' in category_tag.attrs else ''
        date = date_tag.get_text(strip=True) if date_tag else ''

        date_to_db = parse_date(date)

        news_items.append({
            'title': title,
            'source': link,
            'image': image,
            'category': category,
            'category_link': category_link,
            'date': date_to_db,
            'date_origin': date,
            #             'moderation_required': 1,  # Установим значение по умолчанию
        })

    return news_items


def parse_news_article(html, domain):
    """Парсит отдельную новость из HTML-страницы"""
    soup = BeautifulSoup(html, 'html.parser')

    if domain == 'тюменскаяобласть.рф':
        b = soup.find('div', class_='detail-card__entity')
        title_tag = b.find('h1', class_='h2')
        category_tag = b.find('a', class_='prop-list__item colored')
        date_tag = b.find('time', class_='prop-list__item.detail-card-date')
        #image_tag = b.find('div', class_='detail-card__image-wrapper img')
        content_tag = b.find('div', class_='detail-card__text')

        title = title_tag.get_text(strip=True) if title_tag else ""
        category = category_tag.get_text(strip=True) if category_tag else ""
        date = date_tag.get_text(strip=True) if date_tag else ""
        #image = image_tag.find('img')['src'] if image_tag else ""
        content = content_tag.get_text(strip=True) if content_tag else ""

        # Извлечение всех изображений внутри блока с классом "detail-card__entity"
        image_tags = b.select('img')
        images = [img['src'] for img in image_tags if 'src' in img.attrs]

        parsed_date = parse_date(date)

        news_item = {
            'title': title,
            'category': category,
            'date': parsed_date,
            #'image': image,
            'image': images,
            'content': content,
        }

        return news_item

    return False


def parse_news(html, domain):
    """Выбирает парсер новостей в зависимости от домена"""
    if domain == 'тюменскаяобласть.рф':
        return parse_news_tyumen_oblast(html)
    else:
        # Ваш стандартный парсер новостей
        soup = BeautifulSoup(html, 'html.parser')
        news_items = []

        # Ваш стандартный парсинг новостей здесь...

        return news_items


def scrape_website(url, show_html=False):
    """Основная функция для парсинга новостей и добавления их в базу данных"""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем успешность запроса
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

    domain = urlparse(url).netloc
    html = response.text

    news_items = parse_news(html, domain)

    result = {
        "url": url,
        "news": news_items,
        #         "added": [],
        #         "not_added": []
    }

    #     for news_item in news_items:
    #         news_item['source_domain'] = domain
    #         add_result = add_news_to_db(news_item)
    #         if add_result['status']:
    #             result["added"].append(news_item['title'])
    #         else:
    #             result["not_added"].append(news_item['title'])

    if show_html:
        result["html"] = html  # Добавляем HTML-код, если параметр show_html=True

    return result

def parse_catalogs(html, domain):
    """Парсит каталоги новостей (ссылки и названия) с главной страницы"""
    soup = BeautifulSoup(html, 'html.parser')
    catalogs = []

    if domain == 'тюменскаяобласть.рф':
        # Предполагается, что каталоги находятся внутри определённого блока
        ss = soup.find('div', class_='section-filter__categories')
        for title_tag in ss.find_all('a', class_='section-filter__category'):  # Укажите правильный класс блока каталогов
            #title_tag = catalog.find('a', class_='section-filter__category')  # Укажите правильный класс для заголовка
            link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else ""
            title = title_tag.get_text(strip=True) if title_tag else ""

            catalogs.append({
                'title': title,
                'link_full': urljoin(f'https://{domain}', link),
                'link': link
            })

    return catalogs
