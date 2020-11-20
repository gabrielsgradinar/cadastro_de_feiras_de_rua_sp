import click
from feira.db import db
import feira.model
from feira.controller import importar_csv


def init_app(app):
    @app.cli.command()
    def create_db():
        """Este comando inicializa o banco de dados"""
        db.create_all()

    @app.cli.command()
    def import_csv():
        arquivo = './DEINFO_AB_FEIRASLIVRES_2014.csv'
        print(importar_csv(arquivo))
