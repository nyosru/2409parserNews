import requests
from fn import replace_month_with_number, parse_date
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from db_utils import add_news_to_db
import idna
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import random


def random_delay():
    time.sleep(random.uniform(1, 3))


def get_html(url):
    # Путь к chromedriver (замените на ваш путь к драйверу)
    chromedriver_path = '/path/to/chromedriver'

    # Настройки браузера
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Без графического интерфейса
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # Отключение автоматизации
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36')  # Реалистичный user-agent
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-popup-blocking')

    # Инициализация драйвера
    service = Service(chromedriver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Удаляем флаг navigator.webdriver
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        # Открытие страницы по URL
        driver.get(url)

        # Добавляем случайную задержку перед получением HTML
        random_delay()

        # Получение HTML-кода страницы
        html = driver.page_source
    finally:
        # Закрытие браузера
        driver.quit()

    return html

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
from bs4 import BeautifulSoup

def parse_news_72_ru(html):

    """Парсит новости из HTML-страницы для домена тюменскаяобласть.рф"""
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []

    for item in soup.find_all('article', class_='OPHIx'):
        title_tag = item.find('h2', class_='h9Jmx')
        img_tag = item.find('img')
        category_tag = item.find('div', class_='Zrw4X')
        date_tag = item.find('time')

        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else ""
        image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
        category = category_tag.get_text(strip=True) if category_tag else ''
        category_link = category_tag.find('a')['href'] if category_tag and category_tag.find('a') else ''
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
            # 'moderation_required': 1,  # Установим значение по умолчанию
        })

    return news_items



def parse_news_vsluh_ru(html):
    """Парсит новости из HTML-страницы для домена vsluh_ru """
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

    if domain == '72.ru':

        # Извлекаем заголовок
        title = soup.find('h1', {'itemprop': 'headline'}).get_text(strip=True)

        # Извлекаем описание
        description = soup.find('p', {'itemprop': 'description'}).get_text(strip=True)

        # Извлекаем дату публикации
        date_published = soup.find('time', {'itemprop': 'datePublished'}).get_text(strip=True)

        # Извлекаем количество просмотров
        views = soup.find('span', class_='item_VmtHQ').get_text(strip=True)

        # Извлекаем текст статьи
        article_body = soup.find('div', {'itemprop': 'articleBody'})
        paragraphs = article_body.find_all('p')
        article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])

        # Извлекаем количество комментариев
        comments = soup.find('span', class_='counter_sZXgN').get_text(strip=True)

        # Возвращаем словарь с данными
        return {
            'title': title,
            'description': description,
            'date_published': date_published,
            'views': views,
            'article_text': article_text,
            'comments': comments
        }


    elif domain == 'тюменскаяобласть.рф':
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

    if domain == '72.ru':
        return parse_news_72_ru(html)

    if domain == 'тюменскаяобласть.рф':
        return parse_news_tyumen_oblast(html)

    if domain == 'vsluh.ru':
        return parse_news_vsluh_ru(html)
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
        for title_tag in ss.find_all('a', class_='section-filter__category'):
            link = title_tag['href'] if title_tag and 'href' in title_tag.attrs else ""
            title = title_tag.get_text(strip=True) if title_tag else ""

            catalogs.append({
                'title': title,
                'link_full': urljoin(f'https://{domain}', link),
                'link': link
            })

    elif domain == '72.ru':
        # Парсинг выпадающего списка рубрик
        select_tag = soup.find('select', class_='AzM0z')
        if select_tag:
            for option in select_tag.find_all('option'):
                value = option['value']
                title = option.get_text(strip=True)
                # Исключаем пункт "Все рубрики"
                if value != 'all':
                    catalogs.append({
                        'title': title,
                        'link_full': urljoin(f'https://{domain}', f'/category/{value}'),
                        # Предполагаем, что у вас есть структура URL
                        'link': f'/category/{value}'  # Здесь также указываем относительную ссылку
                    })

    return catalogs
