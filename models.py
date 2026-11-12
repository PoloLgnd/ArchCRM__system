from extensions import db

# Клиенты
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    company = db.Column(db.String(100), nullable=False)

    # Связь со проектами (каскадное удаление: при удалении пользователя удаляется и его проекты)
    projects = db.relationship('Project', backref='customer', lazy=True)

# Сотрудники
class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False) # Разработчик, дизайнер и тд
    email = db.Column(db.String(120), unique=True, nullable=False) # Новая, В работе, Выиграно, Проиграно

    tasks = db.relationship('Task', backref='assignee', lazy=True)

# Проекты
class Projects(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default='Планирование') # Планирование, В работе, Завершен, На паузе
    budget = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    transactions = db.relationship('Transaction', backref='project', lazy=True, cascade='all, delete-orphan')

# Задачи (для Диаграммы Ганта и трекинга)
class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    status = db.Column(db.String(50), default='К выполнению') # К выполнению, В процессе, Готово
    start_date = db.Column(db.Date, nullable=True)
    due_date = db.Column(db.Date, nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeinKey('employee_id'), nullable=True)

# Бюджет
class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20), nullable=False) # Доход или Расход
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow)
    descripton = db.Column(db.String(200), nullable=True)

    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=True)
