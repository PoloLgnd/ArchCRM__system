from extensions import db

# Модель Клиента
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    company = db.Column(db.String(100), nullable=True)

    # Связь со сделками (каскадное удаление: при удалении пользователя удаляется и его сделки)
    deals = db.relationship('Deal', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'

# Модель Сделки
class Deal(db.Model):
    __tablename__ = 'deals'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Новая') # Новая, В работе, Выиграно, Проиграно
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)

    def __repr__(self):
        return f'<Deal {self.title}>'