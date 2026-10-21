from flask import Blueprint, request, abort, current_app
from .services import policz_wskazniki, dostepne_regiony

panel_bp = Blueprint('panel', __name__)

@panel_bp.route('/')
def index():
    return "Panel wskaźników"

@panel_bp.route('/kpi')
def kpi_html():
    region = request.args.get("region")
    # Pobranie ścieżki z konfiguracji
    sciezka_csv = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka_csv)
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    w = policz_wskazniki(sciezka_csv, region)
    
    # Dodanie logowania na poziomie INFO, jeśli podano region
    if region is not None:
        current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
    
    wyswietlany_region = region if region else "None" 
    return f"<h1>Wskaźniki: {wyswietlany_region}</h1><p>Marża: {w['marza']:.2%}</p>"
