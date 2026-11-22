from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(200), nullable=False)
    medicamentos = db.relationship('Medicamento', backref='usuario', lazy=True)

class Medicamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    dose = db.Column(db.String(50), nullable=False)        # Ex: "1 comprimido"
    horario = db.Column(db.String(5), nullable=False)      # Formato "HH:MM" para ordenação
    turno = db.Column(db.String(20), nullable=False)       # Manhã, Tarde ou Noite
    estoque_atual = db.Column(db.Integer, nullable=False)  # Quantidade na caixa
    historico = db.relationship('HistoricoDose', backref='medicamento', lazy=True, cascade="all, delete-orphan")

class HistoricoDose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medicamento_id = db.Column(db.Integer, db.ForeignKey('medicamento.id'), nullable=False)
    data_hora = db.Column(db.DateTime, default=datetime.now)