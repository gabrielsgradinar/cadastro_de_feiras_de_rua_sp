from flask import current_app, Blueprint

feira = Blueprint(
    "admin",
    __name__,
)


@feira.route("/")
def ola_mb():
    return "Olá Mercado Bitcon !"


def init_app(app):
    app.register_blueprint(feira)
