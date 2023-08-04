import requests
from bs4 import BeautifulSoup
import fake_headers
import json

KEYWORDS = ["Django", "Flask", "SQL"]
vacancy_data = 'vacancy_data.json'
headers_gen = fake_headers.Headers(browser='chrome', os='win')

HOST = 'https://spb.hh.ru'
page = int(input('Укажите необходимое колличество страниц для обработки по поиску подходящих вакансий: '))

start_page = 0
articles_parsed = []
while page > start_page:
    print(f'Обрабатывается {start_page + 1} страница hh.ru.')
    params = {
        'text': 'python',
        'area': 2,
        'area': 1,
        'items_on_page': 20,
        'page': start_page
    }
    
    response = requests.get('https://spb.hh.ru/search/vacancy?',params=params, headers=headers_gen.generate())
    response_text = response.text

    soup = BeautifulSoup(response_text, features='lxml')
    article_list_tag = soup.find('div', {'data-qa': "vacancy-serp__results"})
    try:
        article_tags = article_list_tag.find_all('div',class_="vacancy-serp-item__layout")
    except:
        break

    for article_tag in article_tags:
        a_tag = article_tag.find('a')

        try:
            salary = article_tag.find('span', class_="bloko-header-section-2").text
        except:
            salary = 'Не указана'

        company_name = article_tag.find('a', class_='bloko-link bloko-link_kind-tertiary').text

        link = a_tag['href']

        adress = article_tag.find('div', {'data-qa': "vacancy-serp__vacancy-address"}).text

        article_response = requests.get(link, headers=headers_gen.generate())
        article = BeautifulSoup(article_response.text, 'lxml')
        
        try:
            description = article.find('div', class_='g-user-content').text
        except:
            description = 'None'

        for word in KEYWORDS:
            # if word in description and '$' in salary:  функция поиска по ЗП в долларах
            if word in description:
                articles_parsed.append({
        'link': link,
        'salary': salary,
        'company_name': company_name,
        'adress': adress
    })
    start_page += 1

print(f'Полученные данные записываются в файл {vacancy_data}.')

with open(vacancy_data, 'w', encoding='utf-8') as f:
    file = json.dumps(articles_parsed, indent=2, ensure_ascii=False)
    f.write(file)

print(f'Данные о вакансиях успешно записаны в {vacancy_data}.')