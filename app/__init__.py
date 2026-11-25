import logging
import time
from datetime import date
from flask import Flask, g
from flask_wtf import CSRFProtect
from .commands import zarejestruj_polecenia
from .config import KONFIGURACJE
from .converters import RegionConverter
from .errors import zarejestruj_obsluge_bledow
from .extensions import db, migrate
from .filters import zarejestruj_filtry
from .services import dostepne_regiony

csrf = CSRFProtect()

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    zarejestruj_polecenia(app)

    app.url_map.converters["region"] = RegionConverter
    zarejestruj_filtry(app)

    @app.context_processor
    def dane_wspolne():
        return {
            "regiony": dostepne_regiony(),
            "rok_biezacy": date.today().year,
        }

    @app.before_request
    def przed_zadaniem():
        g.start = time.perf_counter()

    @app.after_request
    def po_zadaniu(odpowiedz):
        if hasattr(g, "start"):
            czas = (time.perf_counter() - g.start) * 1000.0
            odpowiedz.headers["X-Czas-Ms"] = f"{czas:.2f}"
        return odpowiedz

    csrf.init_app(app)
    zarejestruj_obsluge_bledow(app)

    from .routes_api import api_bp
    from .routes_panel import panel_bp

    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")
    
    return app