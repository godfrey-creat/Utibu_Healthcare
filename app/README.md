# Application API

This Python script sets up a Flask application for handling user authentication, order placement, and order history functionalities. It includes routes for user login, registration, placing orders, and viewing order history.

## Prerequisites

- Python 3.x
- Flask
- Flask-Bcrypt
- Flask-Login
- Flask-Cors
- SQLAlchemy

## Setup

1. Install dependencies:

```bash
pip install flask flask-bcrypt flask-login flask-cors sqlalchemy
Run the Flask application:
bash
Copy code
python run.py.py
Usage
Access the landing page by navigating to / endpoint.
Register a new user by accessing /user_registration endpoint.
Login with existing credentials by accessing /login endpoint.
Place an order by accessing /place_order endpoint with the required parameters.
View order history by accessing /order_history endpoint.
Configuration
SECRET_KEY: Secret key for Flask session management.
SQLALCHEMY_DATABASE_URI: URI for the SQLite database file.
API_HOST: Host IP for running the Flask application (defaults to "0.0.0.0").
API_PORT: Port number for running the Flask application (defaults to "5000").

# Database Models

This Python script defines database models using SQLAlchemy for a Flask application. It includes models for users, medications, and orders.

## Models

### Medication

- **id**: Primary key of the medication.
- **medication**: Name of the medication.
- **quantity**: Quantity of the medication.

### User

- **id**: Primary key of the user.
- **first_name**: First name of the user.
- **last_name**: Last name of the user.
- **category**: Category of the user (e.g., user, admin).
- **email**: Email address of the user (unique).
- **phone**: Phone number of the user (unique).
- **password**: Hashed password of the user.
- **created_at**: Timestamp indicating when the user account was created.

### LegacyOrder

- **id**: Primary key of the order.
- **medication**: Name of the medication in the legacy order.
- **quantity**: Quantity of the medication in the legacy order.
- **delivery_method**: Method of delivery for the legacy order.
- **payment_method**: Payment method for the legacy order.
- **status**: Status of the order (e.g., Pending, Completed).
- **timestamp**: Timestamp indicating when the legacy order was placed.

### Order

- **id**: Primary key of the order.
- **medication**: Name of the medication in the order.
- **quantity**: Quantity of the medication in the order.
- **status**: Status of the order (e.g., Pending, Completed).
- **timestamp**: Timestamp indicating when the order was placed.

## Usage

These database models can be used within a Flask application to interact with a relational database. You can define relationships between these models, query the database, and perform CRUD operations.

## Dependencies

- Flask
- Flask-SQLAlchemy
- Flask-Bcrypt
- Flask-Login