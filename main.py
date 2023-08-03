import requests
from bs4 import BeautifulSoup
import fake_headers
from pprint import pprint

KEYWORDS = ['дизайн', 'фото', 'web', 'python']
headers_gen = fake_headers.Headers(browser='chrome', os='win')

HOST = 'https://habr.com'
habr_url = f'{HOST}/ru/all/'

response = requests.get(habr_url, headers=headers_gen.generate())
response_text = response.text

soup = BeautifulSoup(response_text, features='lxml')
article_list_tag = soup.find('div', class_='tm-articles-list')
article_tags = article_list_tag.find_all('article')

articles_parsed = []
for article_tag in article_tags:
    header_tag = article_tag.find('h2')
    a_tag = header_tag.find('a')

    time_tag = article_tag.find('time')
    publication_time = time_tag['datetime']

    header_text = header_tag.text
    link = a_tag['href']
    publication_link = f'{HOST}{link}'

    article_response = requests.get(publication_link, headers=headers_gen.generate())
    article = BeautifulSoup(article_response.text, 'lxml')
    article_body_tag = article.find('div', id='post-content-body')
    article_body_text = article_body_tag.text

    for word in KEYWORDS:
        if word in article_body_text:
            articles_parsed.append({
    'publication_time': publication_time,
    'header': header_text,
    'link': publication_link
})
            
pprint(articles_parsed)
