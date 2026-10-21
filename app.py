from flask import Flask
app = Flask(__name__)
@app.get("/")
def index():
 return "Panel wskaźników"

from flask import Flask, request, abort, jsonify
from services import policz_wskazniki, dostepne_regiony

app = Flask(__name__)
SCIEZKA_CSV = "dane/zamowienia.csv"

@app.route('/kpi')
def kpi_html():
    region = request.args.get("region")
    regiony = dostepne_regiony(SCIEZKA_CSV)
    
    # Sprawdzenie czy region istnieje
    if region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    wskazniki = policz_wskazniki(SCIEZKA_CSV, region)
    
    # Zwrócenie sformatowanego HTML
    return f"<h1>Wskaźniki: {region}</h1><p>Marża: {wskazniki['marza']:.2%}</p>"

@app.route('/api/kpi')
def kpi_json():
    region = request.args.get("region")
    regiony = dostepne_regiony(SCIEZKA_CSV)
    
    # Sprawdzenie czy region istnieje (to samo co wyżej)
    if region not in regiony:
        abort(404, description=f"Nieznany region: {region}")
        
    wskazniki = policz_wskazniki(SCIEZKA_CSV, region)
    
    # Zwrócenie danych w formacie JSON
    return jsonify(wskazniki)

if __name__ == '__main__':
    app.run(debug=True)
