from etl import n_gt, is_roman, jsonify, KEYS, split_lines
import os

def test_n_gt():
    assert n_gt("Anzahl der Gruppen:\xa02 GT") == 2

def test_n_gt_0():
    assert n_gt("Anzahl der Gruppen: 1 HT") == 0


def test_is_roman():
    assert is_roman("IV") == True
    assert is_roman("OO") == False
    assert is_roman("XIII. Gösting") == True


def test_split_lines_kiga_stad():
    text = 'XVII. Puntigam - Kindergarten Nippelgasse\nNippelgasse 14, 8055 Graz\nTel.: +43 316 872-2629\nAnzahl der Gruppen: 3 GT, 1 HT, davon 1 integrativ\nÖffnungszeiten: Montag bis Freitag von 07.00-18.00 Uhr\nInfos zum Kindergarten Nippelgasse'
    lines = next(split_lines(text))
    expected = ['XVII. Puntigam',
            'Kindergarten Nippelgasse',
             'Nippelgasse 14, 8055 Graz',
             'Tel.: +43 316 872-2629',
             'Anzahl der Gruppen: 3 GT, 1 HT, davon 1 integrativ',
             'Öffnungszeiten: Montag bis Freitag von 07.00-18.00 Uhr',
             'Infos zum Kindergarten Nippelgasse']
    assert lines == expected 

def test_jsonify_kiga_stad():

    os.environ["ETL_KEYS"] = "STAD"
    lines = ['XVII. Puntigam',
             'Kindergarten Nippelgasse',
             'Nippelgasse 14, 8055 Graz',
             'Tel.: +43 316 872-2629',
             'Anzahl der Gruppen: 3 GT, 1 HT, davon 1 integrativ',
             'Öffnungszeiten: Montag bis Freitag von 07.00-18.00 Uhr',
             'Infos zum Kindergarten Nippelgasse']

    d = next(jsonify(lines))
    assert d['district'] == 'XVII. Puntigam'
    assert d['name'] == 'Kindergarten Nippelgasse'



# 'district', 'name', 'address', 'tel', 'n_groups', 'time', 'more']