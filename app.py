from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Função para inicializar o banco de dados
def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS livros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                imagem_url TEXT NOT NULL
            )
        """)
        print("Banco de dados criado ou já existente!")

# Inicializa o banco de dados ao rodar o app
init_db()

# Página inicial (GET /)
@app.route('/')
def home_page():
    return '<h2>Bem-vindo à API de Livros! Doe um livro para nossa biblioteca.</h2>'

# Rota para cadastrar um livro (POST /doar)
@app.route('/doar', methods=['POST'])
def doar():
    dados = request.get_json()

    titulo = dados.get('titulo')
    categoria = dados.get('categoria')
    autor = dados.get('autor')
    imagem_url = dados.get('imagem_url')

    # Verifica se todos os campos estão preenchidos
    if not all([titulo, categoria, autor, imagem_url]):
        return jsonify({'erro': 'Todos os campos são obrigatórios'}), 400

    # Insere o livro no banco de dados
    with sqlite3.connect('database.db') as conn:
        conn.execute("""
            INSERT INTO livros (titulo, categoria, autor, imagem_url)
            VALUES (?, ?, ?, ?)
        """, (titulo, categoria, autor, imagem_url))
        conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201

# Rota para listar todos os livros cadastrados (GET /livros)
@app.route("/livros", methods=["GET"])
def listar_livros():
    """
    Retorna todos os livros cadastrados no banco de dados.
    """

    with sqlite3.connect("database.db") as conn:
        # Consulta todos os livros na tabela
        livros = conn.execute("SELECT * FROM livros").fetchall()

    # Organiza os livros no formato JSON
    livros_formatados = []
    for livro in livros:
        livro_dict = {
            "id": livro[0],
            "titulo": livro[1],
            "categoria": livro[2],
            "autor": livro[3],
            "imagem_url": livro[4]
        }
        livros_formatados.append(livro_dict)

    return jsonify(livros_formatados)

# Rodando a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
