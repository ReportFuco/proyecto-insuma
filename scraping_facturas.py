from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import pandas as pd
import json


class ExtraccionInsuma:

    def __init__(self) -> None:
        self.driver = webdriver.Chrome(options=self.config_driver())

    def _get_credencials(self):
        
        with open(r"credencials\obuma.json") as file:
            return json.load(file)

    def config_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        # chrome_options.add_argument("--disable-gpu")

        return chrome_options

    def login_obuma(self):
        self.driver.get("https://app.obuma.cl/obuma2.0/")
        self.driver.find_element(By.ID, "idLogin").send_keys(self._get_credencials()["user"])
        self.driver.find_element(By.ID, "idPassword").send_keys(self._get_credencials()["password"])
        self.driver.find_element(By.CLASS_NAME, "btn-yellow").click()

    def sales_extractor(self):
        
        self.driver.find_element(By.XPATH, '//*[@id="mainSideMenu"]/li[2]/div/a').click()
        self.driver.find_element(By.XPATH, '//*[@id="accComponents"]/li[3]/a[2]').click()
        
        muestra = self.driver.find_element(By.ID, "_pagi_cuantos")
        Select(muestra).select_by_index(9)
        
    def download_table(self):
        
        table = self.driver.find_element(By.CSS_SELECTOR, 'table.table-striped')
        headers = [header.text for header in table.find_elements(By.TAG_NAME, "th")]
        rows = table.find_elements(By.TAG_NAME, "tr")
        table_data = [[cell.text for cell in row.find_elements(By.TAG_NAME, "td")] for row in rows if row.find_elements(By.TAG_NAME, "td")]

        df = pd.DataFrame(table_data, columns=headers)
        df.drop(columns=['', "ACCIONES"], inplace=True)
        df["TOTAL"] = df["TOTAL"].str.replace("$ ", "")
        df["NETO"] = df["NETO"].str.replace("$ ", "")

        df["TOTAL"] = df["TOTAL"].str.replace(".", "")
        df["NETO"] = df["NETO"].str.replace(".", "")

        for serie in ["TOTAL", "NETO", "FOLIO"]:
            df[serie] = df[serie].astype(int)

        self.driver.quit()

        return df


def extraccion_obuma():

    driver = ExtraccionInsuma()
    driver.login_obuma()
    driver.sales_extractor()
    return driver.download_table()

