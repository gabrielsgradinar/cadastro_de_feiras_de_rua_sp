from flask import Blueprint, jsonify, request, Response
from werkzeug.exceptions import HTTPException
from feira.log import logger

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(HTTPException)
def handle_error(error):
    mensagem = error.description
    status_code = error.code
    response = {"erro": {"mensagem": mensagem}}
    logger.info(f"{request.method} - '{request.path}' - '{error.code}'")
    return jsonify(response), status_code


def init_app(app):
    app.register_blueprint(errors)
