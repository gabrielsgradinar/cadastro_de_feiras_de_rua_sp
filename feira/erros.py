from flask import Blueprint, jsonify
from werkzeug.exceptions import HTTPException

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(HTTPException)
def handle_error(error):
    mensagem = error.description
    status_code = error.code
    response = {"erro": {"mensagem": mensagem}}

    return jsonify(response), status_code


def init_app(app):
    app.register_blueprint(errors)
