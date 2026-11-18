import logging
import time
from datetime import date
from flask import Flask, g
from .config import KONFIGURACJE
from .converters import RegionConverter
from .errors import zarejestruj_obsluge_bledow
from .filters import zarejestruj_filtry
from .services import dostepne_regiony

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)

    # 1. Rejestracja konwertera przed blueprintami
    app.url_map.converters["region"] = RegionConverter

    # 2. Rejestracja filtrów szablonów i procesora kontekstu (Zadanie 2)
    zarejestruj_filtry(app)

    @app.context_processor
    def dane_wspolne():
        return {
            "regiony": dostepne_regiony(app.config["SCIEZKA_DANYCH"]),
            "rok_biezacy": date.today().year,
        }

    # 3. Procedury cyklu żądania (pomiar czasu)
    @app.before_request
    def przed_zadaniem():
        g.start = time.perf_counter()

    @app.after_request
    def po_zadaniu(odpowiedz):
        czas = (time.perf_counter() - g.start) * 1000.0
        odpowiedz.headers["X-Czas-Ms"] = f"{czas:.2f}"
        return odpowiedz

    # 4. Wspólna obsługa błędów HTTP
    zarejestruj_obsluge_bledow(app)

    from .routes_api import api_bp
    from .routes_panel import panel_bp

    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")
    
    return app