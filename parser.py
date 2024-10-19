
from bs4 import BeautifulSoup
import json
from scrapper import add_target_blank

from datetime import datetime


# поиск в ТюменскаяОбласть.рф
def parse_tmo_news_list(html_content):

    # url = request.args.get('url')
    # return jsonify({'url':url})
    #return json.dumps({'url':url}, ensure_ascii=False, indent=4)

    soup = BeautifulSoup(html_content, 'html.parser')
    news_list = []

    # Найти все элементы новостей
    posts = soup.find_all('div', class_='section-video__item')

    # def parse_news_72_ru(html):
    #     """Парсит новости из HTML-страницы для домена тюменскаяобласть.рф"""
    #     soup = BeautifulSoup(html, 'html.parser')
    #     news_items = []
    #
    #     news_items.append({
    #         'title': 777,
    #     });
    #
    #     for item in soup.find_all('article', class_='OPHIx'):
    #         title_tag = item.find('h2', class_='h9Jmx')
    #         img_tag = item.find('img')
    #         category_tag = item.find('div', class_='Zrw4X')
    #         date_tag = item.find('time')
    #
    #         title = title_tag.get_text(strip=True) if title_tag else ""
    #         link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else ""
    #         image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ''
    #         category = category_tag.get_text(strip=True) if category_tag else ''
    #         category_link = category_tag.find('a')['href'] if category_tag and category_tag.find('a') else ''
    #         date = date_tag.get_text(strip=True) if date_tag else ''
    #
    #         date_to_db = parse_date(date)
    #
    #         news_items.append({
    #             'title': title,
    #             'source': link,
    #             'image': image,
    #             'category': category,
    #             'category_link': category_link,
    #             'date': date_to_db,
    #             'date_origin': date,
    #             'item_html': item.get_text,
    #             # 'moderation_required': 1,  # Установим значение по умолчанию
    #         })
    #
    #     return news_items



    for post in posts:

        # Получить каталог новости
        cat = post.find('a', class_='section-video__category')
        cat_link = cat['href'] if cat else ''
        cat_name = cat.get_text(strip=True) if cat else ''

        # Получить заголовок новости
        title_element = post.find('a', class_='section-video__title')
        title = title_element.get_text(strip=True) if title_element else ''

        # Получить картинку
        i = post.find('img')
        img = i.get('src') if i else ''

        # Получить ссылку на новость
        link = title_element['href'] if title_element else ''

        # Получить дату новости
        #date_element = post.find('time', class_='post-section-video__item--date')
        date_element = post.find('time')
        date1 = date_element.get('datetime') if date_element else ''
        date = date_element.get_text(strip=True) if date_element else ''

        # # Получить автора новости
        # author_element = post.find('div', class_='post-list__author')
        # author = author_element.get_text(strip=True) if author_element else ''
        #
        # # Получить анонс новости
        # anons_element = post.find('div', class_='post-list__anons')
        # anons = anons_element.get_text(strip=True) if anons_element else ''

        # Собрать данные в словарь
        news_item = {
            'title': title,
            'link': link,
            'date': date,
            'date_origin': date1,
            # 'author': author,
            # 'anons': anons,
            'catalog_link':cat_link,
            'catalog_name':cat_name,
            'img':img,
        }

        news_list.append(news_item)

    # Возвращаем JSON-данные
    return json.dumps(news_list, ensure_ascii=False)

#parse_ura_news_list
# ura.news
from bs4 import BeautifulSoup
import json

def parse_ura_news_list(html_content):

    soup = BeautifulSoup(html_content, 'html.parser')
    news_list = []

    # Найти все элементы новостей
    posts = soup.find_all('li', class_='list-scroll-item')

    for post in posts:
        # Получить ссылку на новость
        link_element = post.find('a')
        link = link_element['href'] if link_element else ''

        # Получить время новости
        time_element = post.find('span', class_='time')
        time = time_element.get_text(strip=True) if time_element else ''

        # Удалить <span> из заголовка
        if link_element:
            # Удаляем все <span> элементы внутри тега <a>
            for span in link_element.find_all('span'):
                span.decompose()

            # Получаем текст заголовка без <span>
            title = link_element.get_text(strip=True)
        else:
            title = ''

        # Получить дату новости из родительского контейнера
        date_element = post.find_parent('div', class_='list-scroll-container').find_previous_sibling('div', class_='list-scroll-date')
        date = date_element.get_text(strip=True) if date_element else ''

        # Собрать данные в словарь
        news_item = {
            'title': title,
            'link': link,
            'time': time,
            'date': date
        }

        news_list.append(news_item)

    # Возвращаем JSON-данные
    return json.dumps(news_list, ensure_ascii=False)


