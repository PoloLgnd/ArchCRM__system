from flask import Flask, render_template, request, redirect, url_for
from models import Customer, Employee, Projects, Task, Transaction
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATEBASE_URL'] = 'sqlite://crm.db'
app.config['AQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
db.init_app(app)

with app.app_context():
    db.create_all()

# Дальше серверная логика 



@app.route('/')
def index():
    return render_template('index.html')

