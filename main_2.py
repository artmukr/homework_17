import requests
from bs4 import BeautifulSoup
import json


def get_links(input_link):
    res = requests.get(input_link)
    soup = BeautifulSoup(res.text, 'html.parser')
    block = soup.find_all('a', {'class': 'text-block'})
    links = []
    names = []
    status = []
    for el in block:
        a = el['href']
        link = f'https://lostfilm.tv{a}'
        links.append(link)
        res_1 = requests.get(link)
        soup_1 = BeautifulSoup(res_1.text, 'html.parser')
        block_1 = soup_1.find('div', {'class': 'wrapper'})('h2')
        block_2 = soup_1.find('div', {'class': 'wrapper'})\
            ('div', {'class': 'status'})
        names.append(block_1[0].getText())
        first_replace = (block_2[0].getText()).replace('\r\n\t\t\t\t', '')
        second_replace = (first_replace.replace('\r\n\t\t', ''))
        status.append(second_replace.replace('\t', ''))
    films_status = dict(zip(names, status))
    with open('film_status.json', 'w', encoding='utf-8') as j:
        j.write(json.dumps(films_status))
    return films_status


if __name__ == '__main__':
    print(get_links("http://www.lostfilm.tv/"))
