import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint


HOST='https://habr.com'
MAIN=f'{HOST}/ru/all'

def get_headers():
    return Headers(browser='firefox',os='win').generate()

main_page=requests.get(MAIN, headers=get_headers()).text
# print(main_page)

bs=BeautifulSoup(main_page,features='lxml')
articles_list=bs.find(class_='tm-articles-list')
# pprint(articles_list)
articles_tags=articles_list.find_all('article')
# pprint(articles_tags)

parsed_data=[]
for article_tag in articles_tags:
    time_tag=article_tag.find('time')
    time=time_tag['datetime']
    title=article_tag.find('h2').find('span').text
    link=article_tag.find('a',class_='tm-article-snippet__title-link')['href']
    link=f'{HOST}{link}'

    full_article_html=requests.get(link,headers=get_headers()).text
    full_article_bs=BeautifulSoup(full_article_html, features='lxml')
    full_article_tag=full_article_bs.find(class_='tm-article-body')
    text=full_article_tag.text

    parsed_data.append({
    'time':time,
    'title':title,
    'link':link,
    'text':text})
    
pprint(parsed_data)