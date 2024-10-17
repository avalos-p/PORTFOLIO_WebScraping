import logging
import time
import datetime
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from utils.website_1_functions import append_to_csv

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MilanunciosScraper:
    def __init__(self, url: str, headless: bool = False) -> None:
        self.url = url
        self.driver: Optional[WebDriver] = None
        self.options = ChromeOptions()
        self.headless = headless
        self._setup_chrome_options()

    def _setup_chrome_options(self) -> None:
        prefs = {
            "profile.managed_default_content_settings.images": 2,
            "profile.default_content_setting_values.notifications": 2,
            "profile.managed_default_content_settings.popups": 2,
            "profile.default_content_setting_values.popups": 2,
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
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.options)
        self.driver.maximize_window()

    def open_site(self, file_path: str) -> None:
        logger.info(f"Navigating to {self.url}")
        try:
            self.driver.get(self.url)
            self._handle_captcha()
            self.scroll_page(1, 60)
            numero_de_paginas = self._get_total_pages()
            
            for pagina in range(1, numero_de_paginas + 1):
                logger.info(f'Scraping page: {pagina}')
                self.scroll_page(1, 23)
                self.scrape_elements(file_path)
                if not self.next_page():
                    break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
        finally:
            self.driver.quit()

    def _handle_captcha(self) -> None:
        try:
            time.sleep(5)
            self.driver.find_element(By.CSS_SELECTOR, '#captcha-box > div > div.geetest_btn').click()
            logger.info('Closing UPS ...')
        except Exception as e:
            logger.info(f'Could not find any button: {e}')

    def _get_total_pages(self) -> int:
        paginas = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[9]')
        numero_de_paginas = int(paginas[0].text) if paginas else 1
        logger.info(f'Total number of pages: {numero_de_paginas}')
        return numero_de_paginas

    def scroll_page(self, scroll_pause_time: int, tiempo_limite: int = 40) -> None:
        start_time = time.time()
        logger.info('Scrolling page ...')
        while time.time() - start_time < tiempo_limite:
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(scroll_pause_time)

    def next_page(self) -> bool:
        try:
            boton_next = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[last()]')
            boton_next[0].click()
            return True
        except Exception as e:
            logger.info(f'No more pages, or {e}')
            return False

    def scrape_elements(self, file_path: str) -> bool:
        try:
            elementos = self.driver.find_elements(By.CSS_SELECTOR, 'div.ma-AdCardV2-upperGroup')
            for elemento in elementos:
                div_text = elemento.get_attribute('outerHTML')
                append_to_csv(file_path, div_text)
            logger.info(f'Number of elements: {len(elementos)}')
            return True
        except NoSuchElementException:
            logger.info('No elements found')
            return False

    def run_scraper(self, file_path: str) -> None:
        self.initialize_driver()
        self.open_site(file_path)

def main():
    url = 'https://www.milanuncios.com/inmobiliaria/?demanda=n&vendedor=part&orden=relevance&fromSearch=1&hitOrigin=listing'
    fecha = datetime.datetime.now().strftime('%Y-%m-%d')
    file_path = f'Raw_Csv/scraping_milanuncios_{fecha}.csv'

    scraper = MilanunciosScraper(url, False)
    scraper.run_scraper(file_path)

if __name__ == '__main__':
    main()