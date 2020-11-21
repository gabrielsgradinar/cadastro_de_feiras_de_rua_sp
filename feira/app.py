from flask import Flask
import feira.mvc.view as view
import feira.db as db
import feira.linha_de_comando as linha_de_comando
import feira.erros as erros


def create_app():
    app = Flask(__name__)
    erros.init_app(app)
    view.init_app(app)
    db.init_app(app)
    linha_de_comando.init_app(app)

    return app
