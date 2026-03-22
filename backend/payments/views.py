import requests, base64, datetime, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Generate OAuth Token
def get_token():
    consumer_key = settings.MPESA_CONSUMER_KEY.strip()
    consumer_secret = settings.MPESA_CONSUMER_SECRET.strip()

    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    print("TOKEN STATUS:", response.status_code)
    print("TOKEN BODY:", response.text)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to get token: {response.status_code} {response.text}")


# STK Push
@csrf_exempt
def stkpush(request):
    try:
        data = json.loads(request.body)
        phone = data['phone']
        amount = int(data['amount'])

        token = get_token()
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

        # Use official sandbox passkey
        PASSKEY = settings.PASSKEY.strip()

        password_str = f"{settings.BUSINESS_SHORTCODE}{PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        payload = {
            "BusinessShortCode": settings.BUSINESS_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": settings.BUSINESS_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.CALLBACK_URL,
            "AccountReference": "Kelvin Service",
            "TransactionDesc": "Payment"
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            headers=headers,
            json=payload
        )

        print("STK STATUS:", response.status_code)
        print("STK BODY:", response.text)

        if response.status_code == 200:
            return JsonResponse({"message": "STK Push sent. Check your phone 📱"})
        else:
            return JsonResponse({"error": response.json()}, status=500)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# Callback
@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body.decode("utf-8"))
    print("CALLBACK DATA:", data)

    return JsonResponse({
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    })