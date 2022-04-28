from operator import itemgetter


select_command = "SELECT * FROM "
column_infor = ['Id', 'Title', 'Area', 'Price'] \
            + ['Location', 'TimeUpdate', 'Address']
unit_price = ['tỷ', 'triệu']


def check_unit(unit1_, unit2_):
    if unit1_.upper() == unit2_.upper():
        return True
    return False


def convert_list_dictionary(lists_convert):
    """ conver list to dictionary and append to list_informations """
    keys_dic = column_infor
    list_informations = []
    for infor in lists_convert:
        dic_ = dict(zip(keys_dic, infor))
        list_informations.append(dic_)

    return list_informations


def convert_value_by_unit(value_, unit_):
    if check_unit(unit_, unit_price[0]):
        return value_*pow(10, 9)
    elif check_unit(unit_, unit_price[1]):
        return value_*pow(10, 6)
    else:
        return "Unit is not exists"


def get_value_dic(dic_, key_):
    """Convert value in dictionary to float
        Example: 2,4 -> 2.4
    """
    lis_price = dic_.get(key_).strip().split(' ')[0].split(',')
    if len(lis_price) > 1:
        value = float(lis_price[0] + '.' + lis_price[1])
    else:
        value = float(lis_price[0])
    return value


def get_unit(dic_, key_):
    return dic_.get(key_).strip().split(' ')[1]


def sort_list_dic(list_dic, column_sort):
    key_sort = 'order'
    for i, infor in enumerate(list_dic):
        infor_sort = get_value_dic(infor, column_sort)
        list_dic[i][key_sort] = infor_sort
    list_dic.sort(key=itemgetter(key_sort))
    for i in range(len(list_dic)):
        del list_dic[i][key_sort]
    return list_dic


def run_command_sql(my_database, command):
    """ Run Mysql command """
    my_cursor = my_database.cursor()
    my_cursor.execute(command)
    return my_cursor


def get_result_exe(my_database, command):
    """ Get Result return from execute """
    my_cursor = my_database.cursor()
    my_cursor.execute(command)
    results = my_cursor.fetchall()
    return convert_list_dictionary(results)


def recommend_user(results_, unit_):
    min_ = pow(10, 10)
    recommend_item = None
    for i, dic_infor in enumerate(results_):
        unit_dic = get_unit(dic_infor, column_infor[3])
        if check_unit(unit_dic, unit_):
            temp = get_value_dic(dic_infor, column_infor[3])
            price_ = convert_value_by_unit(temp, unit_)
            area_ = get_value_dic(dic_infor, column_infor[2])
            p_div_a = price_/area_
            if min_ > p_div_a:
                min_ = p_div_a
                recommend_item = dic_infor
    return recommend_item


def recommend_and_search(results_, unit_):
    recommend_item = recommend_user(results_, unit_)
    return {"Recommend For User By Price/Area ": recommend_item,
            "Results Search ": results_}


def create_table(my_database, table_name_create):
    """ Create table in database """
    command_sql = "CREATE TABLE " + table_name_create + "("  \
        + "Id MEDIUMINT NOT NULL AUTO_INCREMENT," \
        + "Title TEXT, Area VARCHAR(255)," \
        + "Price VARCHAR(255), Location VARCHAR(255),"  \
        + "TimeUpdate VARCHAR(255), Address VARCHAR(255),"  \
        + "PRIMARY KEY(Id))"

    try:
        run_command_sql(my_database, command_sql)
        return "Create table successfully!"
    except Exception:
        return "Table is exsist"


def check_empty(arr):
    if arr == []:
        return True
    return False


def check_data(my_database, table_name_, values_):
    """ Check if the data exists in the database
        Then return False
        Else return True
    """
    command_check = select_command + table_name_ + " WHERE "   \
        + "Title = " + "'" + values_[0] + "'" + " AND "   \
        + "Area = " + "'" + values_[1] + "'" + " AND "   \
        + "Price = " + "'" + values_[2] + "'" + " AND "   \
        + "Location = " + "'" + values_[3] + "'" + " AND "   \
        + "TimeUpdate = " + "'" + values_[4] + "'" + " AND "   \
        + "Address = " + "'" + values_[5] + "'"

    if get_result_exe(my_database, command_check) != []:
        return False
    else:
        return True


def get_all_data(my_database, table_name_):
    command_get_data = select_command + table_name_
    return get_result_exe(my_database, command_get_data)


