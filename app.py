from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
# from db_utils import check_db_connection, insert_news
from db_utils import check_db_connection
from scrapper import parse_news,scrape_website,parse_news_item


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok'})

@app.route('/check_db', methods=['GET', 'POST'])
def check_db():
    # Проверяем подключение к базе данных
    connect_db = check_db_connection()

    # Формируем JSON-ответ
    response = {
        'connect_db': connect_db,
        'message': "Подключение к базе данных успешно." if connect_db else "Не удалось подключиться к базе данных."
    }

    return jsonify(response)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    show_html = request.args.get('show_html', 'false').lower() == 'true'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = scrape_website(url, show_html=show_html)
#     insert_news(result['news'])
    return jsonify(result)

@app.route('/parse_item', methods=['GET'])
def parse_item():
    url = request.args.get('url')
    show_html = request.args.get('show_html', 'false').lower() == 'true'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)})

    html = response.text
    news_item = parse_news_item(html, base_url=url)

    result = {
        "url": url,
        "news_item": news_item
    }

    if show_html:
        result["html"] = html  # Добавляем полный HTML-код, если параметр show_html=True

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
