from flask import Flask, jsonify
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello World!"

@app.route('/rota2')
def home2():
    return "<H1> Testando segunda rota!!!"

@app.route('/test_parameter/<string:nome>/<int:idade>')
def pessoa(nome, idade):
    return jsonify({'Nome': nome, 'Idade': idade})

@app.route('/timeout')
def timeout():
    time.sleep(70)  # Força a aplicação a esperar 70 segundos antes de responder para verificar o erro de Timeout
    return "Essa rota demorou 70 segundos para responder!"

if __name__ == "__main__":
    app.run(debug=True)