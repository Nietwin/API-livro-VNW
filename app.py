from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS livros(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            autor TEXT NOT NULL,
            imagem_url TEXT NOT NULL)""")

init_db()

@app.route('/')
def home():
    return '<h2>Bem-vindo à Biblioteca Online!</h2>'

@app.route('/doar', methods=['POST'])
def doar():
    dados = request.get_json()
    if not all([dados.get('titulo'), dados.get('categoria'), dados.get('autor'), dados.get('imagem_url')]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400
    
    with sqlite3.connect('database.db') as conn:
        conn.execute("INSERT INTO livros (titulo, categoria, autor, imagem_url) VALUES (?, ?, ?, ?)", 
                     (dados['titulo'], dados['categoria'], dados['autor'], dados['imagem_url']))
        conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso"}), 201

@app.route('/livros', methods=['GET'])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
        livros = conn.execute("SELECT * FROM livros").fetchall()

    return jsonify([{"id": livro[0], "titulo": livro[1], "categoria": livro[2], "autor": livro[3], "imagem_url": livro[4]} for livro in livros])

if __name__ == '__main__':
    app.run(debug=True)
