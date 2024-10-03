import logging
import random
import csv
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import re, time, datetime
import unicodedata

from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys


from utils.website_1_functions import create_csv, random_delay, append_to_csv


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__) # CHECK

class TextUtils:
    @staticmethod
    def normalize_text(text: str) -> str:
        """Normalize Unicode text to ASCII."""
        return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')

    @staticmethod
    def clean_text(text: str) -> str:
        """Remove extra whitespace and strip text."""
        return ' '.join(text.split()).strip()

class MilanunciosScraper:
    def __init__(self, url: str, headless: bool = False) -> None:
        self.url = url
        self.driver: Optional[WebDriver] = None        
        self.options = ChromeOptions()
        self.headless = headless
        self._setup_chrome_options()
        # self.config_index = 0  # Add this line to keep track of configuration index

    def _setup_chrome_options(self)-> None:

        prefs = {
            "profile.managed_default_content_settings.images": 2, #Deshabilitar imágenes para mejorar la velocidad de carga
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "profile.managed_default_content_settings.popups": 2,  # Disable popups
            "profile.default_content_setting_values.popups": 2,  # Asegurarse de que los pop-ups estén bloqueados
            }
        
        self.options.add_argument("--no-sandbox")
        self.options.add_argument('--disable-extensions')
        self.options.add_argument('--disable-iframe')
        self.options.add_experimental_option("prefs", prefs) 
        if self.headless:
            self.options.add_argument("--headless")
        else:
            self.options.add_argument("--window-size=1920,1080")

    def initialize_driver(self) -> None:
        """Initialize the Chrome driver with configured options."""
        self.driver = Chrome(options=self.options)

    def open_site(self,file_path) -> None:
        """Navigate to the target website."""
        logger.info(f"Navigating to {self.url}")
        try:
            self.driver.get(self.url)
                      
            try:
                time.sleep(5) 
                self.driver.find_element(By.CSS_SELECTOR, '#captcha-box > div > div.geetest_btn').click()
                logger.info('Closing UPS ...')
            except Exception as e:
                logger.info('Couldnt find any button,', e)
   
            # Accepted cookies
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#didomi-notice-agree-button'))).click()
            self.scroll_page(1, 60)

            # get total number of pages 
            paginas = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[9]')
            numero_de_paginas =  int(paginas[0].text) if paginas[0] else 1
            logger.info(f'Total number of pages: {numero_de_paginas}')
            
            for pagina in range(1, numero_de_paginas+1):
                if pagina == 1:
                    print('Scrapeando página:', pagina)
                    self.scrape_elements(self,file_path)
                    self.next_page(self)
                else:
                    print('Scrapeando página:', pagina)
                    self.scroll_page(self, 1, 23)
                    self.scrape_elements(self,file_path)
                    self.next_page(self)
            
        except Exception as e:
            print(f"Error desconocido: {e}")
        finally:
            # Cerrar el navegador al finalizar
            self.driver.quit()

    def scroll_page(self, scroll_pause_time:int , tiempo_limite=40):
        start_time = time.time()
        logger.info('Scrolling page ...')
        while True:
            self.driver.execute_script("window.scrollBy(0, 500);")  # Hacer scroll hacia abajo
            time.sleep(scroll_pause_time)  # Pausa entre scrolls
            elapsed_time = time.time() - start_time  # Calcular el tiempo transcurrido
            if elapsed_time > tiempo_limite:  # Verificar si se ha alcanzado el tiempo límite
                break  # Salir del bucle si se alcanza el tiempo límite
        
    def next_page(self):
        try:
            # boton_next = driver.find_elements(By.CSS_SELECTOR, '#app > div.ma-LayoutBasic > div.ma-AdvertisementPageLayout.ma-AdvertisementPageLayout-justify--center > div.ma-AdvertisementPageLayout-center > div.ma-LayoutFullHeight > div.ma-LayoutBasic-content.ma-Listing > div > main > nav > ul > li:nth-child(10) > button')
            boton_next = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[last()]')
            boton_next[0].click()
        except Exception as e:
            print('No hay más páginas, o', e)
            return False
        return True   

    def scrape_elements(driver, file_path):
        try:
            elementos = driver.find_elements(By.CSS_SELECTOR, 'div.ma-AdCardV2-upperGroup')
            for elemento in elementos:
                div_text = elemento.get_attribute('outerHTML')
                append_to_csv(file_path, div_text)

            print(f'Cantidad de elementos: {len(elementos)}')
        except NoSuchElementException:
            print('No se encontraron elementos')
            return False
        return True

    def run_scraper(self, file_path: str) -> None:
        """Run the scraper."""
        self.initialize_driver()
        self.open_site(file_path)
        # self.scrape_elements()
        # self.save_data(file_path)

def main():
    url = 'https://www.milanuncios.com/inmobiliaria/?demanda=n&vendedor=part&orden=relevance&fromSearch=1&hitOrigin=listing'
    fecha = datetime.datetime.now().strftime('%Y-%m-%d')
    file_path = f'Raw_Csv/scraping_milanuncios_{fecha}.csv'

    scraper = MilanunciosScraper(url,False)
    scraper.run_scraper(file_path)


if __name__ == '__main__':
    main()