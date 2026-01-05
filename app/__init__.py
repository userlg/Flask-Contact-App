import os

from dotenv import load_dotenv
from flask import Flask, flash, redirect, url_for

from .config import Config
from .extensions import db
from .routes.contacts import contacts_bp


def create_app() -> Flask:

    load_dotenv()

    app = Flask(__name__)

    app.config.from_object(Config)

    app.config["SECRET_KEY"] = os.getenv(
        "SECRET_KEY",
        app.config.get("SECRET_KEY", "dev_secret_key"))

    debug_value = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
    app.debug = debug_value

    db.init_app(app)

    print(f"Environment: {os.getenv('FLASK_ENV', 'development')}")

    app.register_blueprint(contacts_bp)

    with app.app_context():
        db.create_all()

    # Error handlers
    register_error_handlers(app)

    return app


def register_error_handlers(app):
    """Registra manejadores de errores centralizados."""
    
    @app.errorhandler(404)
    def not_found(error):
        flash("Recurso no encontrado", "error")
        return redirect(url_for("contacts.index")), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        flash("Error interno del servidor. Por favor, intente más tarde.", "error")
        return redirect(url_for("contacts.index")), 500

    @app.errorhandler(400)
    def bad_request(error):
        flash("Solicitud inválida", "error")
        return redirect(url_for("contacts.index")), 400
