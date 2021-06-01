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
        name = ''
        evidence = ''
        inn = ''
        address = ''
        website = ''

        for tag in card:
            cardd = tag.find_all("div", {"class": "coinfo_item row"})

            for tag2 in cardd:
                divs = tag2.find_all("div", {"class": "coinfo_item_text col-md-13 offset-md-1"})
                evidence = divs[1].text
                inn = divs[2].text
                address = divs[3].text
                website = divs[3].text

        doc = Detail(name, evidence, inn, address, website)
        details2return.append(doc)

    return details2return

