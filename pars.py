import json
import requests
from bs4 import BeautifulSoup
import time
from settings import params, cookies, headers, months


def get_data(xp_level: str):
    """
    simple_input = ['no_exp', '1y', '2y', '3y', '4y', '5y']
    at the output list
    """
    try:
        vacancies = read_file()
    except FileNotFoundError:
        vacancies = []

    url_djinni = f"https://djinni.co/jobs/?primary_keyword=Python&region=UKR&exp_level={xp_level}"
    count_page = 1

    s = requests.Session()
    response = s.get(url=url_djinni, params=params, cookies=cookies, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    # find last page

    all_li = soup.find_all('li', class_="page-item")
    try:
        last_page = int(all_li[-2].text.strip())
    except IndexError:
        last_page = 1

    # pagination

    for page in range(last_page):
        link = url_djinni + f'&page={count_page}'
        print(f'page = {count_page}/{last_page}')
        response = s.get(link, params=params, cookies=cookies, headers=headers)
        soap = BeautifulSoup(response.text, 'lxml')
        div_title = soap.find_all('div', 'list-jobs__title')
        time.sleep(3)
        count_page += 1

        # find all links job on page

        for div in div_title:
            link = div.a.get('href')
            title = div.span.text
            page_link = 'https://djinni.co' + link

            response = s.get(page_link, params=params, cookies=cookies, headers=headers)
            soap = BeautifulSoup(response.text, 'lxml')
            toolbar = soap.find_all('li', class_="job-additional-info--item")

            # get time created
            get_time_created = soap.find('div', class_="text-small")
            lst_time = []
            for i in get_time_created:
                p = i.text.replace('\n', '').strip().split(' ')
                for el in p:
                    if el != '':
                        lst_time.append(el)
            time_created = lst_time[2] + '/' + months[lst_time[3]] + '/' + lst_time[4]

            #  collection of all requirements to the list

            jobs_dict = {}
            requirements = []
            for element in toolbar:
                temp_list = []
                element = element.text.replace('\n', '').strip()
                element = element.split(',')
                for requirement in element:
                    requirement = requirement.strip()
                    temp_list.append(requirement)
                requirements.append(temp_list)

            jobs_dict['xp_level'] = xp_level
            jobs_dict['title'] = title
            jobs_dict['link'] = page_link
            jobs_dict['requirements'] = requirements
            jobs_dict['time_created'] = time_created

            if jobs_dict not in vacancies:
                vacancies.append(jobs_dict)

    return vacancies


def writer_file(xp_level: str):
    data = get_data(xp_level)
    id_work = 0
    for el in data:
        id_work += 1
        el['id_work'] = id_work
    with open('some_json.json', 'w') as f:
        json.dump(data, f, indent=4)
        print('Finish write!')


def read_file():
    with open('some_json.json') as f:
        data = json.load(f)
    return data


def main():
    writer_file('no_exp')
    # print(get_data('1y'))
    # print(get_data('1y'))


if __name__ == '__main__':
    main()
