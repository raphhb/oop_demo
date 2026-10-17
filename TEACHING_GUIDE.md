# Instructor walkthrough — 25 to 35 minutes

## 1. Demonstrate the finished application (5 minutes)
1. Add three chicken sandwiches. Their original total is ₱195.00; FoodProduct returns ₱175.50.
2. Add three gel pens. AccessoryProduct returns ₱50.00 (₱20 + ₱10 + ₱20).
3. The subtotal is ₱225.50. Apply Student demo: discount ₱22.55, total ₱202.95.
4. Enter ₱100.00: explain the custom exception and show that the cart stays intact.
5. Enter ₱250.00: complete checkout; change is ₱47.05. Print the receipt.
6. Explain that data is temporary and no database is involved.

## 2. Trace the request (5 minutes)
An Add button submits an HTML POST form with a product ID and CSRF token. Django routes it to index(). The view rebuilds a Cart from the session, calls add(), saves a plain dictionary, and redirects to GET. The template displays totals that Python has computed. JavaScript only filters the displayed products and opens the print dialog.

## 3. Explain the OOP (10 minutes)
| Concept | Actual code | Observable result |
|---|---|---|
| Class and object | Product and the catalog's six instances | Each product has its own name and price |
| Inheritance | FoodProduct and AccessoryProduct inherit Product | Common construction and price access are reused |
| Polymorphism | Cart.lines() calls product.line_total(qty) | The same call applies different offers |
| Encapsulation | Cart.__quantities, set_quantity(), snapshot() | Validation protects state; snapshot returns a copy |
| Composition | Cart contains and uses Product objects | Cart delegates product pricing to the products |
| Custom exceptions | CheckoutError | Invalid cash and quantities show friendly messages |
| Exception handling | try/except in the Django view | A failed checkout does not crash the page |

Python double underscores use name mangling; they do not make an attribute absolutely inaccessible. Encapsulation here is the public interface and validation, not a security boundary.

Focus first on Product subclasses. Discount has two subclasses too, but their formula is intentionally simple. You can explain them later. Decimal avoids binary floating-point surprises with currency; the money() helper rounds at line and discount boundaries.

## 4. Show separation of concerns (5 minutes)
Ask: Would domain.py still work without Django? Yes. It imports only decimal. Could the interface change while preserving the rules? Yes. Could JavaScript's search change a price? No: totals come from Python. Does extending a Django model prove student-designed inheritance? This sample uses their own explicit hierarchy instead.

## Live student tasks
- Easy: add a regular product in make_catalog().
- Inheritance: create a BookProduct subclass with 15% off quantities of 2 or more; add an instance to the catalog.
- Polymorphism: confirm Cart.lines() needs no new if/elif type checks for BookProduct.
- Encapsulation: change the maximum quantity to 10 and demonstrate rejection of 11.
- Exception handling: explain why checkout keeps the cart after insufficient cash.
- Integration: add a new customer policy and connect its selection through the view and template.

## Suggested group adaptation
For three students: each implements a meaningful class, each explains one request from form to response, and each performs an individual modification. Rotate frontend, business logic, and integration roles. This is a reference demo: require original rules and features rather than an identical copy.

## Troubleshooting
- `No module named django`: activate the virtual environment and install requirements with that environment's Python.
- Template/static changes missing: hard refresh; ensure runserver is running from the extracted project.
- Port already in use: `python manage.py runserver 8001`, then open port 8001.
- CSRF error: open through localhost consistently and reload the page; do not remove CSRF protection.
- No database configured: this is intentional. Do not add auth/admin or run migrations for this demo.
