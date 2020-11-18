from flask import Blueprint, jsonify, request
from controller import listar_todas_as_feiras, criar_feira, atualizar_feira
from log import logger

feira = Blueprint(
    "admin",
    __name__,
)


@feira.route("/")
def ola_mb():
    logger.info(f"{request.method} - '{request.path}'")
    return {"message": "Hello Mercado Bitcon !"}


@feira.route("/feiras", methods=["GET"])
def feiras():
    logger.info(f"{request.method} - '{request.path}'")
    feiras = listar_todas_as_feiras()
    return jsonify(feiras)


@feira.route("/feira", methods=["POST"])
def cria_feira():

    feira = request.get_json()
    logger.info(f"{request.method} - '{request.path}'")
    return jsonify(criar_feira(feira))


@feira.route("/feira/<registro>", methods=["PUT"])
def atualiza_feira(registro):
    logger.info(f"{request.method} - '{request.path}'")
    feira = request.get_json()
    return jsonify(atualizar_feira(feira, registro))


def init_app(app):
    app.register_blueprint(feira)
