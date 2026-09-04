# Generador Toluca

Aplicación de Streamlit para crear borradores de comunicación pública con la API de Gemini.

## Configuración en Streamlit Community Cloud

La aplicación se publica desde:

- Repositorio: `anonimowix/bot-toluca`
- Rama: `main`
- Archivo principal: `app.py`

En **Settings > Secrets** de la aplicación agrega:

```toml
APP_PASSWORD = "una-contrasena-nueva"
GEMINI_API_KEY = "tu-clave-de-gemini"
```

Nunca subas las credenciales reales al repositorio. Al guardar cambios en la rama `main`, Streamlit Community Cloud vuelve a publicar la aplicación automáticamente.

## Ejecución local

1. Copia `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml`.
2. Completa las dos credenciales.
3. Instala `requirements.txt`.
4. Ejecuta `streamlit run app.py`.
