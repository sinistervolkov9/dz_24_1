import stripe
from config.settings import STRIPE_SECRET_KEY
# from forex_python.converter import CurrencyRates

stripe.api_key = STRIPE_SECRET_KEY


# def convert_rub_to_dollars(amount):
#     """Конвертирует рубли в доллары"""
#     c = CurrencyRates()
#     rate = c.get_rate('RUB', 'USD')
#     return int(amount * rate)


# def create_sprite_price(amount):
#     stripe.Price.create(
#         currency="rub",
#         unit_amount=amount * 100,
#         product_app={'name': 'Payment'},
#     )
#
#
# def create_stripe_session(price):
#     session = stripe.checkout.Session.create(
#         success_url='http://127.0.0.1:8000/',
#         line_items=[{'price': price.get('id'), 'quantity': 1}],
#         model='payment',
#     )
#
#     return session.get('id'), session.get('url')

def create_stripe_product(name: str):
    return stripe.Product.create(name=name)


def create_stripe_price(product_id: str, unit_amount: int, currency: str = 'usd'):
    return stripe.Price.create(
        product=product_id,
        unit_amount=unit_amount,
        currency=currency,
    )


def create_checkout_session(price_id: str, success_url: str, cancel_url: str):
    return stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
