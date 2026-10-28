from flask import Blueprint, request, abort, jsonify, current_app
from .services import policz_wskazniki, dostepne_regiony, raporty_roku
from .validators import parametr_int
from .decorators import wymagany_parametr

api_bp = Blueprint('api', __name__)

@api_bp.route('/kpi')
def kpi():
    region = request.args.get("region")
    sciezka_csv = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka_csv)
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    w = policz_wskazniki(sciezka_csv, region)
    return jsonify(w)

@api_bp.get("/raporty")
@wymagany_parametr("rok")
def raporty():
    rok = parametr_int("rok", 2020, 2030)
    return jsonify(rok=rok, raporty=raporty_roku(rok))