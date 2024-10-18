import os
import sys
import datetime

import logging
from config.logger_setup import setup_logging

from scrapy.cmdline import execute
from scrapers.milanuncios_selenium.scraper_milanuncios import MilanunciosScraper

# Logging config
setup_logging()
logger = logging.getLogger(__name__)

# Add Scrapy project path to system
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers/Scrapy_project')) 
os.environ['SCRAPY_SETTINGS_MODULE'] = 'Poject_scrapy.settings'

def main():
    execute(['scrapy', 'crawl', 'Trovimap_spider'])  # Can be replaced with any other spider name
    ## Example of running the Milanuncios web scraper
    url = 'https://www.milanuncios.com/inmobiliaria/?demanda=n&vendedor=part&orden=relevance&fromSearch=1&hitOrigin=listing'
    scraper = MilanunciosScraper(url,False)
    scraper.run_scraper()

# Run the main function
if __name__ == '__main__':
    main()