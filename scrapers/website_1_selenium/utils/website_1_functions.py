from io import StringIO
import re, csv, datetime, time, random
from scrapy.selector import Selector
# import pandas as pd
import os
import csv

date = datetime.datetime.now()



# def create_csv(csv_path):
#     '''
#     Esta función crea un archivo CSV en blanco con las columnas necesarias.
#     '''
#     df = pd.DataFrame(columns=['titulo','precio','categoria','baños','habitaciones',
#                            'area','link','operacion','provincia','municipio','teléfono',
#                            'usuario','scraping_date'])
#     df.to_csv(csv_path, index=False)
def create_csv(csv_path):
    '''
    Esta función crea un archivo CSV en blanco con las columnas necesarias.
    '''
    # Define las columnas
    columnas = ['titulo', 'precio', 'categoria', 'baños', 'habitaciones',
                'area', 'link', 'operacion', 'provincia', 'municipio', 
                'telefono', 'usuario', 'scraping_date']
    
    # Asegúrate de que el directorio exista
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Crea el archivo CSV y escribe las columnas
    with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columnas)

def random_delay():
    '''
    Esta función genera un delay aleatorio entre segundos
    para simular una navegación humana.
    '''
    return time.sleep(random.uniform(0,1))

def extract_city(ciudad:str):
    assert isinstance(ciudad, str), 'ciudad must be a string'

    try:
        matcheo = re.match(r'^(.+?) \((.+?)\)$', ciudad.strip())
        return matcheo[1], matcheo[2]
    except:
        return None, None
    
def extract_from_link(text:str):
    """Esta función recibe un string con la URL de un anuncio y devuelve
    la operación y la categoría del anuncio.
    """

    try:
        text_lower = text.lower()
        if 'alquiler' in text_lower:
            operacion = 'alquiler'
        elif 'venta' in text_lower:
            operacion ='venta'
        else:
            operacion = None
    except:
        categoria = None


    try:
        match = re.search(r'-de-(.+?)-en-', text)
        if match:
            categoria = match.group(1)
        else:
            categoria = None        
    except:
        categoria = None
    
    return operacion, categoria
    
def extract_rooms(text:str):
    # Extrae y limpia el número de habitaciones de los anuncios
    try:
        text_lower = text.lower()
        if "dor" in text_lower:
            habitaciones = re.findall(r'\d+', text_lower)
            habitaciones = ''.join(habitaciones)
            habitaciones = int(habitaciones)
        else:
            habitaciones = None
    except:
        habitaciones = None
    return habitaciones

def extract_bathrooms(text:str):
    # Extrae y limpia el número de baños de los anuncios
    try:
        text_lower = text.lower()
        if "baño" in text:
            baños = re.findall(r'\d+', text_lower)
            baños = ''.join(baños)
            baños = int(baños)
        else:
            baños = None
    except:
        baños = None
    return baños

def extract_area(text:str):
    # Extrae y limpia el area de los anuncios
    try:
        if "m²" in text:
            area = text.replace("m²", "")
        else:
            area = None    
    except:
        area = None
    return area

def append_to_csv(filename : str, div_text : str):

    '''Esta función recibe un string con el contenido de los anuncios
      y lo escribe en un archivo CSV.

      Esta función ocupa el slector de scrapy para extraer los datos.
      '''
    try:
    
        assert isinstance(filename, str), 'filename must be a string'
        assert isinstance(div_text, str), 'div_text must be a string'

        selector = Selector(text=div_text)

        municipio_provincia = selector.css('span.ma-SharedText.ma-AdLocation-text.ma-AdLocation-text--isCardListingLocation.ma-SharedText--s.ma-SharedText--gray::text').get()
        municipio,provincia =extract_city(municipio_provincia)

        link =selector.css('div.ma-AdCardV2-row.ma-AdCardV2-row--small.ma-AdCardV2-row--wrap a::attr(href)').get()
        operacion, categoria = extract_from_link(link)

        #Uso ésta estructura para evitar cometer errores
        titulo =  selector.css('h2.ma-SharedText.ma-AdCardV2-title.ma-SharedText--m.ma-SharedText--black.ma-SharedText--numLines::text').get()
        precio = selector.css('span.ma-AdPrice-value.ma-AdPrice-value--dark.ma-AdPrice-value--heading--s::text').get()
        categoria = categoria
        banos = extract_bathrooms(selector.css('li:nth-of-type(2) .ma-AdTag-label::attr(title)').get())
        habitaciones = extract_rooms(selector.css('li:nth-of-type(1) .ma-AdTag-label::attr(title)').get())
        area = extract_area(selector.css('li:nth-of-type(3) .ma-AdTag-label::attr(title)').get())
        link = 'milanuncios.com' + link if type(link) == str else None
        operacion = operacion
        provincia = provincia
        municipio = municipio
        telefono = None
        usuario = None
        scraping_date = date.strftime("%Y-%m-%d %H=%M:%S")

        data = [(titulo,precio,categoria,banos,habitaciones,
                 area,link,operacion,provincia,municipio,telefono,
                 usuario,scraping_date)] # Append data to CSV file


        with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(data)

    except Exception as e:
        print(f"Error: {e}")
        pass




    





