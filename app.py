from flask import Flask, jsonify

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

if __name__ == "__main__":
    app.run(debug=True)