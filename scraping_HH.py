import requests
from fake_headers import Headers
from bs4 import BeautifulSoup
from pprint import pprint
import json


HOST='https://spb.hh.ru'
BASE_SEARCH=f'{HOST}/search/vacancy?text=python&area=1&area=2'


def get_headers():
    return Headers(browser='firefox',os='win').generate()


def get_text(url):
    return requests.get(url, headers=get_headers()).text


if __name__ == "__main__":
    # Get page count
    search_page = requests.get(BASE_SEARCH, headers=get_headers()).text
    bs = BeautifulSoup(search_page, features='lxml')
    page_count = int(bs.find('span', attrs={
            'class': 'pager-item-not-in-short-range', 
            'data-qa': ''}
        ).find('span', attrs={
            'class': '', 'data-qa': '',
        }).text)

    vacancy_list_ok = []
    # Get every page
    for page_n in range(page_count):
        SEARCH=f'{BASE_SEARCH}&page={page_n}'
        print(SEARCH)
        search_page = requests.get(SEARCH, headers=get_headers()).text
        bs = BeautifulSoup(search_page, features='lxml')
        vacancy_list = bs.find(attrs={'data-qa': 'vacancy-serp__results'}).find_all(class_="serp-item")
        # print(vacancy_list)

        vacancy_data=[]
        for vacancy in vacancy_list:
            vacancy_name=vacancy.find('a',class_='serp-item__title')
            name=vacancy_name.text
            vacancy_link=vacancy_name['href']
            salary=vacancy.find('span',attrs={'data-qa': "vacancy-serp__vacancy-compensation"})
            salary = salary.text if salary else "Не указана"
            company_name=vacancy.find('a',attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            city=vacancy.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-address'}).text
            vacancy_data.append({
                "vacancy": name,
                "link": vacancy_link,
                "salary": salary,
                "company": company_name,
                "city": city,
            })
            
        for vacancy in vacancy_data:
            tag = get_text(vacancy_link)
            if 'Django' in tag or 'Flask' in tag:
                vacancy_list_ok.append(vacancy)

    # Print result and write to json file
    pprint(vacancy_list_ok)
    with open('vacancy.json', 'w', encoding='utf-8') as file:
        json.dump(vacancy_list_ok, file, ensure_ascii=False, indent=4)