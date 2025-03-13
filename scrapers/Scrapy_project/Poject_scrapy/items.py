import scrapy

class TicketItem(scrapy.Item):
    titulo = scrapy.Field()
    precio = scrapy.Field()
    categoria = scrapy.Field()
    baños = scrapy.Field()
    habitaciones = scrapy.Field()
    area = scrapy.Field()
    link = scrapy.Field()
    operacion = scrapy.Field()
    provincia = scrapy.Field()
    municipio = scrapy.Field()
    teléfono = scrapy.Field()
    usuario = scrapy.Field()
    scraping_date = scrapy.Field()                     