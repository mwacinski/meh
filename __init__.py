from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///website.sqlite3'
    app.secret_key = 'haha'
    db.init_app(app)
    ma.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()

    from .main import login_blueprint, dashboard_blueprint, logout_blueprint, \
        movie_blueprint

    app.register_blueprint(login_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(logout_blueprint)
    app.register_blueprint(movie_blueprint)

    return app
