from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mensagens.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Mensagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(500), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'texto': self.texto
        }

with app.app_context():
    db.create_all()

@app.route('/mensagens', methods=['GET'])
def listar_mensagens():
    mensagens = Mensagem.query.all()
    return jsonify([msg.to_dict() for msg in mensagens])

@app.route('/mensagens', methods=['POST'])
def adicionar_mensagem():
    data = request.json
    nova = Mensagem(texto=data['conteudo'])
    db.session.add(nova)
    db.session.commit()
    return jsonify(nova.to_dict()), 201

@app.route('/mensagens/<int:id>', methods=['DELETE'])
def deletar_mensagem(id):
    msg = Mensagem.query.get_or_404(id)
    db.session.delete(msg)
    db.session.commit()
    return '', 204

@app.route('/mensagens/<int:id>', methods=['PUT'])
def editar_mensagem(id):
    msg = Mensagem.query.get_or_404(id)
    data = request.json
    msg.texto = data.get('conteudo', msg.texto)
    db.session.commit()
    return jsonify(msg.to_dict())

if __name__ == '__main__':
    app.run(debug=True)