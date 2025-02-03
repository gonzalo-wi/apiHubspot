import os
import requests
from dotenv import load_dotenv

class HubSpotClient:
    def __init__(self):
        load_dotenv()
        self.access_token = os.getenv("ACCESS_TOKEN")
        self.refresh_token = os.getenv("REFRESH_TOKEN")
        self.base_url = os.getenv("HUBSPOT_URL")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        if not self.access_token:
            raise ValueError("ACCESS_TOKEN no está configurada")
        if not self.refresh_token:
            raise ValueError("REFRESH_TOKEN no está configurada")
        if not self.base_url:
            raise ValueError("HUBSPOT_URL no está configurada")
        if not self.client_id:
            raise ValueError("CLIENT_ID no está configurada")
        if not self.client_secret:
            raise ValueError("CLIENT_SECRET no está configurada")
        print(f"ACCESS_TOKEN: {self.access_token}")
        print(f"HUBSPOT_URL: {self.base_url}")

    def refresh_access_token(self):
        url = "https://api.hubapi.com/oauth/v1/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }
        response = requests.post(url, headers=headers, data=data)
        tokens = response.json()
        if response.status_code == 200:
            self.access_token = tokens.get("access_token")
            self.refresh_token = tokens.get("refresh_token")
            with open('.env', 'w') as f:
                f.write(f"ACCESS_TOKEN={self.access_token}\n")
                f.write(f"REFRESH_TOKEN={self.refresh_token}\n")
                f.write(f"HUBSPOT_URL={self.base_url}\n")
                f.write(f"CLIENT_ID={self.client_id}\n")
                f.write(f"CLIENT_SECRET={self.client_secret}\n")
            print(f"Nuevo ACCESS_TOKEN: {self.access_token}")
            print(f"Nuevo REFRESH_TOKEN: {self.refresh_token}")
        else:
            raise Exception(f"Error al refrescar el token de acceso: {response.status_code}, {response.text}")

    def get_contacts(self):
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            print(f"Request URL: {url}")
            print(f"Request Headers: {headers}")
            response = requests.get(url, headers=headers)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                self.refresh_access_token()
                return self.get_contacts()
            else:
                raise Exception(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error al obtener contactos: {str(e)}")

    def create_contact(self, contact_data):
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            response = requests.post(url, headers=headers, json=contact_data)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 401:
                self.refresh_access_token()
                return self.create_contact(contact_data)
            else:
                raise Exception(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error al crear contacto: {str(e)}")

    def update_contact(self, contact_id, contact_data):
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/{contact_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            response = requests.patch(url, headers=headers, json=contact_data)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                self.refresh_access_token()
                return self.update_contact(contact_id, contact_data)
            else:
                raise Exception(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error al actualizar contacto: {str(e)}")

    def search_contact_by_nrocta(self, nrocta):
        try:
            url = f"{self.base_url}/crm/v3/objects/contacts/search"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/json"
            }
            data = {
                "filterGroups": [{
                    "filters": [{
                        "propertyName": "nro_cta",
                        "operator": "EQ",
                        "value": nrocta
                    }]
                }]
            }
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                self.refresh_access_token()
                return self.search_contact_by_nrocta(nrocta)
            else:
                raise Exception(f"Error: {response.status_code}, {response.text}")
        except Exception as e:
            raise Exception(f"Error al buscar contacto por NroCta: {str(e)}")