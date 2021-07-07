import unittest
import stripe
from config import Config
from app import create_app, db
from app.models import SankMerchDb as Merch


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


# Testing creation of payment intent
class StripeCheckout(unittest.TestCase):
    def test_payment_intent(self):
        stripe.api_key = "sk_test_51J9ZCCBUeaWrljhjmzDSI7l72P1dbtRAW5Ro9griA0xs4Ymg3DmeDahi7M29njUANK1AYUvuAp0PxXWtapDDRgam00gzLucYR0"
        transfer_amount = 60

        intent = stripe.PaymentIntent.create(
            amount=transfer_amount,
            currency='cad',
            payment_method_types=['card'],
            receipt_email='nick.mohamed5@gmail.com',
        )
        self.assertTrue(transfer_amount == intent['amount'])


# Testing creation and addition of Sank database
class SankMerchModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        m = Merch(id=1, name='T-Shirt', price = 35, imageLink='./static/assets/Sank_Chew_Air_E_color.svg',
                  description='Check out Sank Tees', quantity=5, isAvailable=True)
        db.session.add(m)
        add_check = Merch.query.get(1)
        self.assertTrue(add_check == m)


if __name__ == '__main__':
    unittest.main()