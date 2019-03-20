import bonobo
from requests_html import HTMLSession
import re
import os
from pprint import pprint
from loguru import logger


URL_KRIPPE_STAD = 'https://www.graz.at/cms/beitrag/10237730/7745079/Staedtische_Kinderkrippen.html'
FILE_KRIPPE_STAD = 'krippe_stad.json'

URL_KRIPPE_PRIVAT = 'https://www.graz.at/cms/beitrag/10238994/7745114/Private_Kinderkrippen.html'
FILE_KRIPPE_PRIVAT = 'krippe_privat.json'

KEYS = {
    'STAD': ['district', 'name', 'address', 'tel', 'n_groups', 'time', 'more'],
    'PRIVAT': ['district', 'name', 'address', 'tel', 'time']
}


def extract():
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
    yield t
        

def split_lines(t):
    lines = t.split('\n')
    logger.debug(lines)
    logger.debug(len(lines))
    if is_roman(lines[0]):
        yield lines
        

def jsonify(lines):
    kk = os.getenv('ETL_KEYS', None)
    if kk is None:
        raise ValueError('ETL_KEYS are not set')
    else:
        keys = KEYS.get(kk)
    d = dict(zip(keys, lines))
    logger.debug(d)
    yield d
    

def extract_gt(d):
    if d.get('n_groups', None):
        d.update({'GT': n_gt(d['n_groups'])})
    yield d
    
    
# Helper functions

def is_roman(l):
    reg = r"^(?=[MDCLXVI])M*(C[MD]|D?C{0,3})(X[CL]|L?X{0,3})(I[XV]|V?I{0,3}).+$"
    res = re.match(reg, l)
    return res is not None

    
def n_gt(text):
    reg = r"(\d+) (?=GT)"
    res = re.findall(reg, text)
    return int(res[0])


def get_graph():
    etl_fname = os.getenv('ETL_FNAME', None)
    if etl_fname is None:
        raise ValueError('ETL_FNAME is not set')
    graph = bonobo.Graph()
    graph.add_chain(extract,
                    to_text,
                    split_lines,
                    jsonify,
                    extract_gt,
                    bonobo.JsonWriter(etl_fname))
    return graph


def main():
    os.environ['ETL_URL'] = URL_KRIPPE_PRIVAT
    os.environ['ETL_FNAME'] = FILE_KRIPPE_PRIVAT
    os.environ['ETL_KEYS'] = 'PRIVAT'
    graph = get_graph()
    bonobo.run(graph)


if __name__ == "__main__":
    main()