from .oop.domain import Product, FoodProduct, AccessoryProduct

def make_catalog():
    return {p.id: p for p in [
        FoodProduct('sandwich', 'Chicken sandwich', '65'),
        FoodProduct('cookie', 'Chocolate cookie', '25'),
        Product('juice', 'Mango juice', '40'),
        Product('notebook', 'Study notebook', '55'),
        AccessoryProduct('pen', 'Gel pen', '20'),
        AccessoryProduct('lanyard', 'Campus lanyard', '80'),
    ]}
