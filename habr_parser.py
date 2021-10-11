from bs4 import BeautifulSoup
import requests
import random


def all_pages_parsing(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    page = soup.find_all('a', attrs={'class': 'tm-article-snippet__title-link'}, href=True)
    for entry in page:
        title = 'https://habr.com' + entry.get('href')
        all_url.append(title)


def all_articles_parsing(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.find('h1', attrs={'class': 'tm-article-snippet__title tm-article-snippet__title_h1'})
    body = soup.find('div', attrs={'xmlns': 'http://www.w3.org/1999/xhtml'})
    no_code = body.find_all('code')
    body = str(body.text)
    for i in no_code:
        i = i.text
        body = body.replace(str(i), '')
    body = body.replace('\r', '').replace('\n', '')
    tag = soup.find('ul', attrs={'class': 'tm-separated-list__list'})
    all_name_title.append(title.text)
    all_body.append(body)
    tm = tag.find_all('li')
    list_tag = []
    for j in tm:
        list_tag.append(j.text)
    new_list = ', '.join(list_tag)
    all_tag.append(new_list)


all_url = []
all_article = []
all_name_title = []
all_body = []
all_tag = []
for dig in range(1, 51):
    full_url = 'https://habr.com/ru/all/page' + str(dig) + '/'
    all_pages_parsing(url=full_url)
while len(all_article) != 55:
    article = random.choice(all_url)
    if article not in all_article:
        all_article.append(article)
for article in all_article:
    all_articles_parsing(url=article)
with open(file='output.txt', mode='w', encoding='utf-8') as file:
    file.write('link\ttitle\tbody\ttags\n')
    for a, n, b, t in zip(all_article, all_name_title, all_body, all_tag):
        b = str(b).replace('\n', '')
        file.write(f'{a}\t{n}\t{b}\t{t}\n')

