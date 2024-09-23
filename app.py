from flask import Flask, request, jsonify
from urllib.parse import urlparse
from scrapper import parse_news, scrape_website, parse_news_article, parse_catalogs
import requests

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

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




@app.route('/catalogs', methods=['GET'])
def parse_catalogs_route():
    """Парсит каталоги новостей с главной страницы сайта, используя Selenium"""
    url = request.args.get('url')
    show_html = request.args.get('show_html', 'false').lower() == 'true'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    try:
        response = requests.get(url, verify=False)
        html = response.content


    except Exception as e:
        return jsonify({
            "error": str(e),
            "line": 50,
            "step": 3
        })

    domain = urlparse(url).netloc
    catalogs = parse_catalogs(html, domain)

    result = {
        "url": url,
        "catalogs": catalogs
    }

    if show_html:
        result["html"] = html  # Добавляем полный HTML-код, если параметр show_html=True

    return jsonify(result)


@app.route('/news_list', methods=['GET'])
def scrape():
    """Парсит новости с указанного URL и добавляет их в базу данных"""
    url = request.args.get('url')
    show_html = request.args.get('show_html', 'false').lower() == 'true'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Парсинг новостей
    result = scrape_website_selenium(url, show_html=show_html)

    return jsonify(result)


@app.route('/parse_item', methods=['GET'])
def parse_item():
    """Парсит одиночную новость с указанного URL"""
    url = request.args.get('url')
    show_html = request.args.get('show_html', 'false').lower() == 'true'

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    # Используем Selenium для загрузки страницы
    html = get_html_selenium(url)
    if 'error' in html:
        return jsonify(html)

    domain = urlparse(url).netloc
    news_item = parse_news_article(html['html'], domain)

    result = {
        "url": url,
        "news_item": news_item
    }

    if show_html:
        result["html"] = html['html']  # Добавляем полный HTML-код, если параметр show_html=True

    return jsonify(result)


def get_html_selenium(url):
    """Использует Selenium для получения HTML-кода страницы"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Запуск в фоновом режиме без открытия окна браузера
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    try:
        # Используем ChromeDriverManager для автоматической установки драйвера
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return {'html': html}
    except Exception as e:
        return {'error': str(e)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5047, debug=True)
