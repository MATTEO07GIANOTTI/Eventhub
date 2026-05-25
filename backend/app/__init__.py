from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.extensions import db, migrate, jwt, ma
from app.routes.auth import auth_bp
from app.routes.events import events_bp
from app.routes.admin import admin_bp
from app.routes.profile import profile_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(profile_bp)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
