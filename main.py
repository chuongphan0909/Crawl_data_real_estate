from enum import Enum
from fastapi import FastAPI

from getData.getDataFromWeb import (
    get_crawl_data_web1, get_crawl_data_web2
)

from mysqlpackage import (
    mydb, table_name
)

from mysqlpackage.gettingMysql import (
    search_area_inrange, write_data,
    search_location, search_area,
    sort_by_infor, search_price_inrange,
    search_general, search_price,
    create_table, get_all_data
)


class unit_price(str, Enum):
    unit1 = 'tỷ'
    unit2 = 'triệu'


class unit_area(str, Enum):
    unit = 'm²'


app = FastAPI()


@app.get('/createtable')
def create_table_db():
    return create_table(mydb, table_name)


@app.get('/updatedata/{number_web}}')
def update_data(number_web: int):
    if number_web == 1:
        data_crawls = get_crawl_data_web1()
    elif number_web == 2:
        data_crawls = get_crawl_data_web2()
    else:
        return 'Not Found'

    for data in data_crawls:
        write_data(mydb, table_name, data)
    return f'Update Data From Web {number_web} Successfully!'


@app.get('/show/all')
def show_all_data():
    return get_all_data(mydb, table_name)


@app.get('/search/location')
def search_by_location(location_: str):
    return search_location(mydb, table_name, location_)


@app.get('/search/area')
def search_by_area(area_: str, unit_: unit_area):
    area_search = area_ + " " + unit_
    return search_area(mydb, table_name, area_search)


@app.get('/search/area_inrange')
def search_by_in_range_area(
        area_min: str, area_max: str,
        unit_: unit_area):

    return search_area_inrange(
            mydb, table_name,
            area_min, area_max, unit_)


@app.get('/search/price')
def search_by_price(price_: str, unit_: unit_price):
    return search_price(mydb, table_name, price_, unit_)


@app.get('/search/price_inrange')
def search_by_in_range_price(
        price_min: str, price_max: str,
        unit_: unit_price):

    return search_price_inrange(
        mydb, table_name,
        price_min, price_max, unit_)


@app.get('/search/general')
def search_by_general(
        area_min: str, area_max: str,
        unit_area_: unit_area, price_min: str,
        price_max: str, unit_price_: unit_price,
        location: str
):
    return search_general(
        mydb, table_name,
        area_min, area_max,
        unit_area_, price_min,
        price_max, unit_price_,
        location)


@app.get('/sort/price')
def sort_by_price(unit_price_: unit_price, column_: str = "Price"):

    return sort_by_infor(
        mydb, table_name,
        column_, unit_price_)


@app.get('/sort/area')
def sort_by_area(unit_area_: unit_area, column_: str = "Area"):

    return sort_by_infor(
        mydb, table_name,
        column_, unit_area_)
