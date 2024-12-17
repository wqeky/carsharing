from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_ECHO'] = True
SQLALCHEMY_TRACK_MODIFICATIONS = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/py_projects/carsharing/instance/car.db'
app.config['SECRET_KEY'] = 'your_secret_key'



# Инициализация расширений
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from app import routes