def parse_tmo_news(html):

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Извлекаем заголовок новости
    title_element = soup.select_one('.detail-card__header h1')
    title = title_element.get_text(strip=True) if title_element else None

    # Извлекаем дату публикации
    date_element = soup.select_one('.detail-card__header time')
    date = date_element.get_text(strip=True) if date_element else None
    date_origin = date_element.get('datetime') if date_element else None

    # Извлекаем ссылку на категорию
    category_element = soup.select_one('.detail-card__header a')
    category_name = category_element.get_text(strip=True) if category_element else None
    category_link = category_element.get('href') if category_element else None

    # Извлекаем изображение
    image_element = soup.select_one('.detail-card__image img')
    image_url = image_element.get('src') if image_element else None

    # Извлекаем текст статьи
    text_element = soup.select_one('.detail-card__text')
    text_html = add_target_blank(str(text_element)) if text_element else None

    # Формируем итоговый JSON с нужными полями
    result = {
        "title": title,
        "date": date,
        "date_origin": date_origin,
        "category_name": category_name,
        "category_link": category_link,
        "image_url": image_url,
        "text_html": text_html
    }

    return json.dumps(result, ensure_ascii=False, indent=4)



from datetime import datetime
from bs4 import BeautifulSoup
import json

def parse_ura_news(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Заголовок новости
    title_tag = soup.find('h1', class_='publication-title')
    title = title_tag.get_text(strip=True) if title_tag else "Заголовок не найден"

    # Дата публикации
    date_published_tag = soup.find('time', itemprop='datePublished')
    date_published_raw = date_published_tag.get_text(strip=True) if date_published_tag else None
    date_published = date_published_raw
    # Преобразование даты к формату 'YYYY-MM-DD HH:MM:SS'
    # if date_published_raw:
    #     try:
    #         date_published = datetime.strptime(date_published_raw, '%d %B %Y, %H:%M')
    #         date_published = date_published.strftime('%Y-%m-%d %H:%M:%S')
    #     except ValueError:
    #         date_published = None  # На случай, если формат даты не распознан
    # else:
    #     date_published = None

    # Автор новости
    author_tag = soup.find('div', class_='author-name')
    author = author_tag.get_text(strip=True) if author_tag else "Автор не указан"

    # Тело статьи
    article_body = soup.find('div', itemprop='articleBody')

    # Извлекаем только <p> теги, которые являются дочерними элементами articleBody
    if article_body:
        paragraphs = article_body.find_all('p', recursive=False)
        body_html = ''.join([str(p) for p in paragraphs])  # Сохраняем HTML с тегами <p>
    else:
        body_html = None

    # Добавляем атрибут target="_blank" в ссылки
    text_html = add_target_blank(body_html) if body_html else None

    # Изображение с описанием
    image_block = soup.find('div', class_='item-img-block')
    image_url = image_block.find('img')['src'] if image_block and image_block.find('img') else None
    image_description_tag = image_block.find('span', itemprop='description') if image_block else None
    image_description = image_description_tag.get_text(strip=True) if image_description_tag else None

    # Собираем результат
    news_data = {
        'title': title,
        'date_published': date_published,
        'author': author,
        'text_html': text_html,
        'image_url': image_url,
        'image_description': image_description
    }

    return json.dumps(news_data, ensure_ascii=False, indent=4)



# Пример использования
if __name__ == "__main__":
    url = "https://72.ru/text"  # Замените на нужный URL

# parsed_data = parse_vsluh_news(url)
# print(parsed_data)
