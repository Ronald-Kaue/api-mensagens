from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

past_json = 'db.json'

def carregar_info():
    if os.path.exists(past_json):
        with open(past_json, 'r') as f:
            return json.load(f).get("mensagens", [])
    return []

def gerar_id(mensagens):
    ids = []
    for msg in mensagens:
        try:
            ids.append(int(msg['id']))
        except (ValueError, TypeError):
            pass
    return max(ids, default=0) + 1

def salvar_info(mensagens):
    with open(past_json, 'w') as f:
        json.dump({"mensagens": mensagens}, f, indent=2)

@app.route('/mensagens', methods=['GET'])
def pegar_mensagens():
    return jsonify(carregar_info())

@app.route('/mensagens/<id>', methods=['GET'])
def pegar_mensagem(id):
    mensagens = carregar_info()
    for msg in mensagens:
        if msg['id'] == id:
            return jsonify(msg)
    return jsonify({"erro": "Mensagem não encontrada"}), 404

@app.route('/mensagens', methods=['POST'])
def adicionar_mensagem():
    nova_mensagem = request.json
    mensagens = carregar_info()

    nova_id = gerar_id(mensagens)
    nova_mensagem['id'] = nova_id

    mensagens.append(nova_mensagem)
    salvar_info(mensagens)
    return jsonify(nova_mensagem), 201

@app.route('/mensagens/<id>', methods=['PUT'])
def atualizar_mensagem(id):
    mensagens = carregar_info()
    for i, msg in enumerate(mensagens):
        if msg['id'] == int(id):
            mensagens[i]['conteudo'] = request.json['conteudo']
            salvar_info(mensagens)
            return jsonify(mensagens[i])
    return jsonify({"erro": "Mensagem não encontrada"}), 404

@app.route('/mensagens/<id>', methods=['DELETE'])
def deletar_mensagem(id):
    mensagens = carregar_info()
    mensagens = [msg for msg in mensagens if str(msg['id']) != str(id)]
    salvar_info(mensagens)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)