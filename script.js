const express = require('express');
const mysql = require('mysql2/promise');
const app = express();

const db = mysql.createPool({
  host: 'localhost',
  user: 'your_username',
  password: 'your_password',
  database: 'your_database'
});

class Jogo {
  constructor(titulo, descricao, genero, plataforma) {
    this.titulo = titulo;
    this.descricao = descricao;
    this.genero = genero;
    this.plataforma = plataforma;
    this.categorias = [];
    this.avaliacoes = [];
  }

  toDict() {
    return {
      titulo: this.titulo,
      descricao: this.descricao,
      genero: this.genero,
      plataforma: this.plataforma,
      categorias: this.categorias.map(categoria => categoria.toDict()),
      avaliacoes: this.avaliacoes.map(avaliacao => avaliacao.toDict())
    };
  }
}

class Categoria {
  constructor(nome, descricao) {
    this.nome = nome;
    this.descricao = descricao;
    this.jogos = [];
  }

  toDict() {
    return {
      nome: this.nome,
      descricao: this.descricao,
      jogos: this.jogos.map(jogo => jogo.toDict())
    };
  }
}

class Avaliacao {
  constructor(nota, comentario) {
    this.nota = nota;
    this.comentario = comentario;
  }

  toDict() {
    return {
      nota: this.nota,
      comentario: this.comentario
    };
  }
}

app.use(express.json());
app.use(express.urlencoded({ extended: true }));

app.get('/', async (req, res) => {
  const jogos = await db.execute('SELECT * FROM jogos');
  res.render('index', { jogos: jogos.map(jogo => new Jogo(...jogo)) });
});

app.get('/jogo/:jogoId', async (req, res) => {
  const jogoId = req.params.jogoId;
  const jogo = await db.execute('SELECT * FROM jogos WHERE id = ?', [jogoId]);
  if (jogo) {
    res.render('jogo', { jogo: new Jogo(...jogo) });
  } else {
    res.status(404).send('Jogo não encontrado');
  }
});

app.post('/criar_jogo', async (req, res) => {
  const { titulo, descricao, imagem } = req.body;
  await db.execute('INSERT INTO jogos (titulo, descricao, imagem) VALUES (?, ?, ?)', [titulo, descricao, imagem]);
  res.send('Jogo criado com sucesso!');
});

app.post('/editar_jogo/:jogoId', async (req, res) => {
  const jogoId = req.params.jogoId;
  const { titulo, descricao, imagem } = req.body;
  await db.execute('UPDATE jogos SET titulo = ?, descricao = ?, imagem = ? WHERE id = ?', [titulo, descricao, imagem, jogoId]);
  res.send('Jogo editado com sucesso!');
});

app.delete('/deletar_jogo/:jogoId', async (req, res) => {
  const jogoId = req.params.jogoId;
  await db.execute('DELETE FROM jogos WHERE id = ?', [jogoId]);
  res.send('Jogo deletado com sucesso!');
});

app.listen(3000, () => {
  console.log('Server listening on port 3000');
});
