from flask import current_app, Blueprint, jsonify, request
from controller import listar_todas_as_feiras
from log import logger

feira = Blueprint(
    "admin",
    __name__,
)


@feira.route("/")
def ola_mb():
    logger.info(f"{request.method} - '{request.path}'")
    return {"message":"Hello Mercado Bitcon !"}


@feira.route("/feiras", methods=['GET'])
def feiras():
    feiras = listar_todas_as_feiras()
    logger.info(f"{request.method} - '{request.path}'")
    return jsonify(feiras)


def init_app(app):
    app.register_blueprint(feira)
