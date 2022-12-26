import requests
from bs4 import BeautifulSoup
import time


def get_data():
    list_skill = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'
    }
    url_djinni = "https://djinni.co/jobs/?primary_keyword=Python&region=UKR"
    response = requests.get(url_djinni, headers=headers)
    soap = BeautifulSoup(response.text, 'lxml')
    div_title = soap.find_all('div', 'list-jobs__title')

    n = 1
    for page in range(1):
        link = url_djinni + f'&page={n}'
        req = requests.get(link, headers=headers)
        if 'Вакансії Python' in req.text.title():
            print(f'&page={n}')
            n += 1
        else:
            break
        time.sleep(3)

        for div in div_title:
            link = div.a.get('href')
            title = div.span.text
            page_link = 'https://djinni.co' + link

            req = requests.get(page_link)
            soap = BeautifulSoup(req.text, 'lxml')
            toolbar = soap.find_all('div', 'job-additional-info--item-text')
            skills = list(toolbar)[1].text.strip().split(',')

            for el in skills:
                new_el = el.replace('\n', ' ').strip().lower()
                list_skill.append(new_el)
    print(list_skill)


def main():
    get_data()


if __name__ == '__main__':
    main()
