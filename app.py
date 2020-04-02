from flask import Flask, jsonify, request
from flask_restful import abort
import function
import json

app = Flask(__name__)

def abortar_ruta_inexistente(ruta):
    abort(404, message="Error 404. Ruta {} Inexistente".format(ruta))

#Ejemplo
@app.route('/')
def hello():
    return "Landing page for API V2!"


@app.route('/servicio/v2/prediccion/24horas')
def version1predict24():
    # dataset = request.args.get('dataset')
    # hours = request.args.get('hours', type = int)
    hours = 24
    hum = function.functionpredicthumidity(hours)
    temp = function.functionpredicttemperature(hours)
    jsonresponse = function.generateresponse(hours, temp, hum)
    return app.response_class(jsonresponse, status=200, mimetype='application/json')


@app.route('/servicio/v2/prediccion/48horas')
def version1predict48():
    # dataset = request.args.get('dataset')
    # hours = request.args.get('hours', type = int)
    hours = 48
    hum = function.functionpredicthumidity(hours)
    temp = function.functionpredicttemperature(hours)
    jsonresponse = function.generateresponse(hours, temp, hum)
    return app.response_class(jsonresponse, status=200, mimetype='application/json')


@app.route('/servicio/v2/prediccion/72horas')
def version1predict72():
    # dataset = request.args.get('dataset')
    # hours = request.args.get('hours', type = int)
    hours = 72
    hum = function.functionpredicthumidity(hours)
    temp = function.functionpredicttemperature(hours)
    jsonresponse = function.generateresponse(hours, temp, hum)
    return app.response_class(jsonresponse, status=200, mimetype='application/json')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8081, debug=False)
