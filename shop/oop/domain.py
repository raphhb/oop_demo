"""Framework-independent business logic. Money uses Decimal, never floats."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def money(value):
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

class CheckoutError(Exception):
    """Expected invalid operation; safe to explain to the user."""

class Product:
    def __init__(self, product_id, name, price):
        self.id, self.name = product_id, name
        self.__price = money(price)
        if self.__price < 0:
            raise CheckoutError('Price cannot be negative.')
    @property
    def price(self):
        return self.__price
    def line_total(self, quantity):
        return money(self.price * quantity)
    def pricing_rule(self):
        return 'Regular unit price'

class FoodProduct(Product):
    def line_total(self, quantity):
        # Classroom promotion: 10% off this product when buying at least 3.
        total = super().line_total(quantity)
        return money(total * Decimal('0.90')) if quantity >= 3 else total
    def pricing_rule(self):
        return 'Buy 3 or more: 10% off the line'

class AccessoryProduct(Product):
    def line_total(self, quantity):
        # Classroom promotion: every second item is half price.
        pairs, single = divmod(quantity, 2)
        return money(self.price * (Decimal('1.5') * pairs + single))
    def pricing_rule(self):
        return 'Every second item: half price'

class Discount:
    rate = Decimal('0')
    label = 'Regular customer'
    def amount(self, subtotal):
        return money(subtotal * self.rate)

class StudentDiscount(Discount):
    rate = Decimal('0.10')
    label = 'Student demo discount (10%)'
    def amount(self, subtotal):
        return money(subtotal * self.rate)

class ClubDiscount(Discount):
    rate = Decimal('0.05')
    label = 'Club demo discount (5%)'
    def amount(self, subtotal):
        return money(subtotal * self.rate)

class Cart:
    def __init__(self, catalog, quantities=None):
        self.catalog = catalog
        self.__quantities = {}
        for key, quantity in (quantities or {}).items():
            self.set_quantity(key, quantity)
    def set_quantity(self, product_id, quantity):
        if product_id not in self.catalog:
            raise CheckoutError('Unknown product.')
        try:
            quantity = int(str(quantity))
        except (ValueError, TypeError):
            raise CheckoutError('Quantity must be a whole number.')
        if not 0 <= quantity <= 20:
            raise CheckoutError('Use a quantity from 0 to 20.')
        if quantity == 0:
            self.__quantities.pop(product_id, None)
        else:
            self.__quantities[product_id] = quantity
    def add(self, product_id):
        self.set_quantity(product_id, self.__quantities.get(product_id, 0) + 1)
    def snapshot(self):
        return dict(self.__quantities)  # Copy prevents callers mutating private state.
    def lines(self):
        result = []
        for key, qty in self.__quantities.items():
            product = self.catalog[key]
            # Polymorphism: no type checks; same method, different pricing behavior.
            result.append({'name': product.name, 'id': key, 'quantity': qty,
                           'price': product.price, 'total': product.line_total(qty)})
        return result
    def totals(self, discount):
        subtotal = sum((line['total'] for line in self.lines()), Decimal('0'))
        reduction = discount.amount(subtotal)
        return {'subtotal': money(subtotal), 'discount': reduction,
                'total': money(subtotal - reduction)}
    def checkout(self, discount, cash):
        if not self.__quantities:
            raise CheckoutError('Add a product before checking out.')
        try:
            cash = Decimal(cash)
            if not cash.is_finite() or cash < 0 or cash != money(cash):
                raise CheckoutError('Cash must be a nonnegative amount with at most 2 decimal places.')
        except (InvalidOperation, TypeError, ValueError):
            raise CheckoutError('Enter a valid cash amount.')
        totals = self.totals(discount)
        if cash < totals['total']:
            raise CheckoutError('Cash is insufficient. Please enter a larger amount.')
        return {**totals, 'cash': money(cash), 'change': money(cash - totals['total']),
                'lines': self.lines(), 'customer': discount.label}
