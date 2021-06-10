from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
#db = Database()
DB_NAME = "database.db"
db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "afafsdgsshsh"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    from .views import views
    from .auth import auth  
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/login')
    
    db.init_app(app)
    
    create_database(app)
    loginManager = LoginManager()
    loginManager.login_view = 'auth.login'
    loginManager.init_app(app)

    from .model.User import User
    @loginManager.user_loader
    def find_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    #if not path.exists('CookBook/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')


