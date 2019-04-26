from etl import n_gt, is_roman

def test_n_gt():
    assert n_gt("Anzahl der Gruppen:\xa02 GT") == 2


def test_is_roman():
    assert is_roman("IV") == True
    assert is_roman("OO") == False
    assert is_roman("XIII. Gösting") == True