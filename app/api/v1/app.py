#!/usr/bin/python3
'''application API'''

import os
from os import getenv
from flask_cors import CORS
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_bcrypt import bcrypt, Bcrypt
from flask_login import LoginManager, login_user, current_user, login_required
from ...forms.form import LoginForm, OrderForm, RegistrationForm, OrderHistoryForm 
from app.models.models import db, User, Order, Medication # Import your database models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'latency_database_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # 'mssql+pyodbc:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)

# Initialise SQLAlchemy with Flask app
db.init_app(app)

# Assuming you have a User model for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

# Define custom error handler for 404
@app.errorhandler(404)
def error_404(error):
    return jsonify(error="Not found"), 404

@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler """
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler """
    return jsonify({"error": "Forbidden"}), 403

@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400

# Add app_context() block to wrap the relevant code
with app.app_context():
    @app.route('/')
    def index():
        return render_template('landing_page/index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login_route():
        form = LoginForm()
        orderform = OrderForm()
        if request.method == 'POST': # and form.validate_on_submit():
            email = form.email.data
            login = form.login.data
            password = form.password.data
           # users = User.query.all()
            
            # Check if login_as is 'user'
            if login == 'user':
                user = User.query.filter_by(email=email).first()
                if not user:
                    return render_template('forms/login.html', form=form, msg='Invalid credentials')
                if user and bcrypt.check_password_hash(user.password, password):
                    # Authentication successful, redirect to dashboard or user-specific route
                    return render_template('forms/order.html', orders=orderform)  # Replace 'user_dashboard' with your desired route
                    #return redirect(url_for('place_order'), form=orderform)
                else:
                    return render_template('forms/login.html', form=form, msg='Invalid credentials')
            else:
                return render_template('forms/order.html', form=orderform, msg='WELCOME TO UTIBU HEALTHCARE')
               # return redirect(url_for('place_order'), form=orderform)
        return render_template('forms/login.html', form=form)
    
    
    @app.route('/user_registration', methods=['GET', 'POST'])
    def user_registration():
        form = RegistrationForm()
        print('form available')
        if request.method == 'POST':
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            phone = form.phone.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            users = User.query.filter_by(email=email).first()
            if users:
                return render_template('forms/user_reg.html', form=form, msg='user already exists')
            if password != confirm_password:
                return render_template('forms/user_reg.html', form=form, msg='Password does not match')
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login_route', msg='Registration successful, Login now.'))
        return render_template('forms/user_reg.html', form=form)

    # Simulated pharmacy inventory (replace with actual database queries)
    latency_database = {
        'paracetamol': 100,
        'insulin': 50,
        'arithromycin': 250,
        # Add more medication
    }

   
    @app.route('/place_order', methods=['POST'])
    def place_order():
        form = OrderForm()
        try:
            # Get order details from the request
            medication = form.medication.data
            quantity = int(form.quantity.data)
            delivery_method = form.delivery_method.data
            payment_method = form.payment_method.data
           # email = form.email.data
           # phone = form.phone.data

            # Check if medication is in stock
            if medication in latency_database:
                if latency_database[medication] >= quantity:
                    # Order can be fulfilled
                    latency_database[medication] -= quantity
                    #confirmation_message = f"Order confirmed for {quantity} {medication}."
                    confirmation_message = "Order placed successfully."
                    #return jsonify({'message': confirmation_message, 'delivery_method': delivery_method, 'payment_method': payment_method})

                    #return redirect(url_for('order_history')) 
                    return jsonify({'message': confirmation_message, 'delivery_method': delivery_method, 'payment_method': payment_method})    
                else:
                    # Insufficient stock
                    return jsonify({'error': f"Insufficient stock for {medication}."})
            else:
                # Medication not found
                 return jsonify({'error': f"{medication} not available."})
        except Exception as e:
            return jsonify({'error': str(e)})
            #return redirect(url_for('order_history'), msg='Order place successfully!') 
        
    @app.route('/order_history', methods=['GET'])
    def order_history():
        form = OrderHistoryForm()
        # Retrieve order history for the logged-in user (you'll need to implement this logic)
        # Example: Fetch orders from a database based on user ID
        email = form.email.data  # Replace with your actual user authentication logic
        orders = form.oders.data(email)  # Replace with your database query
        # Format order history data (assuming each order is a dictionary with relevant details)
        formatted_orders = []
        for order in orders:
            formatted_order = {
                'medication': order['medication'],
                'quantity': order['quantity'],
                'delivery_method': order['delivery_method'],
                'payment_method': order['payment_method'],
                'timestamp': order['timestamp'],  # Add timestamp or date of order
            }
            formatted_orders.append(formatted_order)

        return jsonify({'order_history': formatted_orders})
   

# Run the Flask app
if __name__ == '__main__':
    db.create_all()
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
