from feira.db import db
from dataclasses import dataclass


@dataclass
class Feira(db.Model):
    __tablename__ = "feiras"

    id: int
    registro: str
    nome: str
    distrito: str
    regiao: str
    logradouro: str
    numero: str
    bairro: str
    referencia: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registro = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(80), unique=False, nullable=False)
    distrito = db.Column(db.String(80), nullable=False)
    regiao = db.Column(db.String(80), nullable=False)
    logradouro = db.Column(db.String(10), nullable=False)
    numero = db.Column(db.String(10), nullable=True)
    bairro = db.Column(db.String(10), nullable=False)
    referencia = db.Column(db.String(80), nullable=True)
