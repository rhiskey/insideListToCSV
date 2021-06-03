import csv
import json

from Classes.BlackList import BlackList
from Classes.CSVDoc import CSVDoc


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


def create_csv(inside_list):
    # Remove unused keys
    new_dict_list = []
    for a in inside_list:
        a.pop('__class__')
        a.pop('__module__')
        a.pop('org_id')
        new_dict_list.append(a)

    with open('inside_data.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['name', 'evidence', 'inn', 'address', 'website', 'update_date']
        # header = ['Наименование', 'Признаки', 'ИНН', 'Адрес', 'Сайт', 'Дата добавления']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'name': 'Наименование', 'evidence': 'Признаки', 'inn': 'ИНН', 'address': 'Адрес', 'website': 'Сайт', 'update_date': 'Дата добавления'})
        # writer.writeheader()
        writer.writerows(new_dict_list)


