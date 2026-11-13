from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, logout_user, login_user, login_required, current_user  
from extensions import db
from models import Customer, Employee, Project, Task, Transaction
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

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
    total_projects = Project.query.count()
    income = db.session.query(db.func.sum(Transaction.amount)).filter_by(type='Доход').scalar() or 0.0 # Доходы
    expense = db.session.query(db.func.sum(Transaction.amount)).filter_by(type='Расход').scalar() or 0.0 # Расходы
    net_profit = income - expense # Прибыль

    projects = Project.query.all()
    return render_template('index.html',
                           total_projects=total_projects,
                           income=income,
                           expense=expense,
                           net_profit=net_profit,
                           projects=projects)

@app.route('/projects', method=['GET', 'POST'])
def projects():
    if request.method == 'POST':
        name = request.form['name']
        budget = float(request.form['budget'])
        customer_id = int(request.form['customer_id'])

        # Сейвово парсим даты, если они есть
        start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form['start_date'] else None
        end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date() if request.form['end_date'] else None

        # Создаём объект проекта 
        new_proj = Project(name=name, budget=budget, customer_id=customer_id, start_date=start_date, end_date=end_date)

        # Сохраняем в БД
        db.session.add(new_proj)
        db.session.commit()
        return redirect(url_for('projects'))

    elif request.method == 'GET':
        all_projects = Project.query.all()
        customers = Customer.query.all()
        employees = Employee.query.all()
        return render_template('projects.html', projects=all_projects, customers=customers, employees=employees)


# Далее функции добавления к проекту и управления финансами  

@app.route('/projrct/<intLproject_id>/add_task', methods=['POST'])
def add_task(project_id):
    title = request.form['title']
    employee_id = int(request.form['employee_id']) if request.form['emoloyee_id'] else None
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date() if request.form['due_date'] else None
    due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date() if request.form['due_date'] else None

    # Создаём задачу, жестко привязывая её к конкретному project_id из URL
    task = Task(title=title, project_id=project_id, employee_id=employee_id, start_date=start_date, due_date=due_date)
    db.session.add(task)
    db.session.commit()
    return redirect(url_for('projects'))

@app.route('/finance', methods=['GET', 'POST'])
def finance():
    if request.method == 'POST':
        type_ = request.form['type']
        amount = float(request.form['amount'])
        category = request.form['category']
        project_id = int(request.form['project_id']) if request.form['project_id'] else None

        db.session.add(Transaction(type=type_, amount=amount, category=category, project_id=project_id))
        db.session.commit()
        return redirect(url_for('finance'))

    elif request.method == 'GET':
        transactions = Transaction.query.order_by(Transaction.id.desc()).all()
        projects = Project.query.all()
        return render_template('finance.html', transactions=transactions, projects=projects)

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
