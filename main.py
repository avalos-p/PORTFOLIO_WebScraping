import os
import sys
import logging

from config.logger_setup import setup_logging
from scrapy.cmdline import execute


# Logging config
setup_logging()
logger = logging.getLogger(__name__)

# Añadir la ruta de Scrapy al sistema
sys.path.append(os.path.join(os.path.dirname(__file__), 'scrapers/Scrapy_project'))
os.environ['SCRAPY_SETTINGS_MODULE'] = 'Poject_scrapy.settings'

# Ejecutar el spider
if __name__ == '__main__':
    execute(['scrapy', 'crawl', 'Trovimap_spider']) 