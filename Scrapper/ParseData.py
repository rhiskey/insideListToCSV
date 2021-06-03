import os
import pathlib
import time
import urllib
import urllib.request

from bs4 import BeautifulSoup

from Classes.CSVDoc import CSVDoc
from Classes.Detail import Detail


def process_pages_get_detail(html_names):
    details2return = []

    for index, file in enumerate(html_names):
        filename, file_extension = os.path.splitext(file)
        uuid_file_name = os.path.basename(filename)
        print("{}/{}".format(index, str(len(html_names))))
        html_doc = open(file, encoding='utf-8')
        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding="utf-8")

        card = soup.find_all('div', {"class": "coinfo block-part"})

        id = uuid_file_name
        name = ''
        evidence = ''
        inn = ''
        address = ''
        website = ''

        dict_to_format = {}
        for tag in card:
            cardd = tag.find_all("div", {"class": "coinfo_item row"})

            # rr = cardd.find_next_siblings("div")

            for div in cardd:
                # chld = div.children
                alldivs = div.find_all('div')

                if alldivs[0].text == 'Наименование, знак обслуживания, коммерческое обозначение и иные средства ' \
                                      'индивидуализации лица ':
                    # print('Name: ' + alldivs[1].text)
                    name = alldivs[1].text

                if alldivs[0].text == 'Признаки, установленные Банком России':
                    # print('Evidence: ' + alldivs[1].text)
                    evidence = alldivs[1].text

                if alldivs[0].text == 'ИНН':
                    # print('INN: ' + alldivs[1].text)
                    inn = alldivs[1].text

                if alldivs[0].text == 'Адрес предоставления лицом услуг*':
                    # print('Address: ' + alldivs[1].text)
                    address = alldivs[1].text

                if alldivs[0].text == 'Сайт в сети «Интернет»':
                    # print('Site: ' + alldivs[1].text)
                    website = alldivs[1].text
                # print(alldivs)

        doc = Detail(id, name, evidence, inn, address, website)
        details2return.append(doc)

    return details2return

