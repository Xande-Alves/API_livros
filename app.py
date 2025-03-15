from flask import Flask, request, jsonify, Response
import sqlite3
import json

app = Flask(__name__)


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
        cursor = conn.execute(f"""
        SELECT * FROM LIVROS
        """)
        livros = [
            {
                "id": row[0],
                "titulo": row[1],
                "categoria": row[2],
                "autor": row[3],
                "imagem_url": row[4]
            }
            for row in cursor.fetchall()
        ]

    # Usamos Response para personalizar a saída e manter a ordem
    return Response(json.dumps(livros, ensure_ascii=False), mimetype="application/json"), 200


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
