#! /usr/bin/env python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://pharmacist:utibu@Microsoft SQL Server/latency_database?driver=ODBC+Driver+17+for+SQL+Server'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.api import app
from app.models.models import db

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )
