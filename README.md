# HubSpot API App

Este proyecto es una aplicación en Python que interactúa con la API de HubSpot utilizando una aplicación privada. A continuación se detallan los componentes y cómo utilizar la aplicación.

## Estructura del Proyecto

```
hubspot-api-app
├── src
│   ├── main.py          # Punto de entrada de la aplicación
│   ├── hubspot
│   │   ├── __init__.py  # Inicialización del paquete hubspot
│   │   ├── client.py    # Cliente para interactuar con la API de HubSpot
│   │   └── utils.py     # Funciones auxiliares
├── requirements.txt     # Dependencias del proyecto
├── .env                 # Variables de entorno
└── README.md            # Documentación del proyecto
```

## Instalación

1. Clona el repositorio:
   ```
   git clone <URL_DEL_REPOSITORIO>
   cd hubspot-api-app
   ```

2. Crea un entorno virtual (opcional pero recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```

3. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Configuración

Crea un archivo `.env` en la raíz del proyecto y agrega tus variables de entorno necesarias, como la clave de API de HubSpot:

```
HUBSPOT_API_KEY=tu_clave_api
```

## Uso

Para ejecutar la aplicación, utiliza el siguiente comando:

```
python src/main.py
```

Asegúrate de que el archivo `.env` esté configurado correctamente antes de ejecutar la aplicación.

## Contribuciones

Las contribuciones son bienvenidas. Si deseas mejorar este proyecto, por favor abre un issue o un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT.#   a p i H u b s p o t  
 