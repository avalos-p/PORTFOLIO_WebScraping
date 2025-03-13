import scrapy
import datetime
import logging
from Poject_scrapy.items import TicketItem

date = datetime.datetime.now()

class SpideralquileresSpider_Trovimap(scrapy.Spider):

    name = "Trovimap_spider"
    logger = logging.getLogger(__name__)
    allowed_domains = ["trovimap.com",]
    custom_settings = {
    'FEED_FORMAT': 'csv',
    'FEED_URI': f'Raw_Csv/raw_trovimap_{date.strftime("%Y-%m-%d")}.csv'  # Add date to the filename
    }
    
    def start_requests(self):

        self.start_urls = [
            "https://www.trovimap.com/",
        ]

        for url in self.start_urls:  # Iterate through URLs
            print("Iniciando el Scrapeo de Trovimap.com")
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        
        avisos = response.css('.collapse-sitemap.home-sitemap__list a::attr(href)')

        for aviso in avisos:
            alquiler_texto = aviso.get()
            alquiler_texto = alquiler_texto.replace("vivienda", "todos")
            partes = alquiler_texto.split("/")
            alquiler_texto_join = "/".join(partes[:-1])
            new_url = "https://www.trovimap.com/" + alquiler_texto_join + '?sellerType=13'

            yield scrapy.Request(url=new_url, callback=self.parse_paginas,meta={'operacion': "venta",
                                                                                'municipio': partes[-2]}) # Parts in this position refers to the municipality

        for aviso in avisos:

            alquiler_texto = aviso.get()
            alquiler_texto = alquiler_texto.replace("venta", "alquiler")
            alquiler_texto = alquiler_texto.replace("vivienda", "todos")
            partes = alquiler_texto.split("/")
            alquiler_texto_join = "/".join(partes[:-1])
            new_url = "https://www.trovimap.com/" + alquiler_texto_join + '?sellerType=13'

            yield scrapy.Request(url=new_url, callback=self.parse_paginas,meta={'operacion': "alquiler",
                                                                                'municipio': partes[-2]})

    def parse_paginas(self, response):
        anuncios = response.css('trovimap-virtual-grid .listing.view-3')
        for anuncio in anuncios:
            try:
                item = TicketItem()
                item['titulo'] = anuncio.css('h2.text-capitalize-first-letter ::text').get()
                item['precio'] = anuncio.css('div.price h4::text').get()
                item['categoria'] = anuncio.css('span.property-type ::text').get()
                item['baños'] = anuncio.css('div.card__details span.trovimap-icon:nth-child(3)::text').get()
                item['habitaciones'] = anuncio.css('div.card__details span.trovimap-icon:nth-child(2)::text').get()
                item['area'] = anuncio.css('div.card__details span.trovimap-icon:nth-child(1)::text').get()
                item['link'] = 'https://www.trovimap.com'+anuncio.css('a::attr(href)').get()
                item['operacion'] = response.meta.get('operacion')
                item['provincia'] = response.meta.get('municipio')
                item['municipio'] = anuncio.css('h3::text').get()
                item['teléfono']  =None
                item['usuario'] = anuncio.css('.property-spec ::text').get()
                item['scraping_date']= date.strftime("%Y-%m-%d %H:%M:%S")
                    
                yield item
            except Exception as e:
                self.logger.error(f"Error procesando un ticket: {e}")
        next = response.css('li.pagination-next a::attr(href)').get()  # Get the link to the next page if it exists
        
        if next:
            yield scrapy.Request(url=next, callback=self.parse_paginas, meta=response.meta)  # If there's a next page, call the function again

        else:
            print('Se scrapeó hasta la página:   ',response.url) # If there's no next page, print the URL of the final page to confirm it reached the last one
            pass
      
