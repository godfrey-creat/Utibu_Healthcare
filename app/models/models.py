from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt

class Medication(db.Model, UserMixin):
    id = db.Column(db.String(50), primary_key=True)
    medication = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Medication('{self.medication}', '{self.quantity}')"
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='user')
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(28), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Users('{self.first_name}', '{self.last_name}', '{self.email}', '{self.phone}')" 


class LegacyOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    delivery_method = db.Column(db.String(50), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"LegacyOrder('{self.medication}', '{self.quantity}', '{self.delivery_method}', '{self.payment_method}')"
    
class Order(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    medication = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Pending')
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return f"Orders('{self.medication}', '{self.quantity}')"
