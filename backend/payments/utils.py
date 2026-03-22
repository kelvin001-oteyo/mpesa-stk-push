import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

def get_access_token(consumer_key, consumer_secret):
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    return response.json()["access_token"]

def generate_password(shortcode, passkey):
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    data = shortcode + passkey + timestamp
    password = base64.b64encode(data.encode()).decode("utf-8")
    return password, timestamp

def initiate_stk_push(phone_number, amount, consumer_key, consumer_secret, shortcode, passkey, callback_url):
    access_token = get_access_token(consumer_key, consumer_secret)
    password, timestamp = generate_password(shortcode, passkey)

    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": callback_url,
        "AccountReference": "Test123",
        "TransactionDesc": "Payment for service",
    }

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
