from flask import Blueprint, request, abort, current_app, redirect, url_for
from .services import policz_wskazniki, dostepne_regiony, zapisz_raport, raporty_roku

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
    
    wyswietlany_region = region if region else "None" 
    return f"<h1>Wskaźniki: {wyswietlany_region}</h1><p>Marża: {w['marza']:.2%}</p>"

@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka_csv = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka_csv)
    if kod not in regiony:
        abort(404, description=f"Nieznany region: {kod}")
    w = policz_wskazniki(sciezka_csv, kod)
    return f"<h1>Region {kod}</h1><p>Zamówień: {w['liczba_zamowien']}</p>"

@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    n = len(raporty_roku(rok))
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {n}</p>"

# --- NOWE TRASY Z ZADANIA 2 ---
@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "GET":
        return "Wyślij żądanie POST z polami rok i region, aby zapisać raport."
    
    rok = request.form.get("rok", type=int)
    region_kod = request.form.get("region")
    sciezka_csv = current_app.config["SCIEZKA_DANYCH"]
    regiony = dostepne_regiony(sciezka_csv)
    
    if rok is None or region_kod not in regiony:
        abort(400, description="Niepoprawne dane formularza")
    if not (2020 <= rok <= 2030):
        abort(422, description="Rok poza zakresem 2020-2030")
        
    zapisz_raport(rok, region_kod)
    return redirect(url_for("panel.raport", rok=rok), 303)

@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)