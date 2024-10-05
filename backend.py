from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///jogos.db"
db = SQLAlchemy(app)

@app.route("/jogos", methods=["GET"])
def get_jogos():
    jogos = Jogo.query.all()
    return jsonify([jogo.to_dict() for jogo in jogos])

@app.route("/jogos", methods=["POST"])
def create_jogo():
    data = request.get_json()
    jogo = Jogo(nome=data["nome"], descricao=data["descricao"], imagem=data["imagem"], categoria=data["categoria"])
    db.session.add(jogo)
    db.session.commit()
    return jsonify(jogo.to_dict()), 201

@app.route("/jogos/<int:jogo_id>", methods=["GET"])
def get_jogo(jogo_id):
    jogo = Jogo.query.get(jogo_id)
    if jogo is None:
        return jsonify({"error": "Jogo não encontrado"}), 404
    return jsonify(jogo.to_dict())

@app.route("/jogos/<int:jogo_id>/scores", methods=["GET"])
def get_scores(jogo_id):
    jogo = Jogo.query.get(jogo_id)
    if jogo is None:
        return jsonify({"error": "Jogo não encontrado"}), 404
    scores = jogo.scores.all()
    return jsonify([score.to_dict() for score in scores])

@app.route("/jogos/<int:jogo_id>/scores", methods=["POST"])
def create_score(jogo_id):
    jogo = Jogo.query.get(jogo_id)
    if jogo is None:
        return jsonify({"error": "Jogo não encontrado"}), 404
    data = request.get_json()
    score = Score(jogo_id=jogo_id, score=data["score"])
    db.session.add(score)
    db.session.commit()
    return jsonify(score.to_dict()), 201
