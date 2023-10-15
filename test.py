import squareAuth
import uuid

idempotency_key = str(uuid.uuid4())
result = squareAuth.client.checkout.create_payment_link(
    body = {
        "idempotency_key": idempotency_key,
        "quick_pay": {
        "name": 'fullName',
        "price_money": {
            "amount": 150,
            "currency": "USD"
        },
        "location_id": "LJGHD7PBGN574"
        },
        "pre_populated_data": {}
    }
    )

if result.is_success():
    response_data = result.body
    # print(result.body)
elif result.is_error():
    print(result.errors)
        
# Assuming 'response' contains the JSON response you provided
payment_link = response_data.get('payment_link', {})

# Extract the payment URL
payment_url = payment_link.get('url')

if payment_url:
    print(f'Payment URL for redirection: {payment_url}')
else:
    print('Payment URL not found in the response.')