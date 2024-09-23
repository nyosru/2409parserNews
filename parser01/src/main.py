from bs4 import BeautifulSoup
import requests

def get_html(url):
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

if __name__ == '__main__':
    base_url = 'https://php-cat.com'
    param = {'param1': 'value1', 'param2': 'value2'}
    #full_url = f'{base_url}?{requests.utils.urlencode(param)}'
    full_url = f'{base_url}'
    html = get_html(full_url)
    print(html)