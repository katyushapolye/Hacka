from flask import Flask, jsonify, request
from classifyalerts.model.alert import Alert, AlertSchema
from classifyalerts.utils import pops_dict, topAmeacas, fillTableClass

app = Flask(__name__)

alerts = [
    {
        "description": "abcd",
        "num": "num"
     }
]


@app.route('/alerts')
def get_alerts():
    options = {}
    query_string = request.query_string.decode('utf-8')
    query_string = query_string.split('&')
    for entry in query_string:
        data = entry.split('=')
        options[data[0]] = data[1]
    
    if options['chart'] == 'grafico1':
        entries = topAmeacas(options['_region'], options['date'], options['pop'])
    if options['chart'] == 'grafico2':
        #funcao grafico 2
        pass
    if options['chart'] == 'grafico3':
        #funcao grafico 3
        pass
    if options['chart'] == 'grafico4':
        #funcao grafico 4
        pass
    if options['chart'] == 'grafico5':
        #funcao grafico 5
        pass
    if options['chart'] == 'table':
        entries = fillTableClass(options['_region'], options['pop'])
        pass
    return jsonify(entries)


@app.route('/alerts', methods=['POST'])
def add_alerts():
    alert = AlertSchema().load(request.get_json())
    alerts.append(alert)
    return '', 204

if __name__ == "__main__":
    app.run()