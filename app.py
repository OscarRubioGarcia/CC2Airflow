from flask import Flask, jsonify
from flask_restful import abort
import function

app = Flask(__name__)

def abortar_ruta_inexistente(ruta):
    abort(404, message="Error 404. Ruta {} Inexistente".format(ruta))

#Ejemplo
@app.route('/')
def hello():
    return "Landing page for API V1!"


@app.route('/servicio/v1/prediccion/24horas')
def version1predict24():
    function.functionpredicthumidity(24)
    function.functionpredicttemperature(24)
    return jsonify({"YouCalled": "Predict24"}), 400


@app.route('/servicio/v1/prediccion/48horas')
def version1predict48():
    function.functionpredicthumidity(48)
    function.functionpredicttemperature(48)
    return jsonify({"YouCalled": "Predict48"}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=False)
