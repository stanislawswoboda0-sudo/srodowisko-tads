from datetime import date
from flask import Blueprint, request, abort, current_app, redirect, url_for, render_template, flash
from .services import (
    policz_wskazniki,
    dostepne_regiony,
    zapisz_raport,
    raporty_roku,
    zestawienie_regionow,
    wykaz_raportow,
)
from .forms import FiltrForm, RaportForm

panel_bp = Blueprint('panel', __name__)
ROK_DOMYSLNY = 2026

@panel_bp.route('/')
def index():
    return "Panel wskaźników"

@panel_bp.get("/kpi")
def kpi():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    formularz = FiltrForm(request.args)
    regiony = dostepne_regiony(sciezka)
    formularz.region.choices = [("", "wszystkie")] + [(r, r) for r in regiony]
    
    region = rok = None
    if formularz.validate():
        region = formularz.region.data or None
        rok = formularz.rok.data
    else:
        flash("Kryteria zawężenia zostały pominięte", "warning")
        
    w = policz_wskazniki(sciezka, region, rok)
    if region is not None:
        current_app.logger.info("Obliczono wskaźniki dla regionu %s", w["region"])
        
    return render_template(
        "panel.html",
        formularz=formularz,
        wskazniki=w,
        zestawienie=zestawienie_regionow(sciezka),
        dzisiaj=date.today(),
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

@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    return render_template("report.html", rok=rok, zapisane=raporty_roku(rok))

@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    istniejace = {(r["rok"], r["region"]) for r in wykaz_raportow()}
    formularz = RaportForm(istniejace=istniejace)
    formularz.region.choices = [(r, r) for r in dostepne_regiony(sciezka)]

    if formularz.validate_on_submit():
        zapisz_raport(
            formularz.rok.data,
            formularz.region.data,
            formularz.uwagi.data or "",
        )
        flash(f"Raport za rok {formularz.rok.data} zapisany", "success")
        return redirect(url_for("panel.raport", rok=formularz.rok.data), 303)

    status = 422 if formularz.errors else 200
    return render_template("new_report.html", formularz=formularz), status

@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), 301)