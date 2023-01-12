from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from webapp.admin.routes import blueprint as admin_blueprint
from webapp.cart.routes import blueprint as cart_blueprint
from webapp.db import db
from webapp.catalogue.models import Artist, Product
from webapp.user.models import User
from webapp.user.routes import blueprint as user_blueprint
from webapp.catalogue.routes import blueprint as catalogue_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db, render_as_batch=True)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @app.route("/")
    def main():
        title = "Blackhole Inc"
        return render_template("main.html", page_title=title)

    app.register_blueprint(user_blueprint)
    app.register_blueprint(cart_blueprint)
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(catalogue_blueprint)


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    with app.app_context():
        db.create_all()

    return app
