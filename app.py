from flask import Flask, jsonify, Response, request
import time
import threading
import sys
from waitress import serve
import asyncio
from celery import Celery

app = Flask(__name__)


#* Dicionário para armazenar status das tarefas
tasks = {}  

#* FUNÇÃO: Força a aplicação a esperar 70 segundos antes de responder para verificar o erro de Timeout
def long_task(task_id):
    print("Tarefa iniciada!")  # Confirmação da inicialização
    #sys.stdout.flush()  # Força a exibição do print nos logs
    time.sleep(70)  # Simula uma tarefa longa
    tasks[task_id] = "Tarefa Concluida"
    print("Tarefa concluída!")  # É para aparecer após 70s
    #sys.stdout.flush()


#* FUNÇÃO: processo assíncrono
def generate():
    yield "Tarefa iniciada...\n"
    sys.stdout.flush()
    asyncio.run(asyncio.sleep(70))  # Espera sem travar o worker
    yield "Tarefa concluída!\n"
    sys.stdout.flush()


#! Configuração do Celery
app.config["CELERY_BROKER_URL"] = "rediss://:p06093b8898488be4026a791e27b680d79d75fcbc5cd3ebecc93fcf7fe7e67b04@ec2-34-237-159-195.compute-1.amazonaws.com:20850"
app.config["CELERY_RESULT_BACKEND"] = "rediss://:p06093b8898488be4026a791e27b680d79d75fcbc5cd3ebecc93fcf7fe7e67b04@ec2-34-237-159-195.compute-1.amazonaws.com:20850"

celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


#? ROTA 1: PADRÃO
@app.route('/')
def home():
    return "Hello World!"


#? ROTA 2: TESTE DE MUDANÇA DE ROTA
@app.route('/rota2')
def home2():
    return "<H1> Testando segunda rota!!!"


#? ROTA 3: TESTE DE PARÂMETROS NA ROTA
@app.route('/test_parameter/<string:nome>/<int:idade>')
def pessoa(nome, idade):
    return jsonify({'Nome': nome, 'Idade': idade})


#? ROTA 4: INDUZINDO AO ERRO H12 DE TIMEOUT E POR ELA, SOLUÇÕES
@app.route('/timeout')
def timeout():
    thread = threading.Thread(target=long_task)
    thread.start()  # Inicia a tarefa sem bloquear a resposta HTTP
    return jsonify({"message": "Tarefa iniciada, verifique os logs para status do time.sleep"}), 202


#! ROTA 5: INICIA UMA TAREFA
@app.route('/start-task', methods=["POST"])
def start_task():
    task_id = str(len(tasks) + 1)  # Gera um ID simples
    tasks[task_id] = "Tarefa em andamento"
    
    thread = threading.Thread(target=long_task, args=(task_id,))
    thread.start()

    return jsonify({"message": "Tarefa iniciada", "task_id": task_id}), 202


#? ROTA 6: VERIFICA O STATUS DA TAREFA e É COMPLEMENTAR A ROTA 5
@app.route('/status/<task_id>')
def get_status(task_id):
    status = tasks.get(task_id, "Tarefa nao encontrada")
    return jsonify({"task_id": task_id, "status": status})


#? ROTA 7: FLASK STREAMING
@app.route('/stream')
def stream():
    return Response(generate(), mimetype="text/plain")


#! ROTAS 8: CELERY + REDIS
@celery.task
def process_task(task_id):
    time.sleep(70)  # Simulando um processamento demorado
    return {"task_id": task_id, "status": "completed"}

@app.route("/start-celery-task", methods=["POST"])
def start_task():
    task = process_task.apply_async(args=["123"])  # Gera uma tarefa assíncrona
    return jsonify({"task_id": task.id}), 202

@app.route("/task-status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = process_task.AsyncResult(task_id)
    return jsonify({"task_id": task.id, "status": task.state})

# Main
if __name__ == "__main__":
    from waitress import serve
    print("Rodando com Waitress no Windows...")
    serve(app, host="0.0.0.0", port=8000)