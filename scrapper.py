import requests
from requests.exceptions import RequestException

from fn import replace_month_with_number, parse_date
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import idna
import time
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
# import time

import chardet

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def hide_selenium(driver):
    """Скрытие Selenium от сайтов"""
    # Отключаем navigator.webdriver
    driver.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
            '''
        }
    )

    # Удаляем автоматические заголовки
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'})

    # Скрытие других методов распознавания Selenium
    driver.execute_script("""
        Object.defineProperty(navigator, 'languages', {
          get: function() { return ['en-US', 'en']; }
        });
        Object.defineProperty(navigator, 'plugins', {
          get: function() { return [1, 2, 3]; }
        });
    """)


def get_html2(url):
    """Получение HTML с помощью Selenium с ожиданием выполнения JavaScript и скрытием Selenium"""

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Без интерфейса
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Добавляем кастомный user-agent
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36")

    # Установка драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Скрываем использование Selenium
        hide_selenium(driver)

        # Открываем URL
        driver.get(url)

        # Ожидаем выполнения всех JavaScript и загрузки определённого элемента
        wait = WebDriverWait(driver, 10)  # Устанавливаем тайм-аут ожидания
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Ожидаем появления элемента body

        # Ожидание завершения всех AJAX запросов
        wait.until(lambda d: d.execute_script('return jQuery.active == 0'))

        # Получаем HTML-код страницы
        html = driver.page_source

        return {"status": True, "html": html}

    except Exception as e:
        return {"status": False, "error": str(e)}

    finally:
        driver.quit()


def decode_to_utf8(byte_data):
    """Функция для декодирования строки в UTF-8"""
    detected = chardet.detect(byte_data)
    encoding = detected['encoding']
    if encoding:
        return byte_data.decode(encoding).encode('utf-8').decode('utf-8')
    else:
        raise ValueError("Не удалось определить кодировку")

def get_html2_0726(url):
    """Получение HTML с помощью Selenium"""

    # Настройки браузера (без графического интерфейса)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Запуск без графического интерфейса
    chrome_options.add_argument("--no-sandbox")  # Для работы в контейнере
    chrome_options.add_argument("--disable-dev-shm-usage")  # Для увеличения разделяемой памяти

    # Установка драйвера
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Открываем URL
        driver.get(url)

        # Ждем некоторое время, чтобы страница полностью загрузилась
        time.sleep(2)  # Можно изменить время ожидания при необходимости

        # Получаем HTML-код страницы
        html = driver.page_source

        # Возвращаем результат
        return {
            "status": True,
            "html": html
        }

    except Exception as e:
        # В случае ошибки возвращаем False и описание ошибки
        return {
            "status": False,
            "error": str(e)
        }

    finally:
        # Закрываем браузер
        driver.quit()



def random_delay():
    time.sleep(random.uniform(1, 3))


def get_html(url):
    """Получение HTML с помощью requests или Selenium"""
    result = get_html2(url)

    # Если нужно использовать requests, то можем закомментировать вызов Selenium
    if not result['status']:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            # Декодируем текст HTML
            html = decode_to_utf8(response.content)  # Перекодировка в UTF-8

            return {"status": True, "html": html}
        except RequestException as e:
            return {"status": False, "html": f"An error occurred: {e}"}

    return result

def get_html333(url):

    return get_html2(url)

    """
    Получает HTML содержимое страницы по указанному URL.

    :param url: Ссылка на страницу
    :return: Словарь с параметрами status и html
    """
    try:
        # Отправляем запрос на указанный URL
        response = requests.get(url, timeout=10)
        # Проверяем успешность запроса (статус-код 200)
        response.raise_for_status()
        # Возвращаем успешный статус и HTML содержимое
        return {"status": True, "html": response.text}
    except RequestException as e:
        # Возвращаем статус false и сообщение об ошибке, если запрос не удался
        return {"status": False, "html": f"An error occurred: {e}"}


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


def parse_news_72_ru(html):
    """Парсит новости из HTML-страницы для домена тюменскаяобласть.рф"""
    soup = BeautifulSoup(html, 'html.parser')
    news_items = []

    news_items.append({
        'title': 777,
    });

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
            'item_html': item.get_text,
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
    # return domain
    # return html

    """Парсит отдельную новость из HTML-страницы"""
    soup = BeautifulSoup(html, 'html.parser')

    if domain == '72.ru':

        # Извлекаем заголовок
        title = soup.find('h1', {'itemprop': 'headline'}).get_text(strip=True)
        # return title

        try:
            # Извлекаем описание
            description = soup.find('p', {'itemprop': 'description'}).get_text(strip=True)
        except:
            description = 'ошибка'

        try:
            # Извлекаем дату публикации
            date_published = soup.find('time', {'itemprop': 'datePublished'}).get_text(strip=True)
        except:
            description = 'ошибка2'

        try:
            # Извлекаем количество просмотров
            views = soup.find('span', class_='item_VmtHQ').get_text(strip=True)
        except:
            description = 'ошибка3'

        try:
            # Извлекаем текст статьи
            article_body = soup.find('div', {'itemprop': 'articleBody'})
        except:
            description = 'ошибка4'

        try:
            paragraphs = article_body.find_all('p')
        except:
            description = 'ошибка5'

        try:
            article_text = '\n'.join([p.get_text(strip=True) for p in paragraphs])
        except:
            description = 'ошибка6'

        try:
            # Извлекаем количество комментариев
            comments = soup.find('span', class_='counter_sZXgN').get_text(strip=True)
        except:
            description = 'ошибка7'

        # Возвращаем словарь с данными
        news_item = {
            'ss': 1,
            'title': title,
            'content': article_text,
            'dop': {
                'description': description,
                'views': views,
                'published_datetime': date_published,
                'comments_kolvo': comments
            },
        }


    elif domain == 'тюменскаяобласть.рф':
        b = soup.find('div', class_='detail-card__entity')
        title_tag = b.find('h1', class_='h2')
        category_tag = b.find('a', class_='prop-list__item colored')
        date_tag = b.find('time', class_='prop-list__item.detail-card-date')
        # image_tag = b.find('div', class_='detail-card__image-wrapper img')
        content_tag = b.find('div', class_='detail-card__text')

        title = title_tag.get_text(strip=True) if title_tag else ""
        category = category_tag.get_text(strip=True) if category_tag else ""
        date = date_tag.get_text(strip=True) if date_tag else ""
        # image = image_tag.find('img')['src'] if image_tag else ""
        content = content_tag.get_text(strip=True) if content_tag else ""

        # Извлечение всех изображений внутри блока с классом "detail-card__entity"
        image_tags = b.select('img')
        images = [img['src'] for img in image_tags if 'src' in img.attrs]

        parsed_date = parse_date(date)

        news_item = {
            'title': title,
            'category': category,
            'date': parsed_date,
            # 'image': image,
            'image': images,
            'content': content,
        }

    return news_item

    # return False


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
        # news_items.append(77)
        # Ваш стандартный парсинг новостей здесь...
        return {'status': 'default'}


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
        'domain': domain,
        "url": url,
        "news": news_items,
        'html': html,
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
