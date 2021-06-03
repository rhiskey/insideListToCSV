import csv
import os

import requests
import json
import pathlib
import logging

from os import listdir
from os.path import isfile, join
from pathlib import Path
from datetime import datetime

from Classes.CSVDoc import CSVDoc, CSVDocEncoder
from Scrapper.ScrapCompaniesDetails import SeleniumFirefox
from Classes.BlackList import blacklist_json_decode, BlackList
from Scrapper.ParseData import process_pages_get_detail
from Utils.Helpers import extend_details_with_date, decode_json, create_csv
from Utils.JsonTool import convert_to_dict, dict_to_obj
from config import blacklist_url

# path = pathlib.Path(__file__).parent.absolute()
path = os.getcwd()


def get_blacklist():
    # PageSize - can be
    url = blacklist_url

    payload = {}
    headers = {
        'Cookie': '__ddg1=nXPG2fVqGNCQ6C651Dze; __ddgid=SzRDQRt0QWRaUPxF; __ddgmark=yTdrHIeuPIw8wmwD'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.text


if __name__ == '__main__':
    logging.basicConfig(filename='inside.log', level=logging.INFO)

    cpath = os.getcwd()
    # logging.debug(cpath)
    print(os.getcwd())
    # logging.debug('Started')
    logging.info('Get List')

    resp = get_blacklist()
    bl_class_list = decode_json(resp)
    # logging.debug(bl_class_list)

    # # # TODO: Check if bl_class_list.count != count from Mongo -> compare id's, load missing

    # # Scrap details
    logging.debug('Scrapping details')
    browser = SeleniumFirefox()
    pages_list = browser.process_list_of_companies(bl_class_list)
    browser.quit()

    # Process details page
    try:
        logging.debug('Processing details')
        pages_path = os.path.join(cpath, "details")
        # pages_path = pathlib.Path(os.path.dirname(os.path.abspath(__file__)) + "/"  "details" + "/")
        print(pages_path)
        logging.debug(pages_path)
        pathlib.Path(str(cpath) + "/" + 'details').mkdir(parents=True, exist_ok=True)
        singlePages = [f for f in listdir(pages_path) if isfile(join(pages_path, f))]
        # print(singlePages)
        relative_single_pages = []
        for file in singlePages:
            file = os.path.join(pages_path, file)
                # .Path(str(path) + "/" 'details' + '/' + file)
            relative_single_pages.append(file)
        print(relative_single_pages)
        logging.debug(relative_single_pages)
        details_bl = process_pages_get_detail(relative_single_pages)
        ext_csvdoc_class = extend_details_with_date(details_bl, bl_class_list)
    except Exception as e:
        logging.exception(e)
        exit(1)

    # Save info in MONGO/Json
    try:
        logging.debug('Saving details to inside.json')
        with open(os.path.join(cpath, "inside.json"), 'w', encoding='utf-8') as outfile:
            # data = json.dumps(filtered_users, default=convert_to_dict, indent=4, sort_keys=True)
            json.dump(ext_csvdoc_class, outfile, cls=CSVDocEncoder, default=convert_to_dict, indent=4, sort_keys=True,
                      ensure_ascii=False)
            dict_lst = []
            for u in ext_csvdoc_class:
                dc = vars(u)
                dict_lst.append(dc)
    except Exception as e:
        logging.exception(e)
        exit(2)

    # # TODO: MongoDB
    # # insert_multiple_to_Mongo(dict_lst)

    # Read From json file
    try:
        logging.debug('Reading inside.json')
        dict_lst = []
        with open(os.path.join(cpath, "inside.json"), 'r', encoding='utf-8') as json_file:
            insides_ = json.loads(json_file.read(), object_hook=dict_to_obj)
            for ins in insides_:
                # Preprocess
                ins.address = ins.address.replace('\n', '')
                ins.evidence = ins.evidence.replace('\"', '')
                # Trim time from datetime
                datetime_object = datetime.strptime(ins.update_date, "%Y-%m-%dT%H:%M:%S")
                ins.update_date = datetime_object.strftime("%d.%m.%Y")
            for u in insides_:
                dc = vars(u)
                dict_lst.append(dc)
            # insert_multiple_to_Mongo(dict_lst)
    except Exception as e:
        logging.exception(e)
        exit(3)

    # # TODO: Read from Mongo
    # insides_mongo = read_users_from_Mongo()
    # insides_ = []
    # for u in insides_mongo:
    #     cls = dict_to_obj(u)
    #     users_.append(cls)

    # # Save insides_ to CSV
    try:
        logging.debug('Saving as CSV')
        create_csv(dict_lst)
    except Exception as e:
        logging.exception(e)
        exit(4)

    # Stop console collapse
    # s = input('--> ')

