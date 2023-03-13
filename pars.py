import json
import requests
from bs4 import BeautifulSoup
import time
from settings import params, cookies, headers


def get_data(xp_level: str):
    """
    simple_input = ['no_exp', '1y', '2y', '3y', '4y', '5y']
    at the output list
    """
    jobs = []
    id_work = 0

    url_djinni = f"https://djinni.co/jobs/?primary_keyword=Python&region=UKR&exp_level={xp_level}"
    count_page = 1

    s = requests.Session()
    response = s.get(url=url_djinni, params=params, cookies=cookies, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')

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
            id_work += 1
            link = div.a.get('href')
            title = div.span.text
            page_link = 'https://djinni.co' + link

            req = s.get(page_link, params=params, cookies=cookies, headers=headers)
            soap = BeautifulSoup(req.text, 'lxml')
            toolbar = soap.find_all('li', class_="job-additional-info--item")

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

            jobs_dict['id_work'] = id_work
            jobs_dict['title'] = title
            jobs_dict['link'] = page_link
            jobs_dict['requirements'] = requirements
            jobs.append(jobs_dict)

    return jobs


def writer_file(xp_level: str):
    data = get_data(xp_level)
    with open('some_json.json', 'w') as f:
        json.dump(data, f, indent=4)


def main():
    get_data('1y')


if __name__ == '__main__':
    main()
