from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
from config import *
import pandas as pd
import os
import json


class ExtraccionInsuma:
    """
    # SCRAPING WEB OBUMA
    
    Extractor de información de la página obuma a través de la librería "Selenium".

    ## Principales objetivos:
    
        - Extraer la información de las notas de ventas emitidas por la empresa.
        - Análisis de las ventas realizadas pro cliente.
    
    ## Objetivos mas adelante con el código:

        - extraer otras áreas de la empresa (Logística, Comrpas, Requerimientos entre otros).

    """
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(options=self.config_driver())
        self.username, self.password = self._get_credencials()

    def _get_credencials(self):
        """
        Método para extraer las credenciales de Obuma.
        """
        try:
            with open(os.path.join("secrets", "secrets.json")) as file:
                credencials = json.load(file)
                return credencials["user"], credencials["password"]
        except FileExistsError:
            print("No se encontró el archivo de credenciales")
            return None, None
        except json.JSONDecodeError:
            print("Error con el archivo de credenciales")
            return None, None


    def config_driver(self):
        """
        Configura las opciones del driver de Chrome.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")  
        # chrome_options.add_argument("--disable-gpu")
        return chrome_options

    def login_obuma(self):
        """
        Método para iniciar sesión en la plataforma de Insuma.
        """
        try:
            self.driver.get(URL_INSUMA)
            self.driver.find_element(By.ID, "idLogin").send_keys(self.username)
            self.driver.find_element(By.ID, "idPassword").send_keys(self.password)
            self.driver.find_element(By.CLASS_NAME, "btn-yellow").click()
        except Exception as e:
            print(f"error al iniciar sesión: {e}") 

    def sales_extractor(self):
        """
        Método para extraer las ventas de Insuma.
        """
        try:    
            self.driver.find_element(By.XPATH, '//*[@id="mainSideMenu"]/li[2]/div/a').click()
            self.driver.find_element(By.XPATH, '//*[@id="accComponents"]/li[3]/a[2]').click()
            muestra = self.driver.find_element(By.ID, "_pagi_cuantos")
        except Exception as e:
            print(f"error al extraer las ventas: {e}")

    def download_table(self):
        """
        Metodo para extraer la tabla de ventas de Insuma.
        >>> return: DataFrame con la información de las ventas.
        """
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

        return df

    def main(self):
        """
        Función principal para la extracción de las ventas de Insuma.
        """
        self.login_obuma()
        self.sales_extractor()
        df = self.download_table()
        self.driver.quit()
        return df

if __name__=="__main__":

    scraper = ExtraccionInsuma()
    try:
        df = scraper.main()
        df.to_excel("download\\ventas_insuma.xlsx", index=False)
    except Exception as e:
        print(f"error con el scraping: {e}")
    finally:
        scraper.driver.quit()