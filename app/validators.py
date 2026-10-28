from flask import request, abort

def parametr_int(nazwa, minimum, maksimum):
    if nazwa not in request.args:
        abort(400, description=f"Brak parametru {nazwa}")
    wartosc = request.args.get(nazwa, type=int)
    if wartosc is None:
        abort(400, description=f"Parametr {nazwa} musi byc liczba")
    if not (minimum <= wartosc <= maksimum):
        abort(422, description=f"Parametr {nazwa} poza zakresem {minimum}-{maksimum}")
    return wartosc