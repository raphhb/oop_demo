# Campus Counter — Django + Python OOP Demo
A complete local Mini POS simulator for PELEC 1. Python 3.10+ required.

## Run on Windows
Extract the ZIP first. Open a terminal in the folder containing manage.py.
```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python manage.py runserver
```
If PowerShell blocks activation, use Command Prompt, or run `.venv\Scripts\python.exe` instead of `python` for the last two commands.

## Run on macOS / Linux
```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py runserver
```
Open http://127.0.0.1:8000/ . Stop with Ctrl+C. Internet is needed only to install Django. No migrate command, database, account, API key, or admin setup is needed.

## What you can demonstrate
- Search six products; add items; update quantities; set quantity to 0 to remove.
- Food: buying at least 3 gives 10% off that product line.
- Accessories: every second item is half price.
- Select a fictional customer discount and press Apply.
- Enter cash; complete the sale; view change and print the receipt.
- Invalid quantities, empty checkout, and insufficient cash are checked in Python.

## Code map
| File | Purpose |
|---|---|
| shop/oop/domain.py | Ordinary Python classes and all calculation rules |
| shop/catalog.py | Six predefined product objects |
| shop/views.py | Process forms, rebuild cart, call Python objects, render page |
| shop/templates/shop/index.html | HTML and Django template expressions |
| shop/static/shop/style.css | Responsive layout and print styling |
| shop/static/shop/script.js | Product search and printing |
| config/settings.py | Database-free Django configuration |
| TEACHING_GUIDE.md | Demonstration script, concept map, and exercises |

Run checks: `python manage.py check` and `python manage.py test`.

## State and limitations
The small cart contains product IDs and quantities in a signed browser-session cookie. Objects are reconstructed on each request. Cookies are signed, not encrypted: do not store confidential data. Closing the browser normally expires this session, although browser session restoration can retain cookies. Restarting Django does NOT automatically empty carts because the locally generated secret is reused. Use Reset to clear them. Each browser session has its own cart; tabs in the same browser share it.

Receipts appear only on the checkout response and are not archived. Refreshing that response can resubmit checkout; because the cart is already cleared, the app then reports an empty cart. Use Start next sale after printing. This deliberately small simulation has no stock tracking, saved transactions, authentication, real payments, or production deployment configuration. DEBUG is for localhost teaching only. Prices and discounts are invented classroom rules.

Reference: https://docs.djangoproject.com/en/5.2/topics/http/sessions/#using-cookie-based-sessions
