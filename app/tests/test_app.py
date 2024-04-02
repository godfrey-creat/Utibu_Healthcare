import unittest
from app import app, db, create_db

class TestApp(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            create_db()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_route(self):
        response = self.app.post('/login', data=dict(
            email='test@example.com',
            login='user',
            password='password'
        ))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.app.post('/user_registration', data=dict(
            first_name='Test',
            last_name='User',
            email='test@example.com',
            phone='1234567890',
            password='password',
            confirm_password='password'
        ))
        self.assertEqual(response.status_code, 302)  # Redirect after registration

    def test_place_order(self):
        response = self.app.post('/place_order', data=dict(
            medication='paracetamol',
            quantity=10,
            delivery_method='express',
            payment_method='cash'
        ))
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Order placed successfully.')

    def test_order_history(self):
        response = self.app.get('/order_history')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data['order_history'], list)

if __name__ == '__main__':
    unittest.main()
