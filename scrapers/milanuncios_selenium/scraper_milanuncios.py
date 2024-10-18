import logging
import time, datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from scrapers.milanuncios_selenium.utils.milanuncios_functions import create_csv, append_to_csv, random_delay

logger = logging.getLogger(__name__)


class MilanunciosScraper:
    """Class to scrape Milanuncios website using Selenium"""
    def __init__(self, url: str, headless: bool = False) -> None:
        self.url = url
        self.driver = WebDriver # Can be changed to anopther driver if needed, worked with Undetected-Chromedriver too
        self.options = Options()
        self.headless = headless 
        self._setup_chrome_options() # Set up Chrome options

    def _setup_chrome_options(self)-> None:
        """Set up Chrome options for the driver"""
        prefs = {
            "profile.managed_default_content_settings.images": 2, # Disable images to improve load speed
            "profile.default_content_setting_values.notifications": 2,  # Disable notifications
            "profile.managed_default_content_settings.popups": 2,  # Disable popups
            "profile.default_content_setting_values.popups": 2,  # Make sure pop-ups are blocked
            }
        self.options.add_argument("--no-sandbox") # Bypass OS security model
        self.options.add_argument('--disable-extensions') # Disable extensions
        self.options.add_argument('--disable-iframe') # Disable iframes

        self.options.add_experimental_option("prefs", prefs)  # Add preferences

        if self.headless:
            self.options.add_argument("--headless") # Run in headless mode
        else:
            self.options.add_argument("--window-size=1920,1080") # Set window size

    def _initialize_driver(self) -> None:
        """Initialize the Chrome driver with configured options"""
        service = Service()
        return webdriver.Chrome(service=service, options=self.options)

    def open_site(self, file_path:str) -> None:

        """Navigate to the target website."""

        logger.info(f"Navigating to {self.url}")
        try:
            self.driver.get(self.url)
            try:
                time.sleep(5) 
                self.driver.find_element(By.CSS_SELECTOR, '#captcha-box > div > div.geetest_btn').click()
                logger.info('Closing UPS ad')
            except Exception as e:
                logger.warning('Couldnt find any button,', e)
   
            # Accepted cookies 
            # This is an add that used to appear on the website, it is not present anymore
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#didomi-notice-agree-button'))).click()
            self._scroll_page(1, 60)

            # Get total number of pages 
            paginas = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[9]')
            number_of_pages =  int(paginas[0].text) if paginas[0] else 1
            logger.info(f'Total number of pages: {number_of_pages}')
            
            for pagina in range(1, number_of_pages+1):
                random_delay()
                if pagina == 1:
                    logger.info('Scraping page:', pagina)
                    self._scrape_elements(self,file_path)
                    self._next_page(self)
                else:
                    logger.info('Scraping page:', pagina)
                    self._scroll_page(self, 1, 23)
                    self._scrape_elements(self,file_path)
                    self._next_page(self)
            
        except Exception as e:
            logger.warning(f"Error navigating to {self.url}: {e}")
        finally:
            self.driver.quit()

    def _scroll_page(self, scroll_pause_time:int , limit_time=40):
        start_time = time.time()
        logger.info('Scrolling page ...')
        while True:
            self.driver.execute_script("window.scrollBy(0, 500);")  # Scroll down
            time.sleep(scroll_pause_time)  # Wait for the page to load
            elapsed_time = time.time() - start_time  #  Calculate elapsed time
            if elapsed_time > limit_time:  # Exit the loop if the time limit is reached
                break

    def _next_page(self):
        try:
            # boton_next = driver.find_elements(By.CSS_SELECTOR, '#app > div.ma-LayoutBasic > div.ma-AdvertisementPageLayout.ma-AdvertisementPageLayout-justify--center > div.ma-AdvertisementPageLayout-center > div.ma-LayoutFullHeight > div.ma-LayoutBasic-content.ma-Listing > div > main > nav > ul > li:nth-child(10) > button')
            boton_next = self.driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[last()]')
            boton_next[0].click()
        except Exception as e:
            logger.warning(f"Error navigating to next page: {e}")


    def _scrape_elements(self, file_path):
        try:
            elements = self.driver.find_elements(By.CSS_SELECTOR, 'div.ma-AdCardV2-upperGroup')
            for element in elements:
                div_text = element.get_attribute('outerHTML')
                append_to_csv(file_path, div_text)
            logger.info(f'Number of elements: {len(elements)}')
        except NoSuchElementException:
            logger.warning('No elements found')

    def run_scraper(self, file_path: str) -> None:
        """Run the scraper."""
        try:
            fecha = datetime.datetime.now().strftime('%Y-%m-%d') # Get current date
            file_path = f'Raw_Csv/scraping_milanuncios_{fecha}.csv' # Set file path
            
            create_csv(file_path)
            self._initialize_driver() # Initialize the driver opening a new window
            self.open_site(file_path)

        except Exception as e:
            logger.warning(f"Error running scraper: {e}")