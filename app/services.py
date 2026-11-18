import csv

_RAPORTY = []

def wczytaj_zamowienia(sciezka):
    with open(sciezka, mode='r', encoding='utf-8') as plik:
        reader = csv.DictReader(plik)
        return list(reader)

def dostepne_regiony(sciezka):
    zamowienia = wczytaj_zamowienia(sciezka)
    regiony = {wiersz['region'] for wiersz in zamowienia if 'region' in wiersz}
    return sorted(list(regiony))

def policz_wskazniki(sciezka, region=None, rok=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    liczba_zamowien = 0
    przychod = 0.0
    koszt = 0.0
    
    for wiersz in zamowienia:
        if region and wiersz.get('region') != region:
            continue
        if rok is not None and not wiersz.get('data', '').startswith(str(rok)):
            continue
        liczba_zamowien += 1
        przychod += float(wiersz.get('przychod', 0))
        koszt += float(wiersz.get('koszt', 0))
            
    if przychod == 0.0:
        marza = 0.0
    else:
        marza = round((przychod - koszt) / przychod, 4)
        
    return {
        'region': region or 'wszystkie',
        'liczba_zamowien': liczba_zamowien,
        'przychod': przychod,
        'koszt': koszt,
        'marza': marza
    }

def zestawienie_regionow(sciezka):
    return [policz_wskazniki(sciezka, r) for r in dostepne_regiony(sciezka)]

def zapisz_raport(rok, region, uwagi=""):
    _RAPORTY.append({"rok": rok, "region": region, "uwagi": uwagi})

def raporty_roku(rok):
    return [r for r in _RAPORTY if r["rok"] == rok]

def wykaz_raportow():
    return list(_RAPORTY)