from flask import Flask, request, jsonify
from urllib.parse import urlparse
from scrapper import parse_news_tyumen_oblast, parse_news, scrape_website, parse_news_article, parse_catalogs, get_html
import requests
from vsluh_parser import parse_vsluh_news, parse_vsluh_news_list  # Импортируйте вашу функцию парсинга
from parser import parse_tmo_news_list, parse_tmo_news
from parser import parse_ura_news_list, parse_ura_news  # Импортируйте вашу функцию парсинга
from parser_72ru import parse_72ru_news, parse_72ru_news_list  # Импортируйте вашу функцию парсинга
import json


# Сопоставляем типы парсинга с функциями
PARSER_FUNCTIONS = {
    'parse_vsluh_news_list': parse_vsluh_news_list,
    'parse_vsluh_news': parse_vsluh_news,
    # Добавьте другие типы парсинга, если нужно
    #'parse_news_list': parse_news_list,

    'parse_72ru_news_list': parse_72ru_news_list,
    'parse_tmo_news_list': parse_tmo_news_list,
    'parse_tmo_news': parse_tmo_news,
    'parse_ura_news_list': parse_ura_news_list,
    'parse_ura_news': parse_ura_news
}


# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'ok'})



@app.route('/get_html', methods=['GET'])
def get_html_app():

    url = request.args.get('url')
    parse_type = request.args.get('type')  # Получаем тип парсинга

    # Проверяем, существует ли функция для переданного типа парсинга
    parser_function = PARSER_FUNCTIONS.get(parse_type)

    if parser_function:
        result = get_html(url)  # Используем функцию get_html для получения HTML
        html = result.get('html')  # Извлекаем HTML из результата
        # Вызываем соответствующую функцию парсинга
        parsed_data = parser_function(html)
        return jsonify(json.loads(parsed_data))  # Преобразуем JSON-строку обратно в объект
    else:
        # Если тип не указан или нет соответствующей функции, возвращаем HTML
        return jsonify({'error': 'no_function', 'parse_type':parse_type})




# @app.route('/check_db', methods=['GET', 'POST'])
# def check_db():
#     """Проверяет подключение к базе данных"""
#     connect_db = check_db_connection()
#     response = {
#         'connect_db': connect_db,
#         'message': "Подключение к базе данных успешно." if connect_db else "Не удалось подключиться к базе данных."
#     }
#     return jsonify(response)




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

    # Парсинг новостей в зависимости от домена
    response = requests.get(url, verify=False)

    if '72.ru' in url:
        res = parse_news(response.content, '72.ru')
    else:
        if 'vsluh.ru' in url:
            res = parse_news(response.content, 'vsluh.ru')
        else:
            res = parse_news_tyumen_oblast(response.content)

    result = {
        'url': url,
        'items': res,
        'html_length': len(response.content)  # Добавляем длину HTML-кода
    }

    # if show_html:
    # result["html"] = response.content  # Добавляем полный HTML-код, если параметр show_html=True

    return jsonify(result)

# @app.route('/get_html2', methods=['GET'])
# def get_html_app2():
#     url = request.args.get('url')
#     # html = get_html(url)
#     #
#     # result = {
#     #     "url": url,
#     #     "html": html
#     # }
#     # return jsonify(result)
#     driver = setup_driver()  # Инициализируем драйвер через setup_driver
#     try:
#         driver.get(url)
#         print(f"Title of the page is: {driver.title}")
#         # Ваш код для скрапинга здесь
#
#     finally:
#         driver.quit()



# @app.route('/get_html', methods=['GET'])
# def get_html_app():
#     url = request.args.get('url')
#     result = get_html(url)
#     return jsonify(result)

@app.route('/parse_news_full', methods=['GET'])
def parse_news_full():
    url = request.args.get('url')
    result = scrape_website(url)
    return jsonify(result)


@app.route('/parse_item', methods=['GET', 'POST'])
def parse_item():
    """Парсит одиночную новость с указанного URL"""

    # Получаем все параметры запроса (GET и POST)
    # all_get_params = request.args.to_dict()  # Все GET параметры
    # all_post_params = request.form.to_dict()  # Все POST параметры
    # all_params = request.values.to_dict()  # Объединяет GET и POST параметры

    # Получаем отдельно url и html_in для примера
    # url = request.values.get('url')
    url = request.form.get('url')
    # html_in = request.values.get('html')
    html_in = request.form.get('html')

    # result = {
    #     # "get_params": all_get_params,
    #     # "post_params": all_post_params,
    #     # "all_params": all_params,  # Все параметры (GET и POST)
    #     "url": url,
    #     "html_in": html_in
    # }
    #
    # return jsonify(result)

    # html_in1 = 1

    # if request.method == 'POST':
    #     url = request.args.get('url')
    #     # url = request.form.get('url')
    #     html_in = request.form.get('html')
    #     html_in1 = request.args.get('html')
    # else:  # Для GET-запросов
    #     url = request.args.get('url')
    #     html_in = request.args.get('html')
    #
    # result = {
    #     "url": url,
    #     "html_in": html_in,
    #     "html_in1": html_in1
    # }

    # return jsonify(result)

    show_html = request.args.get('show_html', 'false').lower() == 'true'

    # response = requests.get(url, verify=False)
    # res = parse_news_tyumen_oblast(response.content)
    domain = urlparse(url).netloc
    #  news_item = parse_news_article(response.content, domain)

    if html_in:  # Если html_in не пустой
        news_item = parse_news_article(html_in, domain)
        result = {
            "news_item": news_item
        }
    else:  # Если html_in пустой, парсим новость с указанного URL
        response = requests.get(url, verify=False)
        news_item = parse_news_article(response.content, domain)
        result = {
            "url": url,
            "news_item": news_item
        }

        if show_html:
            result["html"] = response.content  # Добавляем полный HTML-код, если параметр show_html=True

    return jsonify(result)

# def get_html_selenium(url):
#     """Использует Selenium для получения HTML-кода страницы"""
#     chrome_options = Options()
#     chrome_options.add_argument('--headless')  # Запуск в фоновом режиме без открытия окна браузера
#     chrome_options.add_argument('--no-sandbox')
#     chrome_options.add_argument('--disable-dev-shm-usage')
#
#     try:
#         # Используем ChromeDriverManager для автоматической установки драйвера
#         driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
#         driver.get(url)
#         html = driver.page_source
#         driver.quit()
#         return {'html': html}
#     except Exception as e:
#         return {'error': str(e)}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5047, debug=True)
