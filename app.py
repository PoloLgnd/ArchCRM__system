from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, logout_user, login_user, login_required, current_user  
from extensions import db
from models import Customer, Employee, Projects, Task, Transaction
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'blabla'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crm.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))

with app.app_context():
    db.create_all()

# Дальше серверная логика 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
