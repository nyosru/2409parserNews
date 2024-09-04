from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from db_utils import check_db_connection, add_news_to_db
from scrapper import parse_news, scrape_website, parse_news, parse_news_article

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok'})

@app.route('/check_db', methods=['GET', 'POST'])
def check_db():
    """Проверяет подключение к базе данных"""
    connect_db = check_db_connection()
    response = {
        'connect_db': connect_db,
        'message': "Подключение к базе данных успешно." if connect_db else "Не удалось подключиться к базе данных."
    }
    return jsonify(response)



@app.route('/news_list', methods=['GET'])
def scrape():
    """Парсит новости с указанного URL и добавляет их в базу данных"""
    url = request.args.get('url')
    show_html = request.args.get('show_html', 'false').lower() == 'true'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Парсинг новостей
    result = scrape_website(url, show_html=show_html)

    # Списки для хранения результатов
#     added_news = []
#     not_added_news = []

    # Обрабатываем новости
#     for news_item in result.get('news', []):
#         add_result = add_news_to_db(news_item)
#         if add_result['status']:
#             added_news.append(news_item['title'])
#         else:
#             not_added_news.append(news_item['title'])

    # Добавляем списки в результат
#     result['added_news'] = added_news
#     result['not_added_news'] = not_added_news

    return jsonify(result)



@app.route('/parse_item', methods=['GET'])
def parse_item():
    """Парсит одиночную новость с указанного URL"""
    url = request.args.get('url')
    show_html = request.args.get('show_html', 'false').lower() == 'true'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})

    domain = urlparse(url).netloc
    html = response.text
    news_item = parse_news_article(html,domain)

    result = {
        "url": url,
        "news_item": news_item
    }

    if show_html:
        result["html"] = html  # Добавляем полный HTML-код, если параметр show_html=True

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5047, debug=True)
