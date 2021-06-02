import os
import pathlib
import time

from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver import FirefoxOptions

from Classes.BlackList import BlackList


class SeleniumFirefox(object):
    def __init__(self):
        opts = FirefoxOptions()
        # opts.add_argument("--headless")
        self.driver = webdriver.Firefox(options=opts)
        self.wait = WebDriverWait(self.driver, 10)

    # def login_process(self):
    #     self.driver.get("")
    #
    #     inputElementLogin = self.driver.find_element_by_name("login")
    #     inputElementLogin.send_keys(login)
    #     inputElementPassword = self.driver.find_element_by_name("password")
    #     inputElementPassword.send_keys(pass)
    #     inputElementPassword.submit()
    #
    #     self.wait.until(presence_of_element_located((By.CLASS_NAME, "card-title")))

    def process_list_of_companies(self, companies_class_list: list[BlackList]):
        html_names = []
        for company in companies_class_list:
            self.driver.implicitly_wait(1)
            url = "{}={}".format("https://www.cbr.ru/inside/BlackList/detail/?id", str(company.id))
            self.driver.get(url)
            # info_div = self.driver.find_element_by_id("coinfo block-part")
            # table_load = self.wait.until(
            #         presence_of_element_located((By.CLASS_NAME, "coinfo block-part")))
            # time.sleep(1)

            html_names.append(str(company.id) + '.html')
            path = os.getcwd()
            page_file = pathlib.Path(str(path) + '/details/' + str(company.id) + '.html')
            if page_file.is_file():
                print('file exist: ', str(company.id) + str('.html'))
            else:
                pathlib.Path(str(path) + '/details/').mkdir(parents=True, exist_ok=True)
                fname = str(path) + '/details/' + str(company.id) + '.html'
                with open(fname, 'w', encoding="utf-8") as f:
                    page = self.driver.page_source
                    f.write(page)
        return html_names

    def get_portfolios(self, table_pages_folder_name):
        self.driver.implicitly_wait(5)  # seconds
        self.driver.get("https://portfolio.bmstu.ru/portfolio/index")

        # next_page = self.wait.until(presence_of_element_located((By.ID, "DataTables_Table_0_next")))
        # TODO: rewrite click iteration loop - get pages count
        for x in range(897):
            try:
                print('Current page: ', x)
                next_page_button = self.driver.find_element_by_id('DataTables_Table_0_next').click()  # 897 times
                table_load = self.wait.until(
                    presence_of_element_located((By.CSS_SELECTOR, "#DataTables_Table_0>tbody")))
                time.sleep(2)
            except:
                print('No element on page')

            path = os.getcwd()
            page_file = pathlib.Path(str(path) + '/' + table_pages_folder_name + '/' + str(x) + '.html')
            if page_file.is_file():
                print('file exist: ', str(x) + str('.html'))
            else:
                pathlib.Path(str(path) + "/" + table_pages_folder_name + '/').mkdir(parents=True, exist_ok=True)
                fname = str(path) + "/" + table_pages_folder_name + '/' + str(x) + '.html'
                with open(fname, 'w') as f:
                    f.write(self.driver.page_source)

    def open_profile_page_and_get_info(self, relative, folder_name):
        html_names = []

        for page in relative:
            open_page = "https://portfolio.bmstu.ru" + page
            # self.driver.execute_script("window.open('"+open_page + "');")
            try:
                self.driver.get(open_page)
                time.sleep(0.1)
                page = page.strip('/portfolio/single/')
                html_name = page + '.html'
                html_names.append(html_name)

                path = os.getcwd()
                # Check if already have file  in \singlepages
                my_file = pathlib.Path(str(path) + '/' + folder_name + '/' + html_name)
                if my_file.is_file():
                    print('file exist: ', html_name)
                else:
                    pathlib.Path(str(path) + "/" + folder_name).mkdir(parents=True, exist_ok=True)
                    with open(folder_name + '/' + html_name, 'a') as f:
                        f.write(self.driver.page_source)
            except UnicodeEncodeError:
                print('Unicode err')

        with open("html_names.txt", "w") as txt_file:
            for line in html_names:
                line = folder_name + '/' + line
                txt_file.write("".join(line) + "\n")
        return html_names

    def quit(self):
        self.driver.quit()