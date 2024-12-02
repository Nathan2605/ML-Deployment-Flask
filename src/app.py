#from src.utils import db_connect
#engine = db_connect()

# your code here

from flask import Flask, request, render_template
from pickle import load
import numpy as np

app = Flask(__name__)
# Cargar modelo
model = load(open("../models/ramfom_forrest_colombia_bank.sav", "rb"))

# Diccionario de clases
class_dict = {
    0: "NO BANCAROTA",
    1: "BANCAROTA"
}

@app.route("/", methods=["GET", "POST"])
def index():
    pred_class = None  # Inicializar predicción
    if request.method == "POST":
        try:
            # Obtener los valores desde el formulario
            sector = int(request.form["sector"])
            roa = float(request.form["roa"])
            roe = float(request.form["roe"])
            dr = float(request.form["dr"])
            dc = float(request.form["dc"])
            wcr = float(request.form["wcr"])
            
            # Crear un array con los valores de entrada
            data = [[sector, roa, roe, dr, dc, wcr]]
            
            # Realizar predicción
            prediction = model.predict(data)[0]
            pred_class = class_dict[prediction]  # Mapear predicción a su clase
        except Exception as e:
            pred_class = f"Error en la predicción: {e}"

    return render_template("index.html", prediction=pred_class)

if __name__ == "__main__":
    app.run(debug=True)