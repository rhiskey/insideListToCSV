import csv
import requests
import json
import pathlib
from os import listdir
from os.path import isfile, join
from pathlib import Path
from datetime import datetime

from Classes.CSVDoc import CSVDoc, CSVDocEncoder
from Scrapper.ScrapCompaniesDetails import SeleniumFirefox
from Classes.BlackList import blacklist_json_decode, BlackList
from Scrapper.ParseData import process_pages_get_detail
from Utils.JsonTool import convert_to_dict, dict_to_obj

path = pathlib.Path(__file__).parent.absolute()


def get_blacklist():
    # PageSize - can be
    url = "https://www.cbr.ru/inside/BlackList/datasource/?page=0&dateFrom=&dateTo=&SPhrase=&PageSize=5000&Thema=-1&_" \
          "=1622632910146 "

    payload = {}
    headers = {
        'Cookie': '__ddg1=nXPG2fVqGNCQ6C651Dze; __ddgid=SzRDQRt0QWRaUPxF; __ddgmark=yTdrHIeuPIw8wmwD'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


def decode_json(json_string):
    dev_dict = json.loads(json_string)
    count = dev_dict["Counter"][0]['sm']
    data_dict = dev_dict["Data"]
    # dev_dict = json.loads(data_dict, object_hook=blacklist_json_decode)
    bl_list = []

    for company in data_dict:
        comp_obj = BlackList(company['id'], company['DT'], company['nameOrg'])
        # print(company['nameOrg'])
        bl_list.append(comp_obj)

    return bl_list


def create_csv():
    with open('.csv', 'w', newline='') as csvfile:
        file_writer = csv.writer(csvfile, delimiter=',', lineterminator="\r",
                                 quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(["Имя", "Класс", "Возраст"])
        file_writer.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])


def extend_details_with_date(detail_class_list, blacklist_class_list):
    ext_list = []
    for dc in detail_class_list:
        # csv_class_obj = CSVDoc('', '', '', '', '', '', '')
        for bc in blacklist_class_list:
            if int(dc.org_id) == bc.id:
                # datetime_object = datetime.strptime(bc.DT, "%Y-%m-%dT%H:%M:%S")
                csv_class_obj = CSVDoc(bc.id, dc.name, dc.evidence, dc.inn, dc.address, dc.website, bc.DT)
                ext_list.append(csv_class_obj)
    return ext_list


if __name__ == '__main__':
    # resp = get_blacklist()
    # bl_class_list = decode_json(resp)

    # # Check if bl_class_list.count != count from Mongo -> compare id's, load missing

    # # Scrap details
    # browser = SeleniumFirefox()
    # pages_list = browser.process_list_of_companies(bl_class_list)
    # browser.quit()

    # # Process details page
    # pages_path = Path(str(path) + "/"  'details' + "/")
    # Path(str(path) + "/" + 'details').mkdir(parents=True, exist_ok=True)
    # singlePages = [f for f in listdir(pages_path) if isfile(join(pages_path, f))]
    # relative_single_pages = []
    # for file in singlePages:
    #     file = 'details' + '/' + file
    #     relative_single_pages.append(file)
    #
    # details_bl = process_pages_get_detail(relative_single_pages)
    # ext_csvdoc_class = extend_details_with_date(details_bl, bl_class_list)
    #
    # # Save info in MONGO/Json
    # with open('inside.json', 'w', encoding='utf-8') as outfile:
    #     # data = json.dumps(filtered_users, default=convert_to_dict, indent=4, sort_keys=True)
    #     json.dump(ext_csvdoc_class, outfile, cls=CSVDocEncoder, default=convert_to_dict, indent=4, sort_keys=True,
    #               ensure_ascii=False)
    #     dict_lst = []
    #     for u in ext_csvdoc_class:
    #         dc = vars(u)
    #         dict_lst.append(dc)
    #     # insert_multiple_to_Mongo(dict_lst)

    # Read From json file
    with open('inside.json', 'r', encoding='utf-8') as json_file:
        insides_ = json.loads(json_file.read(), object_hook=dict_to_obj)
        print(insides_)
        # dict_lst = []
        # for u in insides_:
        #     dc = vars(u)
        #     dict_lst.append(dc)
        # insert_multiple_to_Mongo(dict_lst)

    # # Read from Mongo
    # insides_mongo = read_users_from_Mongo()
    # insides_ = []
    # for u in insides_mongo:
    #     cls = dict_to_obj(u)
    #     users_.append(cls)

    # # Save insides_ to CSV
