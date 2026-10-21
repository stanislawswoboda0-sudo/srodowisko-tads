import csv

def wczytaj_zamowienia(sciezka):
    """Wczytuje dane z pliku CSV."""
    with open(sciezka, mode='r', encoding='utf-8') as plik:
        reader = csv.DictReader(plik)
        return list(reader)

def dostepne_regiony(sciezka):
    """Zwraca posortowaną listę unikalnych regionów."""
    zamowienia = wczytaj_zamowienia(sciezka)
    regiony = {wiersz['region'] for wiersz in zamowienia if 'region' in wiersz}
    return sorted(list(regiony))

def policz_wskazniki(sciezka, region=None):
    """Oblicza wskaźniki dla danego regionu lub całości."""
    zamowienia = wczytaj_zamowienia(sciezka)
    
    liczba_zamowien = 0
    przychod = 0.0
    koszt = 0.0
    
    for wiersz in zamowienia:
        if region is None or wiersz.get('region') == region:
            liczba_zamowien += 1
            przychod += float(wiersz.get('przychod', 0))
            koszt += float(wiersz.get('koszt', 0))
            
    # Zabezpieczenie przed ZeroDivisionError
    if przychod == 0.0:
        marza = 0.0
    else:
        marza = (przychod - koszt) / przychod
        marza = round(marza, 4) # Zaokrąglenie dla zgodności z przykładem w konsoli
        
    return {
        'region': region,
        'liczba_zamowien': liczba_zamowien,
        'przychod': przychod,
        'koszt': koszt,
        'marza': marza
    }