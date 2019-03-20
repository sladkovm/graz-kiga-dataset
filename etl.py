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
    t = e.text
    logger.debug(t)
    yield t
        

def split_lines(t):
    lines = t.split('\n')
    logger.debug(lines)
    logger.debug(len(lines))
    if (len(lines) == 7):
        yield lines
        

def jsonify(lines):
    keys = ['district', 'name', 'address', 'tel', 'n_groups', 'time', 'more']
    d = dict(zip(keys, lines))
    logger.debug(d)
    yield d
    

def extract_gt(d):
    d.update({'GT': n_gt(d['n_groups'])})
    yield d
    
    
# Helper functions
    
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
    graph = get_graph()
    bonobo.run(graph)


if __name__ == "__main__":
    main()