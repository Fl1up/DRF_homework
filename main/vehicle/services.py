import stripe
from django.shortcuts import render


def payment(request):
    if request.method == 'POST':
        stripe.api_key = 'sk_test_51NexkmDyPJ4N4cRkA0ddCgzqu35kFSAYhrDChFbJKTWYYdmjFSXhWxNSExsSCAehSPhywRgXDD3EmB8Ib7D5Fc4m0074WtOdLC:'
        token = request.POST.get('stripeToken')
        amount = request.POST.get('amount')

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                description='Payment for course'
            )
            # Здесь можно добавить логику обработки успешного платежа
            return render(request, 'success.html')
        except stripe.error.CardError as e:
            # Обработка ошибки оплаты
            pass
    return render(request, 'payment.html')