# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from datetime import datetime, timedelta
import re


class CleanDataPipeline:
    def process_item(self, item, spider):
        # Limpiar espacios en blanco al principio y al final de las cadenas
        if item.get('titulo'):
            item['titulo'] = item['empresa_de_titulotransporte'].strip()
        
        if item.get('precio'):
            item['precio'] = item['precio'].strip()
        
        if item.get('categoria'):
            item['categoria'] = item['categoria'].strip()
        
        if item.get('baños'):
            item['baños'] = item['baños'].strip()

        if item.get('habitaciones'):
            item['habitaciones'] = item['habitaciones'].strip()

        if item.get('area'):
            item['area'] = item['area'].strip()
        
        if item.get('link'):
            item['link'] = item['link'].strip()

        if item.get('operacion'):
            item['operacion'] = item['operacion'].strip()

        if item.get('provincia'):
            item['provincia'] = item['provincia'].strip()

        if item.get('municipio'):
            item['municipio'] = item['municipio'].strip()

        if item.get('teléfono'):
            item['teléfono'] = item['teléfono'].strip()

        if item.get('usuario'):
            item['usuario'] = item['usuario'].strip()
        
        if item.get('scraping_date'):
            item['scraping_date'] = item['scraping_date'].strip()
            
        # Validar datos
        if not item.get('titulo') or not item.get('precio'):
            raise ValueError("Missing required fields in item: titulo / precio")
        
        return item


class TrovimapPipeline:
    def process_item(self, item, spider):
        return item