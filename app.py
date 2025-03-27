from flask import Flask, request, jsonify, Response
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def vnw():
    return "<h1>A Vai na Web é a escola de tecnologia mais topada do Brasil!!!</h1>"


def init_db():
    with sqlite3.connect('database.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS LIVROS(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                imagem_url TEXT NOT NULL
            )
        ''')

init_db()


@app.route("/livros", methods = ["GET"])
def listar_livros():
    with sqlite3.connect("database.db") as conn:
        livros = conn.execute(f"SELECT * FROM LIVROS").fetchall()
        livros_formatados = []

        for item in livros:
            dicionario_livros = {
                    "id": item[0],
                    "titulo": item[1],
                    "categoria": item[2],
                    "autor": item[3],
                    "imagem_url": item[4]
            }
            livros_formatados.append(dicionario_livros)  

    return jsonify(livros_formatados),200


@app.route("/doar", methods=["POST"])
def doar():
    # Capturamos os dados enviados na requisição em formato JSON
    dados = request.get_json()

    # Extraímos as informações do JSON recebido
    titulo = dados.get("titulo")  # Obtém o título do livro
    categoria = dados.get("categoria")  # Obtém a categoria do livro
    autor = dados.get("autor")  # Obtém o nome do autor do livro
    imagem_url = dados.get("imagem_url")  # Obtém a URL da imagem do livro

    if not titulo or not categoria or not autor or not imagem_url:
        return jsonify({"erro":"Todos os campos são obrigatórios"}), 400

    with sqlite3.connect("database.db") as conn:
        conn.execute(f"""
        INSERT INTO LIVROS (titulo,categoria,autor,imagem_url) 
        VALUES ("{titulo}", "{categoria}", "{autor}", "{imagem_url}")
        """)

    conn.commit()

    return jsonify({"mensagem":"Livro cadastrado com sucesso"}), 201


if __name__ == "__main__":
    app.run(debug=True)
