from decimal import Decimal
from flask import Blueprint, request, abort, jsonify
from .services import policz_wskazniki, dostepne_regiony, raporty_roku
from .validators import parametr_int
from .decorators import wymagany_parametr

api_bp = Blueprint('api', __name__)

def _jako_liczby(slownik):
    return {k: float(v) if isinstance(v, Decimal) else v for k, v in slownik.items()}

@api_bp.route('/kpi')
def kpi():
    region = request.args.get("region")
    regiony = dostepne_regiony()
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    w = policz_wskazniki(region)
    return jsonify(_jako_liczby(w))

@api_bp.get("/raporty")
@wymagany_parametr("rok")
def raporty():
    rok = parametr_int("rok", 2020, 2030)
    return jsonify(rok=rok, raporty=raporty_roku(rok))