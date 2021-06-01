import os
import pathlib
import time
import urllib
import urllib.request

from bs4 import BeautifulSoup


def process_pages_get_detail(html_names):
    details2return = []

    for index, file in enumerate(html_names):
        filename, file_extension = os.path.splitext(file)
        uuid_file_name = os.path.basename(filename)
        print("{}/{}".format(index, str(len(html_names))))
        html_doc = open(file, encoding='utf-8')
        soup = BeautifulSoup(html_doc, 'html.parser', from_encoding="utf-8")

        card = soup.find_all('div', {"class": "coinfo block-part"})
        img_url = ''
        alt = ''
        birth_date = ''
        education = ''
        group = ''
        uuid = uuid_file_name

        for tag in card:
            cardd = tag.find_all("div", {"class": "card"})
            img = tag.find_all("img")
            src = img[0].attrs['src']
            alt = img[0].attrs['alt']

            if src != "/static/lks/images/profile.png":
                # img_url = src
                img_url = 'https://portfolio.bmstu.ru' + src
            for tag2 in cardd:
                date_educ_group = tag2.find_all("h6", {"class": "card-subtitle"})
                birth_date = date_educ_group[1].text
                education = date_educ_group[2].text
                group = date_educ_group[3].text

        user = PortfolioUser(alt, img_url, birth_date, education, group, uuid)
        details2return.append(user)

    return details2return