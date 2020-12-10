from flask import Flask, jsonify, g
from flask_cors import CORS
import models
from flask_login import LoginManager
from blueprints.plants import plant
from blueprints.users import user

DEBUG = True
PORT = 8000

app = Flask(__name__)

app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)

app.secret_key = "pennywenny"
login_manager = LoginManager()

login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    try:
        print("loading the following user")
        user = models.User.get_by_id(user_id)
        return user

    except models.DoesNotExist:
        return None

CORS(plant, origins=['http://localhost:3000', 'https://depak.herokuapp.com'], supports_credentials=True)
CORS(user, origins=['http://localhost:3000', 'https://depak.herokuapp.com'], supports_credentials=True)

app.register_blueprint(plant, url_prefix='/directory/plants/')
app.register_blueprint(user, url_prefix='/directory/users/')

'''
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_SAMESITE='None'
)
'''
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'hi'

if 'SANDBOX' == os.environ.get('FLASK_ENV'):
  print('\non heroku!')
  models.initialize()


if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)

