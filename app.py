from flask import Flask, jsonify
import time
import threading
import sys

app = Flask(__name__)


# Dicionário para armazenar status das tarefas
tasks = {}  

#! FUNÇÃO: Força a aplicação a esperar 70 segundos antes de responder para verificar o erro de Timeout
def long_task(task_id):
    time.sleep(70)  # Simula uma tarefa longa
    tasks[task_id] = "Concluído"


#? ROTA: PADRÃO
@app.route('/')
def home():
    return "Hello World!"


#? ROTA: TESTE DE MUDANÇA DE ROTA
@app.route('/rota2')
def home2():
    return "<H1> Testando segunda rota!!!"


#? ROTA: TESTE DE PARÂMETROS NA ROTA
@app.route('/test_parameter/<string:nome>/<int:idade>')
def pessoa(nome, idade):
    return jsonify({'Nome': nome, 'Idade': idade})


#? ROTA: INDUZINDO AO ERRO H12 DE TIMEOUT E POR ELA, SOLUÇÕES
@app.route('/timeout')
def timeout():
    thread = threading.Thread(target=long_task)
    thread.start()  # Inicia a tarefa sem bloquear a resposta HTTP
    return jsonify({"message": "Tarefa iniciada, verifique os logs para status do time.sleep"}), 202


def start_task():
    task_id = str(len(tasks) + 1)  # Gera um ID simples
    tasks[task_id] = "Em andamento"
    
    thread = threading.Thread(target=long_task, args=(task_id,))
    thread.start()

    return jsonify({"message": "Tarefa iniciada", "task_id": task_id}), 202


@app.route('/status/<task_id>')
def get_status(task_id):
    status = tasks.get(task_id, "Não encontrada")
    return jsonify({"task_id": task_id, "status": status})

# Main
if __name__ == "__main__":
    app.run(debug=True)