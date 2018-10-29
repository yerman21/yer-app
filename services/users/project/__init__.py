# Services/users/project/__init__.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# inicializamos la bd posgrest
db = SQLAlchemy()


def create_app(script_info=None):
    # instancia la app
    app = Flask(__name__)
    # estableciendo configuracion
    app_settings = os.getenv("APP_SETTINGS")
    # app.config.from_object("project.config.DevelopmentConfig")
    app.config.from_object(app_settings)
    # print(app.config, file=sys.stderr)

    # establece extensiones
    db.init_app(app)
    from project.api.users import users_blueprint
    app.register_blueprint(users_blueprint)

    # contexto shell para flask cli
    @app.shell_context_processor
    def ctx():
        return {'app': app, 'db': db}
    return app
