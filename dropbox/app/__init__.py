from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson.objectid import ObjectId



mongo = PyMongo()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/dropbox_clone'

    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None

    # Register Blueprints
    from .routes import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app
