from decimal import Decimal
from django.test import SimpleTestCase, Client
from .catalog import make_catalog
from .oop.domain import Cart, Discount, StudentDiscount, CheckoutError

class POSRulesTests(SimpleTestCase):
    def test_polymorphic_promotions(self):
        cart = Cart(make_catalog(), {'sandwich': 3, 'pen': 3})
        self.assertEqual(cart.totals(Discount())['total'], Decimal('225.50'))
        self.assertEqual(cart.totals(StudentDiscount())['total'], Decimal('202.95'))
    def test_encapsulation_and_invalid_operations(self):
        cart = Cart(make_catalog(), {'pen': 1})
        copy = cart.snapshot(); copy['pen'] = 100
        self.assertEqual(cart.snapshot()['pen'], 1)
        for qty in ['1.5', '-1', '21']:
            with self.assertRaises(CheckoutError): cart.set_quantity('pen', qty)
        for cash in ['NaN', 'Infinity', '19', 'abc', '20.001']:
            with self.assertRaises(CheckoutError): cart.checkout(Discount(), cash)
    def test_checkout_change(self):
        receipt = Cart(make_catalog(), {'pen': 2}).checkout(Discount(), '100')
        self.assertEqual(receipt['change'], Decimal('70.00'))
    def test_workflow_and_separate_carts(self):
        client = Client()
        self.assertEqual(client.get('/').status_code, 200)
        client.post('/', {'action': 'add', 'product_id': 'pen'})
        self.assertEqual(client.session['cart'], {'pen': 1})
        self.assertEqual(Client().session.get('cart', {}), {})
        bad = client.post('/', {'action': 'checkout', 'cash': '1'})
        self.assertContains(bad, 'Cash is insufficient')
        good = client.post('/', {'action': 'checkout', 'cash': '50'})
        self.assertContains(good, 'Your receipt')
        self.assertEqual(client.session['cart'], {})
    def test_csrf(self):
        client = Client(enforce_csrf_checks=True)
        self.assertEqual(client.post('/', {'action': 'reset'}).status_code, 403)
