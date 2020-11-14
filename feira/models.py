from db import db


class Feira(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registro = db.Column(db.String(10), unique=True, nullable=False)
    nome = db.Column(db.String(80), unique=True, nullable=False)   
    distrito = db.Column(db.String(80), nullable=False)
    regiao = db.Column(db.String(80), nullable=False)    
    logradouro = db.Column(db.String(10), nullable=False)
    numero = db.Column(db.String(10), nullable=True)
    bairro = db.Column(db.String(10), nullable=False)
    referencia = db.Column(db.String(10), nullable=True)
    

    def __repr__(self):
        return "<Feira %r>" % self.name
