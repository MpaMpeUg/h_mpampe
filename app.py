import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for,send_from_directory
import uuid
import squareAuth

app = Flask(__name__)
idempotency_key = str(uuid.uuid4())

@app.route('/')
def index():
    return render_template('index.html')

@app.route(methods=['GET'])
def charge():
    amount = int(request.form['amount'])
    email = request.form['email']
    fullName = request.form['fullName']
    phone_number = request.form['phoneNumber']
    txRef = request.form['txRef']
    
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
        response_data = result.json()
        print(result.body)
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


    # return response.json()
    redirect_url = response_data.get('data', {}).get('link', '')  # Get the redirect URL from the response data

    if redirect_url:
        return redirect(redirect_url)
    else:
        return "Payment initiation failed."

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('images', filename)

@app.route('/success')
def success():
    return render_template('success.html')

# if __name__ == '__main__':
#     app.run()
