import bonobo
from requests_html import HTMLSession
import re
import os
import sys
from pprint import pprint
from loguru import logger
from unidecode import unidecode
from geopy.geocoders import Nominatim, ArcGIS


URL_KRIPPE_STAD = 'https://www.graz.at/cms/beitrag/10237730/7745079/Staedtische_Kinderkrippen.html'
FILE_KRIPPE_STAD = 'data/krippe_stad.json'

URL_KRIPPE_PRIVAT = 'https://www.graz.at/cms/beitrag/10238994/7745114/Private_Kinderkrippen.html'
FILE_KRIPPE_PRIVAT = 'data/krippe_privat.json'

URL_KIGA_STAD = 'https://www.graz.at/cms/beitrag/10237817/7745175/Kindergaerten_der_Stadt_Graz.html'
FILE_KIGA_STAD = 'data/kiga_stad.json'

URL_KIGA_PRIVAT = 'https://www.graz.at/cms/beitrag/10239003/7745240/Private_Kindergaerten.html'
FILE_KIGA_PRIVAT = 'data/kiga_privat.json'


KEYS = {
    'STAD': ['district', 'name', 'address', 'tel', 'n_groups', 'time', 'more'],
    'PRIVAT': ['district', 'name', 'address', 'tel', 'time']
}


geolocator = Nominatim(user_agent="Kiga Graz")
arcgis = ArcGIS()


def extract():
    """Extract divs with krippe/kiga info from the GrazStadt page"""
    url = os.getenv('ETL_URL', None)
    if url is None:
        raise ValueError('ETL_URL is not set')
    session = HTMLSession()
    r = session.get(url)
    sel = '//*[@id="middle-content"]/div/div'
    elements = r.html.xpath(sel)
    for e in elements:
        yield e


def to_text(e):
    """Converts html el to text"""
    t = e.text
    logger.debug(t)
    yield t
        

def split_lines(t):
    lines = t.split('\n')
    if is_roman(lines[0]):
        sub_lines = lines[0].split(' - ')
        if len(sub_lines) == 2:
            del lines[0]
            lines = sub_lines + lines
        logger.debug(lines)
        yield lines
        

def jsonify(lines):
    """Return kiga info as a dict with keys according to ETL_KEYS"""
    kk = os.getenv('ETL_KEYS', None)
    if kk is None:
        raise ValueError('ETL_KEYS are not defined')
    else:
        keys = KEYS.get(kk)
    d = dict(zip(keys, lines))
    yield d
    

def extract_gt(d):
    """Extract the number of Ganze Tag groups"""
    if d.get('n_groups', None):
        logger.debug(d.get('n_groups', None))
        d.update({'GT': n_gt(d['n_groups'])})
    yield d
    

def location(d):
    """Calculate location from the address"""
    address = unidecode(d.get('address'))
    logger.debug(address)
    loc = geolocator.geocode(address)
    logger.debug(loc)
    if loc is not None:
        d.update({'location': loc.raw})
        d.update({'lat': loc.latitude})
        d.update({'lon': loc.longitude})
        return d
    
    loc = arcgis.geocode(address)
    if loc is not None:
        d.update({'location': loc.raw})
        d.update({'lat': loc.latitude})
        d.update({'lon': loc.longitude})
        return d
    
    logger.warning(f"Could not find location for {address}")
    d.update({'location': None})
    return d
    
# Helper functions

def is_roman(l):
    """Check if string represents a roman number"""
    reg = r"^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3}).+$"
    res = re.match(reg, l)
    return res is not None

    
def n_gt(text):
    """Extract number of GT groups"""
    reg = r"(\d+) (?=GT)"
    res = re.findall(reg, text)
    logger.debug(res)
    if res == []:
        return 0
    else:
        return int(res[0])


def get_graph():
    """Build the ETL graph"""
    etl_fname = os.getenv('ETL_FNAME', None)
    if etl_fname is None:
        raise ValueError('ETL_FNAME is not set')
    graph = bonobo.Graph()
    graph.add_chain(extract,
                    to_text,
                    split_lines,
                    jsonify,
                    extract_gt,
                    location,
                    bonobo.JsonWriter(etl_fname))
    return graph


def main():

    logger.remove(0)
    logger.add(sys.stderr, level="INFO")

    # # Run krippe privat
    # os.environ['ETL_KEYS'] = 'PRIVAT'
    # os.environ['ETL_URL'] = URL_KRIPPE_PRIVAT
    # os.environ['ETL_FNAME'] = FILE_KRIPPE_PRIVAT
    # graph = get_graph()
    # bonobo.run(graph)

    # # Run krippe stad
    # os.environ['ETL_KEYS'] = 'STAD'
    # os.environ['ETL_URL'] = URL_KRIPPE_STAD
    # os.environ['ETL_FNAME'] = FILE_KRIPPE_STAD
    # graph = get_graph()
    # bonobo.run(graph)

    # # Run kiga privat
    # os.environ['ETL_KEYS'] = 'PRIVAT'
    # os.environ['ETL_URL'] = URL_KIGA_PRIVAT
    # os.environ['ETL_FNAME'] = FILE_KIGA_PRIVAT
    # graph = get_graph()
    # bonobo.run(graph)

    # # Run kiga stad
    # os.environ['ETL_KEYS'] = 'STAD'
    # os.environ['ETL_URL'] = URL_KIGA_STAD
    # os.environ['ETL_FNAME'] = FILE_KIGA_STAD
    # graph = get_graph()
    # bonobo.run(graph)



if __name__ == "__main__":
    main()