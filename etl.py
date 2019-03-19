import bonobo
from requests_html import HTMLSession
import re
from pprint import pprint


URL_KIGA = 'https://www.graz.at/cms/beitrag/10237730/7745079/Staedtische_Kinderkrippen.html'


def extract():
    url = URL_KIGA
    session = HTMLSession()
    r = session.get(url)
    sel = '//*[@id="middle-content"]/div/div'
    elements = r.html.xpath(sel)
    for e in elements:
        yield e
        

def split_lines(e):
    text = e.text
    lines = text.split('\n')
    if len(lines) == 7:
        yield lines
        

def jsonify(lines):
    keys = ['district', 'name', 'address', 'tel', 'n_groups', 'time', 'more']
    d = dict(zip(keys, lines))
    pprint(d)
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
    graph = bonobo.Graph()
    graph.add_chain(extract,
                    split_lines,
                    jsonify,
                    extract_gt,
                    bonobo.JsonWriter('kiga.json'))
    return graph


def main():
    graph = get_graph()
    bonobo.run(graph)


if __name__ == "__main__":
    main()