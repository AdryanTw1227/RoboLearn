from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)

# Conecte-se ao banco de dados
cnx = mysql.connector.connect(
    user='seu_nome_de_usuario',
    password='sua_senha',
    host='localhost',
    database='seu_nome_do_banco_de_dados'
)

# Crie o cursor para executar comandos SQL
cursor = cnx.cursor()

class Jogo:
    def __init__(self, titulo, descricao, genero, plataforma):
        self.titulo = titulo
        self.descricao = descricao
        self.genero = genero
        self.plataforma = plataforma
        self.categorias = []
        self.avaliacoes = []

    def to_dict(self):
        return {
            'titulo': self.titulo,
            'descricao': self.descricao,
            'genero': self.genero,
            'plataforma': self.plataforma,
            'categorias': [categoria.to_dict() for categoria in self.categorias],
            'avaliacoes': [avaliacao.to_dict() for avaliacao in self.avaliacoes]
        }

class Categoria:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao
        self.jogos = []

    def to_dict(self):
        return {
            'nome': self.nome,
            'descricao': self.descricao,
            'jogos': [jogo.to_dict() for jogo in self.jogos]
        }

class Avaliacao:
    def __init__(self, nota, comentario):
        self.nota = nota
        self.comentario = comentario

    def to_dict(self):
        return {
            'nota': self.nota,
            'comentario': self.comentario
        }

def criar_jogo(titulo, descricao, imagem):
    cursor.execute('INSERT INTO jogos (titulo, descricao, imagem) VALUES (%s, %s, %s)', (titulo, descricao, imagem))
    cnx.commit()

def editar_jogo(jogo_id, titulo, descricao, imagem):
    cursor.execute('UPDATE jogos SET titulo = %s, descricao = %s, imagem = %s WHERE id = %s', (titulo, descricao, imagem, jogo_id))
    cnx.commit()

def deletar_jogo(jogo_id):
    cursor.execute('DELETE FROM jogos WHERE id = %s', (jogo_id,))
    cnx.commit()

@app.route('/')
def index():
    jogos = [Jogo(*jogo) for jogo in cursor.execute('SELECT * FROM jogos').fetchall()]
    return render_template('index.html', jogos=jogos)

@app.route('/jogo/<int:jogo_id>')
def jogo(jogo_id):
    jogo = cursor.execute('SELECT * FROM jogos WHERE id = %s', (jogo_id,)).fetchone()
    if jogo:
        return render_template('jogo.html', jogo=Jogo(*jogo))
    else:
        return 'Jogo não encontrado', 404

@app.route('/criar_jogo', methods=['GET', 'POST'])
def criar_jogo_view():
    if request.method == 'POST':
        criar_jogo(request.form['titulo'], request.form['descricao'], request.form['imagem'])
        return 'Jogo criado com sucesso!'
    return render_template('criar_jogo.html')

@app.route('/editar_jogo/<int:jogo_id>', methods=['GET', 'POST'])
def editar_jogo_view(jogo_id):
    if request.method == 'POST':
        editar_jogo(jogo_id, request.form['titulo'], request.form['descricao'], request.form['imagem'])
        return 'Jogo editado com sucesso!'
    jogo = cursor.execute('SELECT * FROM jogos WHERE id = %s ', (jogo_id,)).fetchone()
    if jogo:
        return render_template('editar_jogo.html', jogo=Jogo(*jogo))
    else:
        return 'Jogo não encontrado ', 404

@app.route('/deletar_jogo/<int:jogo_id>')
def deletar_jogo_view(jogo_id):
    deletar_jogo(jogo_id)
    return 'Jogo deletado com sucesso!'

if __name__ == '__main__':
    app.run(debug=True)
