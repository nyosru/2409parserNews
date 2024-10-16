from bs4 import BeautifulSoup
import json
from scrapper import add_target_blank

def parse_vsluh_news(html):

    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Извлекаем первую картинку
    first_image = soup.select_one('.swiper-link img')
    first_image_url = first_image['src'] if first_image else None

    # Извлекаем HTML из блока с классом post__text
    post_text = soup.select_one('.post__text')
    post_text_html = add_target_blank(str(post_text)) if post_text else None

    # Извлекаем название категории
    category = soup.select_one('.post__category')
    category_name = category.text.strip() if category else None

    # Извлекаем ссылку на категорию новости
    category_link = category['href'] if category and 'href' in category.attrs else None

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
    url = "https://vsluh.ru/news/example-news-url"  # Замените на нужный URL
    parsed_data = parse_vsluh_news(url)
    print(parsed_data)
