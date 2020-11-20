from flask import Flask
import feira.view
import feira.db
import feira.linha_de_comando
import feira.erros


def create_app():
    app = Flask(__name__)
    feira.erros.init_app(app)
    feira.view.init_app(app)
    feira.db.init_app(app)
    feira.linha_de_comando.init_app(app)

    return app
