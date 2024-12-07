# Importa os módulos necessários
from flask import Flask, jsonify, json, abort, request
from Tarevas import Tarevas

# Criação de tarefas iniciais como objetos da classe Tarevas
cuzinhar = Tarevas("Jantar", "fazer panqueca para o jantar")
estudar = Tarevas("programar um pouco", "fazer o desafio do gpt", True)
plata = Tarevas("molhar as plantas", "botar bastante agual no gira sol e pouco no cacto")

# Lista de tarefas simulando um banco de dados
tarevas = [plata, estudar, cuzinhar]

# Inicializa a aplicação Flask
app = Flask(__name__)

# Rota raiz para verificar o status do servidor
@app.route("/")
def index():
    return "flask on"

# Tratamento para erros 404 (não encontrado)
@app.errorhandler(404)
def erro404(erro):
    return (jsonify(erro=str(erro)), 404)

# Tratamento para erros 400 (requisição inválida)
@app.errorhandler(400)
def erro400(erro):
    return (jsonify(erro=str(erro)), 400)

# Rota para listar todas as tarefas
@app.route("/api/tarevas")
def get_tarevas():
    tareva_dict = []
    for tareva in tarevas:
        tareva_dict.append(tareva.__dict__)  # Converte cada tarefa em um dicionário
    return jsonify(tareva_dict)

# Rota para criar uma nova tarefa
@app.route("/api/tarevas", methods=["POST"])
def cria_post():
    data = json.loads(request.data)
    titulo = data.get("titulo")
    descricao = data.get("descricao")
    completo = data.get("completo")
    
    if not titulo:
        abort(400, "a Tareva tem que ter um titulo")

    if completo == "True":
        tareva = Tarevas(titulo=titulo, descricao=descricao, completa=True)
    else:
        tareva = Tarevas(titulo=titulo, descricao=descricao)
    
    tarevas.append(tareva)
    return {
        "id": tareva.id,
        "url": f"/api/tarevas/{tareva.id}/"
    }

# Função utilitária para buscar uma tarefa pelo ID ou retornar 404
def get_id_or_404(id):
    for tareva in tarevas:
        if id == tareva.id:
            return tareva
    abort(404, f"tareva do id {id} não encontrado")

# Rota para detalhar informações de uma tarefa específica
@app.route("/api/tarevas/<int:id>/")
def get_tareva_id(id):
    data = get_id_or_404(id)
    return jsonify(data.__dict__)

# Rota para alterar completamente uma tarefa existente
@app.route("/api/tarevas/<int:id>/", methods=["PUT"])
def alterar_post(id):
    data = request.get_json()
    titulo = data.get("titulo")
    descricao = data.get("descricao")
    completo = data.get("completa")
    
    if not titulo:
        abort(400, "a Tareva tem que ter um titulo")
    if not descricao:
        abort(400, "a Tareva tem que ter um descrição")
    if completo != "True" and completo != "False":
        abort(400, "a Tareva tem que ter se ta completa ou não")
    
    tareva = get_id_or_404(id)
    tareva.titulo = titulo
    tareva.descricao = descricao
    tareva.completa = completo

    return jsonify(tareva.__dict__)

# Rota para alterar parcialmente uma tarefa existente
@app.route("/api/tarevas/<int:id>/", methods=["PATCH"])
def alterar_parcialmente_post(id):
    data = request.get_json()
    tareva = get_id_or_404(id)
    
    if "titulo" in data.keys():
        titulo = data.get("titulo")
        if not titulo:
            abort(400, "a Tareva tem que ter um titulo")
        tareva.titulo = titulo
    
    if "descricao" in data.keys():
        descricao = data.get("descricao")
        if not descricao:
            abort(400, "a Tareva tem que ter um descrição")
        tareva.descricao = descricao
    
    if "completa" in data.keys():
        completo = data.get("completa")
        if completo != "True" and completo != "False":
            abort(400, "a Tareva tem que ter se ta completa ou não")
        tareva.completa = completo

    return jsonify(tareva.__dict__)

# Rota para deletar uma tarefa pelo ID
@app.route("/api/tarevas/<int:id>/", methods=["DELETE"])
def deleta_tareva_id(id):
    data = get_id_or_404(id)
    tarevas.remove(data)
    return jsonify(id=id)
