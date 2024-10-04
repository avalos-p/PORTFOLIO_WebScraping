import scrapy
import datetime
import logging

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

        for url in self.start_urls:  # Iterate through URLs (test)
            print("Iniciando el Scrapeo de Trovimap.com")
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):

        # Logic to get links from the main page
        print('inicia el parse')
        avisos = response.css('.collapse-sitemap.home-sitemap__list a::attr(href)')
        # Using links from the main page to get provinces and format
        # Then modify in these two loops, one for sales and one for rentals

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

        # At this point, get data from the listings themselves
        anuncios = response.css('trovimap-virtual-grid .listing.view-3')
        for anuncio in anuncios:
            try:
                yield{
                        'titulo' : anuncio.css('h2.text-capitalize-first-letter ::text').get(),
                        'precio' : anuncio.css('div.price h4::text').get(),
                        'categoria' : anuncio.css('span.property-type ::text').get(),
                        'baños' : anuncio.css('div.card__details span.trovimap-icon:nth-child(3)::text').get(),
                        'habitaciones' : anuncio.css('div.card__details span.trovimap-icon:nth-child(2)::text').get(),
                        'area(m2)' : anuncio.css('div.card__details span.trovimap-icon:nth-child(1)::text').get(),
                        'link' : 'https://www.trovimap.com'+anuncio.css('a::attr(href)').get(),
                        'operacion' : response.meta.get('operacion'),
                        'provincia' : response.meta.get('municipio'),
                        'municipio' : anuncio.css('h3::text').get(),
                        'teléfono':None,
                        'usuario' : anuncio.css('.property-spec ::text').get(),
                        'scraping_date': date.strftime("%Y-%m-%d %H:%M:%S"),
                    }
            except:
                pass
        next = response.css('li.pagination-next a::attr(href)').get()  # Get the link to the next page if it exists
        print(next)    # Print the link to the next page to see if it's actually moving
        if next:
            yield scrapy.Request(url=next, callback=self.parse_paginas, meta=response.meta)  # If there's a next page, call the function again

        else:
            print('Se scrapeó hasta la página:   ',response.url) # If there's no next page, print the URL of the final page to confirm it reached the last one
            pass
      
