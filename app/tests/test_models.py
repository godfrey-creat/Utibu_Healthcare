import unittest
from app import db, Medication, User, LegacyOrder, Order

class TestModels(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_medication_model(self):
        medication = Medication(medication='paracetamol', quantity=100)
        db.session.add(medication)
        db.session.commit()

        self.assertIsNotNone(medication.id)
        self.assertEqual(medication.medication, 'paracetamol')
        self.assertEqual(medication.quantity, 100)

    def test_user_model(self):
        user = User(first_name='John', last_name='Doe', email='john@example.com', phone='1234567890', password='password')
        db.session.add(user)
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@example.com')
        self.assertEqual(user.phone, '1234567890')
        self.assertEqual(user.category, 'user')  # Default value
        self.assertIsNotNone(user.created_at)

    def test_legacy_order_model(self):
        legacy_order = LegacyOrder(medication='paracetamol', quantity=10, delivery_method='express', payment_method='cash')
        db.session.add(legacy_order)
        db.session.commit()

        self.assertIsNotNone(legacy_order.id)
        self.assertEqual(legacy_order.medication, 'paracetamol')
        self.assertEqual(legacy_order.quantity, 10)
        self.assertEqual(legacy_order.delivery_method, 'express')
        self.assertEqual(legacy_order.payment_method, 'cash')
        self.assertEqual(legacy_order.status, 'Pending')  # Default value
        self.assertIsNotNone(legacy_order.timestamp)

    def test_order_model(self):
        order = Order(medication='paracetamol', quantity=10)
        db.session.add(order)
        db.session.commit()

        self.assertIsNotNone(order.id)
        self.assertEqual(order.medication, 'paracetamol')
        self.assertEqual(order.quantity, 10)
        self.assertEqual(order.status, 'Pending')  # Default value
        self.assertIsNotNone(order.timestamp)

if __name__ == '__main__':
    unittest.main()
