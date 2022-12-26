import requests
from bs4 import BeautifulSoup
import time


def get_data(xp_level: str = 'no_exp'):
    list_skill = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'
    }
    url_djinni = f"https://djinni.co/jobs/?primary_keyword=Python&region=UKR&exp_level={xp_level}"
    count_page = 1
    n = 1
    title_list = []
    find_number_page = requests.get(url_djinni, headers=headers)
    soap_page = BeautifulSoup(find_number_page.text, 'lxml')
    li = soap_page.find_all('li', 'page-item')
    lst = []
    for i in li:
        el = i.text.strip()
        if el != '':
            lst.append(el)
    if len(lst) > 0:
        n = int(lst[-1])
    elif len(lst) <= 0:
        n = 1

    for page in range(n):
        link = url_djinni + f'&page={count_page}'
        print(f'page={count_page}')
        response = requests.get(link, headers=headers)
        soap = BeautifulSoup(response.text, 'lxml')
        div_title = soap.find_all('div', 'list-jobs__title')
        time.sleep(2)
        count_page += 1

        for div in div_title:
            link = div.a.get('href')
            title = div.span.text
            page_link = 'https://djinni.co' + link

            req = requests.get(page_link, headers=headers)
            soap = BeautifulSoup(req.text, 'lxml')
            toolbar = soap.find_all('div', 'job-additional-info--item-text')
            skills = list(toolbar)[1].text.strip().split(',')

            for el in skills:
                new_el = el.replace('\n', ' ').strip().lower()
                list_skill.append(new_el)
            title_list.append(title)
    print(len(title_list))
    print(len(list_skill))


def main():
    get_data()


if __name__ == '__main__':
    main()
