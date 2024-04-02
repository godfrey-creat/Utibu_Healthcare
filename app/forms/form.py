from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Log In')

class OrderForm(FlaskForm):
    medication = StringField('Medication Name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    delivery_method = SelectField('Delivery Method', choices=[('pick_up', 'Pick Up'), ('delivery', 'Delivery')], validators=[DataRequired()])
    payment_method = SelectField('Payment Option', choices=[('immediate', 'Pay Immediately'), ('later', 'Pay Later')], validators=[DataRequired()])
    submit = SubmitField('Place Order')

class RegistrationForm(FlaskForm):
    first_name = StringField('First_name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = IntegerField('Phone', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class OrderHistoryForm(FlaskForm):
    orders = StringField('Orders', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    medication = StringField('Medication', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    delivery_method = SelectField('Delivery Method', choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')],  validators=[DataRequired()])
    payment_method = SelectField('Payment Method', choices=[('credit_card', 'Credit Card'), ('cash', 'Cash')], validators=[DataRequired()])
    timestamp = StringField('Timestamp')    


