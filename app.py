from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'fljfjr2llh3l3jl3h3lh43j43ljl'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста авторизируйтесь для доступа к этой странице'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #@app.teardown_appcontext
    #def close_db(error):
    #    if hasattr(g, 'link_db'):
    #        g.link_db.close()

    #@app.route("/")
    #def index():
    #    return "index"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)