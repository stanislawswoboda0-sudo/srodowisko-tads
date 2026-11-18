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

def policz_wskazniki(sciezka, region=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    liczba_zamowien = 0
    przychod = 0.0
    koszt = 0.0
    
    for wiersz in zamowienia:
        if region is None or wiersz.get('region') == region:
            liczba_zamowien += 1
            przychod += float(wiersz.get('przychod', 0))
            koszt += float(wiersz.get('koszt', 0))
            
    if przychod == 0.0:
        marza = 0.0
    else:
        marza = round((przychod - koszt) / przychod, 4)
        
    return {
        'region': region,
        'liczba_zamowien': liczba_zamowien,
        'przychod': przychod,
        'koszt': koszt,
        'marza': marza
    }

def zapisz_raport(rok, region):
    _RAPORTY.append({"rok": rok, "region": region})

def raporty_roku(rok):
    return [r for r in _RAPORTY if r["rok"] == rok]

def zestawienie_regionow(sciezka):
    return [policz_wskazniki(sciezka, r) for r in dostepne_regiony(sciezka)]