from datetime import date
from flask import Blueprint, request, abort, current_app, redirect, url_for, render_template
from .services import policz_wskazniki, dostepne_regiony, zapisz_raport, raporty_roku, zestawienie_regionow

panel_bp = Blueprint('panel', __name__)
ROK_DOMYSLNY = 2026

@panel_bp.route('/')
def index():
    return "Panel wskaźników"

@panel_bp.route('/kpi')
def kpi():
    region = request.args.get("region")
    sciezka_csv = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka_csv)
    
    if region is not None and region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    w = policz_wskazniki(sciezka_csv, region)
    
    if region is not None:
        current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
    
    return render_template(
        "panel.html",
        wskazniki=w,
        zestawienie=zestawienie_regionow(sciezka_csv),
        dzisiaj=date.today()
    )

@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka_csv = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka_csv)
    if kod not in regiony:
        abort(404, description=f"Nieznany region: {kod}")
    w = policz_wskazniki(sciezka_csv, kod)
    return render_template(
        "panel.html",
        wskazniki=w,
        zestawienie=zestawienie_regionow(sciezka_csv),
        dzisiaj=date.today()
    )

# ... pozostałe trasy (raport, nowy_raport, stary_panel) zostają bez zmian ...