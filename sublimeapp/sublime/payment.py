import json
import stripe

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# test secret API key.
stripe.api_key = 'sk_test_51OrtCCKUEJ3Xwud5lQP6Qk9AjtH2Y58XOvhYslqXpCRADWusXh1SpAEJuRBtmQsXX0luezeyaDlOTvHMlcpwzEdG00K01N5w0A'


# @csrf_exempt
# @require_POST
# def create_payment_intent(request):
#     try:
#         data = json.loads(request.body)
#
#         amount = calculate_order_amount(data['items'])
#
#         intent = stripe.PaymentIntent.create(
#             amount=amount,
#             currency='cad',
#             automatic_payment_methods={
#                 'enabled': True,
#             },
#         )
#         return JsonResponse({'clientSecret': intent.client_secret})
#     except Exception as e:
#         return JsonResponse({'error': str(e)}, status=403)
#
#
# def calculate_order_amount(items):
#     # Replace this constant with a calculation of the order's amount
#     return 0

def create_payment_link(price_in_cents):
    try:
        product = stripe.Product.create(
            name="Event name",
            description="Event or Ticket Description"
        )

        price = stripe.Price.create(
            product=product.id,
            unit_amount=price_in_cents,
            currency='cad'
        )

        payment_link = stripe.PaymentLink.create(
            line_items=[{'price': price.id, 'quantity': 1}],
            payment_method_types=['card'],
            allow_promotion_codes=True
        )

        return payment_link.url
    except Exception as e:
        return str(e)