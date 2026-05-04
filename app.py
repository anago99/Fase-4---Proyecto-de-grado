from flask import Flask
from mongoengine import connect
from routes.categories import categories_bp
from routes.products import products_bp
from routes.home import home_bp
from routes.login import login_bp
from models.models import User
from config import config
import os
import flask_login
app = Flask(__name__)
app.secret_key = os.urandom(24)

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

app.register_blueprint(categories_bp)
app.register_blueprint(products_bp)
app.register_blueprint(home_bp)
app.register_blueprint(login_bp)



if __name__ == '__main__':
    connect(host=config['CONNECTION_DB'])
    print("Connected to MongoDB")


    if config['DEBUG']:
        app.run(threaded=True, port=config['PORT'], debug=config['DEBUG'])
    else:
        app.run(host=config['HOST'], port=config['PORT'],
                debug=config['DEBUG'])
