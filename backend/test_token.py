import requests, base64

consumer_key = "3FTaAZvMQJJcjktRj5cGAGgxWdMSnzNxdlwBzw1frh7YsOkAnTkKzByJGGu1rKr1"
consumer_secret = "DVyKYqAT93MFh7GN4cbNWxP4DDchGymIeFTwpB4YNKqiMnK6"

auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

response = requests.get(url, headers={"Authorization": f"Basic {auth}"})
print(response.status_code, response.text)
