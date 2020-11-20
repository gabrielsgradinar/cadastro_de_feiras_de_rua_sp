from flask import Blueprint, jsonify, request, Response
from feira.controller import atualizar_feira, criar_feira, excluir_feira, listar_todas_as_feiras, listar_feiras_por_filtro
from feira.log import logger

feira = Blueprint(
    "admin",
    __name__,
)

@feira.route("/")
def ola_mb():    
    logger.info(f"{request.method} - '{request.path}' - '{Response().status}'")
    return {"message": "Hello Mercado Bitcon !"}


@feira.route("/feiras", methods=["GET"])
def feiras():
    distrito = request.args.get('distrito')
    regiao = request.args.get('regiao')
    nome = request.args.get('nome')
    bairro = request.args.get('bairro')

    filtros = {
        "distrito": distrito if distrito else "",
        "regiao": regiao if regiao else "",
        "nome": nome if nome else "",
        "bairro": bairro if bairro else "",
    }
    
    valores = 0
    for valor in filtros.values():
        if valor != "":
            valores += 1

    logger.info(f"{request.method} - '{request.path}' - '{Response().status}'")
    if valores > 0:
        return jsonify(listar_feiras_por_filtro(filtros))
    else:        
        return jsonify(listar_todas_as_feiras())

@feira.route("/feira", methods=["POST"])
def cria_feira():
    logger.info(f"{request.method} - '{request.path}' - '{Response().status}'")
    feira = request.get_json()
    return jsonify(criar_feira(feira))


@feira.route("/feira/<registro>", methods=["PUT"])
def atualiza_feira(registro):
    logger.info(f"{request.method} - '{request.path}' - '{Response().status}'")
    feira = request.get_json()
    return jsonify(atualizar_feira(feira, registro))


@feira.route("/feira/<registro>", methods=["DELETE"])
def exclui_feira(registro):
    logger.info(f"{request.method} - '{request.path}' - '{Response().status}'")
    return jsonify(excluir_feira(registro))


def init_app(app):
    app.register_blueprint(feira)
