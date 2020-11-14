from flask import current_app, Blueprint, jsonify
from controller import listar_todas_as_feiras

feira = Blueprint(
    "admin",
    __name__,
)


@feira.route("/")
def ola_mb():
    return "Olá Mercado Bitcon !"


@feira.route("/feiras", methods=['GET'])
def feiras():
    feiras = listar_todas_as_feiras()
    return jsonify(feiras)


def init_app(app):
    app.register_blueprint(feira)
