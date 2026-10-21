from flask import Blueprint, request, abort, jsonify, current_app
from .services import policz_wskazniki, dostepne_regiony

api_bp = Blueprint('api', __name__)

@api_bp.route('/kpi')
def kpi_json():
    region = request.args.get("region")
    sciezka_csv = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka_csv)
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    w = policz_wskazniki(sciezka_csv, region)
    return jsonify(w)