import os, re, csv, datetime, time, random
import logging
from io import StringIO
from scrapy.selector import Selector

date = datetime.datetime.now()
logger = logging.getLogger(__name__)

def create_csv(csv_path:str) -> None:
    '''
    This function creates a blank CSV file with the necessary columns.
    '''
    assert isinstance(csv_path, str), 'csv_path must be a string'
    try:
        # Define the columns
        columnas = ['titulo', 'precio', 'categoria', 'baños', 'habitaciones',
                    'area', 'link', 'operacion', 'provincia', 'municipio', 
                    'telefono', 'usuario', 'scraping_date']
        
        # Check if the directory exists
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        
        # Create the CSV file and write the columns
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(columnas)
    except Exception as e:
        logger.error(f"Error creating CSV file: {e}")

def random_delay(a: int = 1,b: int = 2)-> None:
    '''
    This function generates a random delay between two integers.
    '''
    if type(a) == int and type(b) == int:
        if a != b:
            return time.sleep(random.randint(min(a,b),max(a,b)))
        else:
            return time.sleep(random.randint(0,a))
    else:
        return time.sleep(random.uniform(1,2))

def extract_city(ciudad:str):
    assert isinstance(ciudad, str), 'Ciudad must be a string'

    try:
        matcheo = re.match(r'^(.+?) \((.+?)\)$', ciudad.strip())
        return matcheo[1], matcheo[2]
    except:
        return None, None
    
def extract_from_link(text:str):
    """
    This function receives a string with the URL of an ad and returns
    the operation and category of the ad.
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
    """
    This function receives a string with the number of rooms of the ads
    """
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
    """
    This function receives a string with the number of bathrooms of the ads
    """
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

def extract_area(text:str)-> str:
    """
    This function receives a string and returns the are.
    """
    try:
        if "m²" in text:
            area = text.replace("m²", "")
        else:
            area = None    
    except:
        area = None
    return area

def append_to_csv(filename : str, div_text : str):

    '''
    This function receives a string with the content of the ads
    and writes it to a CSV file.

    This function uses the scrapy selector to extract the data.
    '''
    try:    
        assert isinstance(filename, str), 'filename must be a string'
        assert isinstance(div_text, str), 'div_text must be a string'

        selector = Selector(text=div_text)

        municipio_provincia = selector.css('span.ma-SharedText.ma-AdLocation-text.ma-AdLocation-text--isCardListingLocation.ma-SharedText--s.ma-SharedText--gray::text').get()
        municipio,provincia =extract_city(municipio_provincia)

        link =selector.css('div.ma-AdCardV2-row.ma-AdCardV2-row--small.ma-AdCardV2-row--wrap a::attr(href)').get()
        operacion, categoria = extract_from_link(link)

        # Using this structure to avoid making mistakes
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
        logger.warning(f"Error appending to CSV file: {e}")
        pass