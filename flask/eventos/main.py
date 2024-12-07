from flask import Flask, jsonify, abort, make_response, request, json
from evento import Evento
from evento_on import EventoOn

app = Flask(__name__)

ev = Evento("aula de musica", "musica e cia")
ev_on = EventoOn("aula dde java")
ev_on2 = EventoOn("aula de excel")
evento = [ev, ev_on, ev_on2]

@app.errorhandler(400)
def nao_encontrado(erro):
    return (jsonify(erro=str(erro)), 400) 

@app.errorhandler(404)
def nao_encontrado(erro):
    return (jsonify(erro=str(erro)), 404) 

@app.route("/")
def index():
    return "<h1>teste de flask</h1>"

@app.route("/api/eventos/")
def listar_evento():
    evento_dict = []
    for ev in evento:
        evento_dict.append(ev.__dict__)

    return jsonify(evento_dict)

@app.route("/api/eventos/", methods=["post"])
def cria_eventos():
    #parsing
    data = json.loads(request.data)
    nome = data.get("nome")
    local = data.get("local")

 #validade
    if not nome:
        abort (400, "'nome' precisa ser informado")


 # criando eventos
    if local:
        eventos = Evento(nome = nome, local = local)
    else:
        eventos = EventoOn(nome = nome)
   
    evento.append(eventos)

    return {
        "id": eventos.id,
        "url":  f"/api/eventos/{eventos.id}/"
    }

def get_evento_or_404(id):
    for ev in evento:
        if ev.id  == id:
            return ev
    abort(404, "evento não  encontrado")

@app.route("/api/eventos/<int:id>/")
def id_evento(id):
    ev = get_evento_or_404(id)
    return jsonify(ev.__dict__)
        
    #data = {"err0": "no equixiste este evento"}
    #return make_response(jsonify(data), 404)

@app.route("/api/eventos/<int:id>/", methods=["DELETE"])
def deletar_evento(id):
    ev = get_evento_or_404(id)
    evento.remove(ev)
    return jsonify(id=id)        

@app.route("/api/eventos/<int:id>/", methods=["PUT"])
def editar_evento(id):
    
   #parsing
    data = request.get_json()
    nome = data.get("nome")
    local = data.get("local")

 #validade
    if not nome:
        abort (400, "'nome' precisa ser informado")
    if not local:
        abort (400, "'local' precisa ser informado")
    
    ev = get_evento_or_404(id)
    ev.nome= nome
    ev.local = local

    return jsonify(ev.__dict__)

@app.route("/api/eventos/<int:id>/", methods=["PATCH"])
def editar_evento_parcial(id):
    
   #parsing
    data = request.get_json()
    #{} -> não quero alterar nada
    #{"nome": ""} -> apagar nome -> não pode!
    #{"nome": "aula de java"}
    ev = get_evento_or_404(id)
    
    if "nome" in data.keys():
        nome = data.get("nome")    
        if not nome:
         abort (400, "'nome' precisa ser informado")
        ev.nome= nome

    if"local" in data.keys():   
        local = data.get("local")
        if not local:
            abort (400, "'local' precisa ser informado")
        ev.local = local

    return jsonify(ev.__dict__)


app.run(debug=True)