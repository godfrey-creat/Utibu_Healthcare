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
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc:///latency_database' #Microsoft SQL
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

@app.route('/')
def index():
    return render_template('landing_page/index.html')

@app.errorhandler(404)
def error_404(error):
    return jsonify(error="Not found"), 404

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
            # Authentication failed, handle accordingly
            return render_template('login.html', error="Invalid username or password")
    return render_template('login.html')

@app.route('/user_registration', methods=['GET', 'POST'])
def user_registration():
    form = RegistrationForm
    if request.method == 'POST':
        # You should add code here to register the user
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
        hashed_password bcrypt.generate_password_hash(password).decode('utf-8')

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
    if request.method == 'POST':
        # You should add code here to place an order
        def validate_order(order_details):
            medication = order_details.get('medication')
            quantity = order_details.get('quantity')
            
            if not medication or not quantity:
                return False, "Medication and quantity are required fields."
            
            # Check if medication is available in inventory
            is_available, error_message = check_inventory(medication, quantity)
            if not is_available:
                return False, "Medication is not available"
            return True, None
        
        # Custom function to check if medication is available in inventory
        def check_inventory(medication, quantity):
            available_quantity = get_available_quantity_from_inventory(medication)
            if available_quantity < quantity:
                return False, f"Not enough stock availablle for medication: {medication}. Available quantity: {available_quantity}"
            return True, None
        
        #custom function to save order details to the legacy database.
        def save_order_to_legacy_database(order_details):
            try:
                #connect to legacy database
                legacy_database_conn = legacy_database_connector.connect()
                #insert order details to legacy db
                cursor = legacy_database_conn.cursor()
                cursor.execute("INSERT INTO orders (medication, quantity) VALUES (%s, %s)", (order_details['medication'], order_details['quantity']))
                legacy_database_conn.commit()
                cursor.close()

                #close the database connection
                legacy_database_conn.close()

                return True, None
            except Exception as e:
                return False, str(e)  # Error occurred while saving order.
        pass
    return render_template('order.html')

if __name__ == '__main__':
    app.run(debug=True)
