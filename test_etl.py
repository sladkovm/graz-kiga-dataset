from etl import n_gt

def test_n_gt():
    assert n_gt("Anzahl der Gruppen:\xa02 GT") == 2