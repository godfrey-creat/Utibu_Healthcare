import os
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_bcrypt import bcrypt
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from app.forms.form import LoginForm, OrderForm, RegistrationForm
from app.models.models import db, User, Order  # Import your database models
#import legacy_database_connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'latency_database_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://pharmacist:utibu@Microsoft SQL Server/latency_database?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

#Initialise SQLAlchemy with Flask app
db.init_app(app)

# Assuming you have a User model for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Define custom error handler for 404
@app.errorhandler(404)
def error_404(error):
    return jsonify(error="Not found"), 404

# Add app_context() block to wrap the relevant code
with app.app_context():
    @app.route('/')
    def index():
        return render_template('landing_page/index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login_route():
        form = LoginForm
        if request.method == 'POST':
            username = form.username.data
            password = form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for('home.html'))
            else:
                return render_template('login.html', error="Invalid username or password")
        return render_template('login.html')

    @app.route('/user_registration', methods=['GET', 'POST'])
    def user_registration():
        form = RegistrationForm
        if request.method == 'POST':
            username = form.username.data
            email = form.email.data
            phone = form.phone.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            users = User.querry.filter_by(email).first()
            if users:
                return render_template('forms/user_reg.html', form=form, msg='user already exists')
            if password != confirm_password:
                return render_template('forms/user_reg.html', form=form, msg='Password does not match')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(
                username=username,
                email=email,
                phone=phone,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect('login_route', msg='Registration successful, Login now.')
        return render_template('forms/user_reg.html', form=form)

    @app.route('/order', methods=['GET', 'POST'])
    @login_required
    def order():
        form = OrderForm
        if request.method == 'POST':
            # You should add code here to place an order
            pass
        return render_template('order.html')

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

