import re, time, datetime
import pandas as pd
from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

from utils.milanuncios_functions import create_csv, random_delay, append_to_csv

options = ChromeOptions()
# options.add_argument("--headless")  # Ejecutar en modo sin ventana
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--disable-extensions')
options.add_argument('--disable-iframe')

prefs = {
    "profile.managed_default_content_settings.images": 2, #Deshabilitar imágenes para mejorar la velocidad de carga
    "profile.default_content_setting_values.notifications": 2,  # Disable notifications
    "profile.managed_default_content_settings.popups": 2,  # Disable popups
    "profile.default_content_setting_values.popups": 2,  # Asegurarse de que los pop-ups estén bloqueados
    }
options.add_experimental_option("prefs", prefs)

url = 'https://www.milanuncios.com/inmobiliaria/?demanda=n&vendedor=part&orden=relevance&fromSearch=1&hitOrigin=listing'

fecha = datetime.datetime.now().strftime('%Y-%m-%d')
csv_path = f'csv/scraping_milanuncios_{fecha}.csv'

create_csv(csv_path)

driver = Chrome(options=options)

def open_site(url:str):
    assert isinstance(url, str), 'url must be a string'

    """
    Abre el navegador y navega a la URL de habitaclia.
    Ejecuta el scraping de la página principal y de las comarcas.
    """

    try:
        driver.set_window_position(2000, 0)
        driver.maximize_window()

        print('Dirigiendo a la página: ',url)
        driver.get(url)

        random_delay()
        # Cierro el UPS
        print('Cierro UPS')
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#captcha-box > div > div.geetest_btn'))).click()

        # Hago click en aceptar cookies
        #WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#didomi-notice-agree-button'))).click()

        # Hago click en saltar filtro
        print('Salteo Filtro')
        #WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#react-joyride-step-0 > div > div > div.ma-SharedCoachmark-tooltip > div.ma-SharedCoachmark-tooltipCloseButtonContainer > button'))).click() 
        
        # Scrolleo hasta el final de la página, esto carga los anuncios
        scroll_page(driver, 1, 60)

        # Obtengo la cantidad dotal de paginas ###
        paginas = driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[9]')
        numero_de_paginas =  int(paginas[0].text) if paginas[0] else 1

        print(f'Cantidad de páginas: {numero_de_paginas}')
        
        for pagina in range(1, numero_de_paginas+1):
            if pagina == 1:
                print('Scrapeando página:', pagina)
                scrape_elements(driver)
                next_page(driver)
            else:
                print('Scrapeando página:', pagina)
                scroll_page(driver, 1, 23)
                scrape_elements(driver)
                next_page(driver)
        
    except Exception as e:
        print(f"Error desconocido: {e}")
    finally:
        # Cerrar el navegador al finalizar
        driver.quit()


def scroll_page(driver, scroll_pause_time, tiempo_limite=40):
    start_time = time.time()  # Tiempo de inicio
    while True:
        driver.execute_script("window.scrollBy(0, 500);")  # Hacer scroll hacia abajo
        time.sleep(scroll_pause_time)  # Pausa entre scrolls
        elapsed_time = time.time() - start_time  # Calcular el tiempo transcurrido
        if elapsed_time > tiempo_limite:  # Verificar si se ha alcanzado el tiempo límite
            break  # Salir del bucle si se alcanza el tiempo límite

def next_page(driver):
    try:
        # boton_next = driver.find_elements(By.CSS_SELECTOR, '#app > div.ma-LayoutBasic > div.ma-AdvertisementPageLayout.ma-AdvertisementPageLayout-justify--center > div.ma-AdvertisementPageLayout-center > div.ma-LayoutFullHeight > div.ma-LayoutBasic-content.ma-Listing > div > main > nav > ul > li:nth-child(10) > button')
        boton_next = driver.find_elements(By.XPATH, '/html/body/div[2]/div[3]/div[3]/div[1]/div[2]/div[3]/div/main/nav/ul/li[last()]')
        boton_next[0].click()
    except Exception as e:
        print('No hay más páginas, o', e)
        return False
    return True
    

def scrape_elements(driver):
    try:
        elementos = driver.find_elements(By.CSS_SELECTOR, 'div.ma-AdCardV2-upperGroup')
        for elemento in elementos:
            div_text = elemento.get_attribute('outerHTML')
            append_to_csv(csv_path, div_text)

        print(f'Cantidad de elementos: {len(elementos)}')

    except NoSuchElementException:
        print('No se encontraron elementos')
        return False
    
    return True


open_site(url)
