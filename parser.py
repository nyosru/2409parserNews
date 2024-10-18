
from flask import request, jsonify
from bs4 import BeautifulSoup
import json
from scrapper import add_target_blank



def parse_news_list(html_content):

    url = request.args.get('url')
    return jsonify({'url':url})

    soup = BeautifulSoup(html_content, 'html.parser')
    news_list = []

    # Найти все элементы новостей
    posts = soup.find_all('div', class_='post-list__item')

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
        # Получить заголовок новости
        title_element = post.find('div', class_='post-list__name')
        title = title_element.get_text(strip=True) if title_element else ''

        # Получить ссылку на новость
        link_element = post.find('a', class_='post-list__link')
        link = link_element['href'] if link_element else ''

        # Получить дату новости
        date_element = post.find('div', class_='post-list__date')
        date = date_element.get_text(strip=True) if date_element else ''

        # Получить автора новости
        author_element = post.find('div', class_='post-list__author')
        author = author_element.get_text(strip=True) if author_element else ''

        # Получить анонс новости
        anons_element = post.find('div', class_='post-list__anons')
        anons = anons_element.get_text(strip=True) if anons_element else ''

        # Собрать данные в словарь
        news_item = {
            'title': title,
            'link': link,
            'date': date,
            'author': author,
            'anons': anons,
        }

        news_list.append(news_item)

    # Возвращаем JSON-данные
    return json.dumps(news_list, ensure_ascii=False)


def parse_72ru_news(html):

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Извлекаем первую картинку
    first_image = soup.select_one('.swiper-link img')
    first_image_url = first_image['src'] if first_image else None

    # Извлекаем HTML из блока с классом post__text
    post_text = soup.select_one('.post__text')
    post_text_html = add_target_blank(str(post_text)) if post_text else None



    # # Извлекаем название категории
    # category = soup.select_one('.post__category')
    # category_name = category.text.strip() if category else None
    #
    # # Извлекаем ссылку на категорию новости
    # category_link = category['href'] if category and 'href' in category.attrs else None

    # Находим последний элемент с классом 'bread__item'
    last_bread_item = soup.select_one('.bread__item:last-of-type')

    if last_bread_item:
        # Получаем ссылку и текст
        category_link = last_bread_item.a['href']
        category_name = last_bread_item.a.text

        # print("Категория:", category_name)
        # print("Ссылка на категорию:", category_link)
    else:
        # print("Категория не найдена.")
        category_link = None
        category_name = None


    # Извлекаем дату публикации
    date_published = soup.select_one('.post__date')
    date_published_text = date_published.text.strip() if date_published else None

    # Формируем итоговый JSON
    result = {
        "first_image": first_image_url,
        "post_text_html": post_text_html,
        "category_name": category_name,
        "category_link": category_link,
        "date_published": date_published_text
    }

    return json.dumps(result, ensure_ascii=False, indent=4)

# Пример использования
if __name__ == "__main__":
    url = "https://72.ru/text"  # Замените на нужный URL

# parsed_data = parse_vsluh_news(url)
# print(parsed_data)
