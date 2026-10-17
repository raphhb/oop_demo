from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .catalog import make_catalog
from .oop.domain import Cart, Discount, StudentDiscount, ClubDiscount, CheckoutError

POLICIES = {'regular': Discount, 'student': StudentDiscount, 'club': ClubDiscount}

@require_http_methods(['GET', 'POST'])
def index(request):
    catalog = make_catalog()
    cart = Cart(catalog, request.session.get('cart', {}))
    policy_key = request.session.get('policy', 'regular')
    error, receipt = '', None
    if request.method == 'POST':
        try:
            action = request.POST.get('action')
            if action == 'add':
                cart.add(request.POST.get('product_id'))
            elif action == 'quantity':
                cart.set_quantity(request.POST.get('product_id'), request.POST.get('quantity'))
            elif action == 'policy':
                candidate = request.POST.get('policy')
                if candidate not in POLICIES:
                    raise CheckoutError('Select a valid discount.')
                policy_key = candidate
            elif action == 'reset':
                cart = Cart(catalog)
                policy_key = 'regular'
            elif action == 'checkout':
                receipt = cart.checkout(POLICIES[policy_key](), request.POST.get('cash', ''))
                cart = Cart(catalog)
            else:
                raise CheckoutError('Unknown action.')
            request.session['cart'] = cart.snapshot()
            request.session['policy'] = policy_key
            if receipt is None:
                return redirect('index')  # Refresh does not repeat an add operation.
        except CheckoutError as exc:
            error = str(exc)
    return render(request, 'shop/index.html', {
        'products': catalog.values(), 'lines': cart.lines(),
        'totals': cart.totals(POLICIES[policy_key]()), 'policy': policy_key,
        'error': error, 'receipt': receipt,
    })
