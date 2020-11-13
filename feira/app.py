from flask import Flask
import rotas
import db
import linha_de_comando


def create_app():
    app = Flask(__name__)
    rotas.init_app(app)
    db.init_app(app)
    linha_de_comando.init_app(app)

    return app
