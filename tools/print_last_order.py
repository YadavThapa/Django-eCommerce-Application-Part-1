# Script intended to be run via: python manage.py shell < tools/print_last_order.py
# It assumes the Django environment is already configured by manage.py shell.
try:
    from main.shop.models import Order
except (ImportError, ModuleNotFoundError):
    # If the module cannot be imported, report and re-raise
    import sys

    print('Failed to import Order model: module not found', file=sys.stderr)
    raise
except Exception as e:
    # If Django settings aren't configured or other config errors occur,
    # surface the error so the caller can run the script under manage.py shell.
    print('Failed to import Order model:', e)
    raise

o = Order.objects.order_by('-created_at').first()
if not o:
    print('No orders found')
else:
    def buyer_repr(order):
        if getattr(order, 'buyer_id', None):
            try:
                name = (
                    order.buyer.get_full_name()
                    or getattr(order.buyer, 'username', str(order.buyer))
                )
                email = getattr(order.buyer, 'email', '')
                return 'AUTH: {} <{}>'.format(name, email)
            except AttributeError:
                # Defensive: buyer object missing the expected attrs
                return 'AUTH: {}'.format(order.buyer)
        return (
            'GUEST: {} <{}>'
        ).format(getattr(order, 'guest_name', ''), getattr(order, 'guest_email', ''))

    print('Order ID:', getattr(o, 'order_id', str(o.pk)))
    created = getattr(o, 'created_at', None)
    if created:
        try:
            print('Created:', created.isoformat())
        except (AttributeError, TypeError):
            print('Created:', created)
    else:
        print('Created: (unknown)')
    print('Status:', getattr(o, 'status', '(unknown)'))
    print('Buyer:', buyer_repr(o))
    print('Total:', getattr(o, 'total_amount', '(unknown)'))
    print('Shipping:', getattr(o, 'shipping_address', '(none)') or '(none)')
    print('Items:')
    items = list(o.items.all())
    if not items:
        print('  (no items)')
        for it in items:
            pname = getattr(it, 'product_name', getattr(it, 'product', '(product)'))
            qty = getattr(it, 'quantity', '(qty)')
            unit = getattr(it, 'unit_price', '(price)')
            line = getattr(it, 'line_total', None)
            if line is None:
                try:
                    line = float(qty) * float(unit)
                except (TypeError, ValueError):
                    line = '(unknown)'
            print(' - {} x{} @ {} = {}'.format(pname, qty, unit, line))
    # Additional metadata if available
    print('\nRaw repr:')
    try:
        import json

        def safe_obj(obj):
            return str(obj)
        print(json.dumps({
            'id': getattr(o, 'order_id', o.pk),
            'created_at': getattr(o, 'created_at', None) and getattr(o, 'created_at').isoformat(),
            'status': getattr(o, 'status', None),
            'buyer': buyer_repr(o),
            'total': getattr(o, 'total_amount', None),
            'shipping': getattr(o, 'shipping_address', None),
            'items': [
                {
                    'product': (
                        getattr(
                            it,
                            'product_name',
                            getattr(it, 'product', safe_obj(getattr(it, 'product_id', None))),
                        )
                    ),
                    'qty': getattr(it, 'quantity', None),
                    'unit': getattr(it, 'unit_price', None),
                    'line': getattr(it, 'line_total', None),
                }
                for it in items
            ]
        }, default=safe_obj, indent=2))
    except (TypeError, ValueError):
        # JSON serialization failed for unexpected types; ignore safely
        pass
