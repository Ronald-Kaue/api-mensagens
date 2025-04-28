from flask import render_template, Flask
import json
import os

app = Flask(__name__)

database = os.past.exist("db.json")



@app.route('/get_mensagens')
def get_mensagens():
	mensagens = requests.get("https://bug-free-chainsaw-ww4x4r4945q3gq4-3000.app.github.dev/mensagens")
	dicionario = json.loads(mensagens.text)
	lista_msg = print(dicionario['mensagens'])
	return lista_msg


if __name__ == '__main__':
	app.run()