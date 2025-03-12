from flask import Flask, jsonify
import time
import threading
import sys

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

# Força a aplicação a esperar 70 segundos antes de responder para verificar o erro de Timeout
def long_task():
    print("Tarefa iniciada!")  # Confirmação da inicialização
    sys.stdout.flush()  # Força a exibição do print nos logs
    time.sleep(70)  # Simula uma tarefa longa
    print("Tarefa concluída!")  # Deveria aparecer após 70s
    sys.stdout.flush()


@app.route('/timeout')
def timeout():
    thread = threading.Thread(target=long_task)
    thread.start()  # Inicia a tarefa sem bloquear a resposta HTTP
    return jsonify({"message": "Tarefa iniciada, verifique os logs para status"}), 202

if __name__ == "__main__":
    app.run(debug=True)