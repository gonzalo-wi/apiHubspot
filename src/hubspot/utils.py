def load_env_variables():
    """Carga las variables de entorno desde el archivo .env."""
    from dotenv import load_dotenv
    import os

    load_dotenv()

    hubspot_api_key = os.getenv("HUBSPOT_API_KEY")
    if not hubspot_api_key:
        raise ValueError("La variable de entorno HUBSPOT_API_KEY no está configurada.")

    return {
        "HUBSPOT_API_KEY": hubspot_api_key,
    }