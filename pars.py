import requests
from bs4 import BeautifulSoup
import time


def get_data():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'
    }
    url_djinni = "https://djinni.co/jobs/?primary_keyword=Python&region=UKR"
    response = requests.get(url_djinni, headers=headers)
    soap = BeautifulSoup(response.text, 'lxml')
    div_title = soap.find_all('div', 'list-jobs__title')

    job_for_senior = []
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

            if 'Senior' in title:
                job_for_senior.append(title)
            else:
                req = requests.get(page_link)
                soap = BeautifulSoup(req.text, 'lxml')
                toolbar = soap.find('div', 'job-additional-info--item-text')
                print(toolbar)
                '''for i in toolbar:
                    print(i.text.strip())
                    print('-' * 20)'''


def main():
    get_data()


if __name__ == '__main__':
    main()