def write_data(my_database, table_name_, values):
    """ Write information in datatabase """
    if check_data(my_database, table_name_, values):
        command_write = "INSERT INTO " + table_name_    \
                        + "(Title, Area, Price, "   \
                        + "Location, TimeUpdate, Address) " \
                        + "VALUES(%s, %s, %s, %s, %s, %s)"

        my_database.cursor().execute(command_write, values)
        my_database.commit()
        return "Writting data to Database successfully!"
    else:
        return "Data exsist in database and not update"


def find_area_max(list_dic):
    """ Find real estate have area biggest """
    max_area = -1
    recommend_item = None
    for i, infor in enumerate(list_dic):
        area = get_value_dic(infor, column_infor[2])
        if max_area < area:
            max_area = area
            recommend_item = infor
    return recommend_item


def search_location(
        my_database, table_name_,
        location_search):
    """ Search information real estate with location """
    command_location = select_command + table_name_   \
        + " WHERE Location LIKE " + "'"    \
        + "%" + location_search + "%" + "'"
    results = get_result_exe(my_database, command_location)
    if check_empty(results):
        return results
    return recommend_and_search(results, unit_price[0])


def search_area(my_database, table_name_, area_search):
    """ Search information real estate with area """
    command_area = select_command + table_name_   \
        + " WHERE Area LIKE " + "'"    \
        + area_search + "%" + "'"
    results = get_result_exe(my_database, command_area)
    if check_empty(results):
        return results
    return recommend_and_search(results, unit_price[0])


def search_area_inrange(
        my_database, table_name_,
        area_min, area_max,
        unit):
    command_area = select_command + table_name_   \
                + " WHERE Area >= " + area_min  \
                + " AND Area <= " + area_max  \
                + " AND Area LIKE '%" + unit + "%'"  \
                + " ORDER BY Area"

    results_search = get_result_exe(my_database, command_area)
    if check_empty(results_search):
        return results_search
    results_sort = sort_list_dic(results_search, column_infor[2])
    if len(results_sort) > 5:
        area_bigs = results_sort[len(results_sort)-5:]
    else:
        area_bigs = results_sort
    recommend_item1 = recommend_user(area_bigs, unit_price[0])
    recommend_item2 = recommend_user(results_search, unit_price[0])
    return {"Recommend For User By Big Area ": recommend_item1,
            "Recommend For User By Price/Area ": recommend_item2,
            "Results Search ": results_search}


def output_search_price(list_dic):
    """  Output for search by price """
    if check_empty(list_dic):
        return list_dic
    area_max = find_area_max(list_dic)
    recommend_item = recommend_user(list_dic, unit_price[0])
    return {"Recommend For User By Biggest Area ": area_max,
            "Recommend For User By Price/Area": recommend_item,
            "Results Search": list_dic}


def search_price(
        my_database, table_name_,
        price_search, unit):
    """ Search information real estate with price abd unit """
    command_price = select_command + table_name_   \
        + " WHERE Price LIKE " + "'"    \
        + price_search + "%'"    \
        + " AND Price LIKE " + "'%" \
        + unit + "%'" + " ORDER BY Price"

    results = []
    for dic_ in get_result_exe(my_database, command_price):
        # get price return from database
        price = get_value_dic(dic_, column_infor[3])
        if price == float(price_search):
            results.append(dic_)
    return output_search_price(results)


def search_price_inrange(
        my_database, table_name_,
        price_min, price_max,
        unit):
    """ Search information real estate with price abd unit"""
    command_price = select_command + table_name_   \
        + " WHERE Price " + ">= "  \
        + price_min + " AND Price <= "  \
        + price_max + " AND Price LIKE "    \
        + "'%" + unit + "%' ORDER BY Price"
    results = get_result_exe(my_database, command_price)
    return output_search_price(results)


def search_general(
        my_database, table_name_,
        area_min, area_max,
        unit_area, price_min,
        price_max, unit_price,
        location):
    """ Search real estate with informations """
    command = select_command + table_name_   \
        + " WHERE Price >= "  \
        + price_min + " AND Price <="   \
        + price_max + " AND "   \
        + "Price LIKE " + "'%" \
        + unit_price + "%'"  \
        + " AND Area >= " + area_min   \
        + " AND Area <= " + area_max   \
        + " AND Area LIKE '%" + unit_area   \
        + "%' AND Location LIKE '"   \
        + "%" + location + "%'"
    results = get_result_exe(my_database, command)
    return output_search_price(results)


def sort_by_infor(my_database, table_name_, column_sort, unit_):
    """ Sort real estate by column_sort """
    all_data = get_all_data(my_database, table_name_)
    element_common_unit = []
    for data in all_data:
        unit = data.get(column_sort).strip().split(' ')[1]
        if check_unit(unit, unit_):
            element_common_unit.append(data)
    del(all_data)
    return sort_list_dic(element_common_unit, column_sort)
