from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from hubspot.client import HubSpotClient
import os
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()


origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_external_contacts():
    url = "http://192.168.0.58:83/api/contacts"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error al obtener los contactos externos: {response.status_code}, {response.text}")

def map_contact_to_hubspot(contact):
    return {
        "properties": {
            "nro_cta": contact.get("NroCta"),
            "firstname": contact.get("nombre"),
            "address": contact.get("Direcc"),
            "locali": contact.get("Locali"),
            "phone": contact.get("Telefn"),
            "email": contact.get("EMails"),
            "cond_iva": contact.get("condIVA"),
            "cuit": contact.get("NrCUIT"),
            "cond_pago": contact.get("CondPago"),
            "descripcion": contact.get("Descrp"),
            "list_precio": contact.get("ListPrecio"),
            "comodato": contact.get("comodato"),
            "empresa": contact.get("Descripcion")
        }
    }

def send_contacts_to_hubspot(contacts):
    hubspot_client = HubSpotClient()
    for contact in contacts:
        try:
            nrocta = contact.get("NroCta")
            search_result = hubspot_client.search_contact_by_nrocta(nrocta)
            if not search_result.get("results"):
                hubspot_contact = map_contact_to_hubspot(contact)
                hubspot_client.create_contact(hubspot_contact)
            else:
                contact_id = search_result["results"][0]["id"]
                hubspot_contact = map_contact_to_hubspot(contact)
                hubspot_client.update_contact(contact_id, hubspot_contact)
        except Exception as e:
            print(f"Error al procesar el contacto con NroCta {nrocta}: {e}")

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de HubSpot"}

@app.get("/contacts")
def get_contacts():
    try:
        hubspot_client = HubSpotClient()
        contacts = hubspot_client.get_contacts()
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/contacts")
def create_contact(contact_data: dict):
    try:
        hubspot_client = HubSpotClient()
        new_contact = hubspot_client.create_contact(contact_data)
        return new_contact
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/contacts/{contact_id}")
def update_contact(contact_id: int, contact_data: dict):
    try:
        hubspot_client = HubSpotClient()
        updated_contact = hubspot_client.update_contact(contact_id, contact_data)
        return updated_contact
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sync-contacts")
def sync_contacts():
    try:
        external_contacts = get_external_contacts()
        send_contacts_to_hubspot(external_contacts)
        return {"message": "Contactos sincronizados exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))