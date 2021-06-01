import csv
import requests
import json
import pathlib
from os import listdir
from os.path import isfile, join
from pathlib import Path

from Scrapper.ScrapCompaniesDetails import SeleniumFirefox
from Classes.BlackList import blacklist_json_decode, BlackList
from Scrapper.ParseData import process_pages_get_detail

path = pathlib.Path(__file__).parent.absolute()


def get_blacklist():
    url = "https://www.cbr.ru/inside/BlackList/datasource/?page=0&dateFrom=2021-06-01&dateTo=2022-02-01&SPhrase" \
          "=&PageSize=5000&Thema=-1&_=1622552351973 "

    payload = {}
    headers = {
        'Cookie': '__ddg1=nXPG2fVqGNCQ6C651Dze'
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


if __name__ == '__main__':
    resp = get_blacklist()
    bl_class_list = decode_json(resp)

    # browser = SeleniumFirefox()
    # pages_list = browser.process_list_of_companies(bl_class_list)
    # browser.quit()

    # # Process details page
    pages_path = Path(str(path) + "/"  'details' + "/")
    Path(str(path) + "/" + 'details').mkdir(parents=True, exist_ok=True)
    singlePages = [f for f in listdir(pages_path) if isfile(join(pages_path, f))]
    relative_single_pages = []
    for file in singlePages:
        file = 'details' + '/' + file
        relative_single_pages.append(file)

    details_bl = process_pages_get_detail(relative_single_pages)

