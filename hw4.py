import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

"""### Получение всего контента страницы"""

response = requests.get('https://lifehacker.ru/topics/technology/')
response.text

"""### Попробуем спарсить контент первых 10 страниц Лайфхакера

"""

base_url = 'https://lifehacker.ru/topics/technology/' # базовая часть ссылки, позже в цикле будем добавлять к ней пагинацию
response = requests.get('https://lifehacker.ru/topics/technology/?page=1') # получаем контент первой страиниц
soup = BeautifulSoup(response.text, 'lxml') # инициализируем объект bs4 и задаем парсер lxml

soup.find_all('a', class_='lh-small-article-card__link') # ищем все a-элементы с классом lh-small-article-card__link

raw_items = soup.find_all('a', class_='lh-small-article-card__link')  # ищем все a-элементы с классом lh-small-article-card__link
links = [item.get('href') for item in raw_items] # получаем у ссылок только href-атрибут
links

base_url = 'https://lifehacker.ru/topics/technology'
all_parsed_urls = []

for page_num in range(1, 11):
    url = f'{base_url}/?page={page_num}' # подставляем нужный номер страницы для пагинации, дальше парсим каждую страницу аналогично коду выше
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    raw_items = soup.find_all('a', class_='lh-small-article-card__link')
    parsed_urls = [item.get('href') for item in raw_items]
    all_parsed_urls.extend(parsed_urls)

len(all_parsed_urls) # 10 страниц X 30 статей

all_parsed_urls[60:65]

all_parsed_urls[43:44]

base_url = 'https://lifehacker.ru/'

response = requests.get('https://lifehacker.ru/atlas-tancuet-breik-dans/')
soup = BeautifulSoup(response.text, 'lxml')
soup.find(class_='single-article__post-content single-article__content-container').text

response = requests.get('https://lifehacker.ru/atlas-tancuet-breik-dans/')
soup = BeautifulSoup(response.text, 'lxml')
soup.find('h1', class_='article-card__title').text

#при следующем шаге возникла ошибка и оказалось,что 43 статья сделана по другой верстке
response = requests.get('https://lifehacker.ru/special/elektronika-i-bytovaya-tekhnika/')
soup = BeautifulSoup(response.text, 'lxml')
soup.find('h1', class_='banner__title').text

#при следующем шаге возникла ошибка и оказалось,что 43 статья сделана по другой верстке
response = requests.get('https://lifehacker.ru/special/elektronika-i-bytovaya-tekhnika/')
soup = BeautifulSoup(response.text, 'lxml')
soup.find('div', class_='mustread-view-sections').text

result = []

for url in tqdm(all_parsed_urls):
    article = {}

    article_url = f'{base_url}{url}'  # Подставляем часть ссылки, ведущую к материалу
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'lxml')

    # Получаем заголовок
    title_element = soup.find('h1', class_='article-card__title')
    if title_element:
        article['title'] = title_element.text.strip()  # Убираем лишние пробелы
    else:
        title_element = soup.find('h1', class_='banner__title')
        if title_element:
            article['title'] = title_element.text.strip()  # Убираем лишние пробелы
        else:
            article['title'] = 'Заголовок не найден'

    # Получаем текст статьи
    text_element = soup.find(class_='single-article__post-content single-article__content-container')
    if text_element:
        article['text'] = text_element.text.strip()  # Убираем лишние пробелы
    else:
        text_element = soup.find('div', class_='mustread-view-sections')
        if text_element:
            article['text'] = text_element.text.strip()  # Убираем лишние пробелы
        else:
            article['text'] = 'Текст не найден'

    result.append(article)

# Выводим результат
for article in result:
    print(article)

"""Сделаем красивый датафрейм"""

pd.set_option('display.max_colwidth', 400)

data = pd.DataFrame(result)
data.head(300)
