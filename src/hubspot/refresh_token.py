import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id = "13249845-7202-492f-88ff-3ad4753019f6"
client_secret = "556105d1-adb3-4059-b501-a9f594b5ed8f"
refresh_token = os.getenv("REFRESH_TOKEN")

url = "https://api.hubapi.com/oauth/v1/token"
headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}
data = {
    "grant_type": "refresh_token",
    "client_id": client_id,
    "client_secret": client_secret,
    "refresh_token": refresh_token
}

response = requests.post(url, headers=headers, data=data)
tokens = response.json()


print(f"Response JSON: {tokens}")


access_token = tokens.get("access_token")
new_refresh_token = tokens.get("refresh_token")

if access_token and new_refresh_token:
    print(f"Access Token: {access_token}")
    print(f"Refresh Token: {new_refresh_token}")
    
    with open('.env', 'w') as f:
        f.write(f"ACCESS_TOKEN={access_token}\n")
        f.write(f"REFRESH_TOKEN={new_refresh_token}\n")
        f.write(f"HUBSPOT_URL=https://api.hubapi.com\n")
        f.write(f"PORT=8000\n")
        f.write(f"DEBUG=True\n")
else:
    print("Error: No se pudo obtener el nuevo token de acceso. Verifica la respuesta de la API.")