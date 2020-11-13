import click
from db import db
import models


def init_app(app):
    @app.cli.command()
    def create_db():
        """Este comando inicializa o db"""
        db.create_all()
