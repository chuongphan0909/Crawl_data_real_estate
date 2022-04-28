from datetime import datetime
import requests
from bs4 import BeautifulSoup


def convert_timeupdate():
    """ Convert keyword Hôm nay to current day """
    list_time = str(datetime.date(datetime.now())).split('-')
    timeupdate = list_time[2] + '/' + list_time[1] + '/' + list_time[0]
    return timeupdate


def find_informations(content_response, content_find, class_):
    """ Find informations from html and return content """

    return BeautifulSoup(content_response, 'lxml').find_all(
            content_find, class_)


def extract_information(container_informations,
                        position, character_split):
    """ Extraction information in containner informations """

    return container_informations[position].text.split(
        character_split)[1].strip()


def get_status_response(link_request):
    """ Read value response from sever """

    return requests.get(link_request).status_code


def get_crawl_data_web1():
    """ Get crawl the data from the website extract
        the information, sort and return all data  """

    page = 1
    all_data = []
    while True:
        link_base = 'https://nhadatcantho.vn/?page='
        link_get_data = link_base + str(page)
        print(f'Crawling data page number {page}')
        content_response = requests.get(link_get_data).text

        if get_status_response(link_get_data) == 200:

            container_title = find_informations(
                content_response, content_find='h3',
                class_='hidden-xs')
            container_price = find_informations(
                content_response, content_find='div',
                class_='price')
            container_area = find_informations(
                content_response, content_find='div',
                class_='area')
            container_location = find_informations(
                content_response, content_find='div',
                class_='location')
            container_date = find_informations(
                content_response, content_find='div',
                class_='date')

            list_informations = []
            for i, item in enumerate(container_title):
                title = item.text
                price = extract_information(
                    container_price, i,
                    character_split=':').split('/')[0]
                area = extract_information(
                    container_area, i,
                    character_split=':')
                location = extract_information(
                    container_location, i,
                    character_split=':')
                date = extract_information(
                    container_date, i,
                    character_split='-')
                list_temp = [title, area, price, location, date, link_get_data]
                list_informations.append(list_temp)
                all_data.append(list_temp)
                del(list_temp)

            page += 1
            if list_informations == []:
                break
        else:
            break

    return all_data


def get_crawl_data_web2():
    """ Get crawl the data from the website extract
        the information, sort and return all data  """

    page = 1
    all_data = []
    while True:

        link_get_data = "https://alonhadat.com.vn/" \
                        + "nha-dat/cho-thue/nha-trong-hem/5/can-tho/trang--" \
                        + str(page) + ".html"
        print(f'Crawling data page number {page}')
        content_response = requests.get(link_get_data).text

        if get_status_response(link_get_data) == 200:

            container_title = find_informations(
                content_response, content_find='div',
                class_='ct_title')
            container_price = find_informations(
                content_response, content_find='div',
                class_='ct_price')
            container_area = find_informations(
                content_response, content_find='div',
                class_='ct_dt')
            container_location = find_informations(
                content_response, content_find='div',
                class_='ct_dis')
            container_date = find_informations(
                content_response, content_find='div',
                class_='ct_date')

            list_informations = []
            for i, item in enumerate(container_title):
                title = item.text
                price = extract_information(
                    container_price, i,
                    character_split=':').split('/')[0]
                area = extract_information(
                    container_area, i,
                    character_split=':')
                location = container_location[i].text
                date = container_date[i].text
                if date == "Hôm nay" or date == "Hôm qua":
                    date = convert_timeupdate()
                list_temp = [title, area, price, location, date, link_get_data]
                list_informations.append(list_temp)
                all_data.append(list_temp)
                del(list_temp)
            # going to next page
            page += 1
            if list_informations == []:
                break
        else:
            break

    return all_data
