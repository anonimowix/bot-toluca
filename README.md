# Generador Toluca

Aplicación de Streamlit para crear borradores de comunicación pública con la API de Groq.

## Configuración en Streamlit Community Cloud

La aplicación se publica desde:

- Repositorio: `anonimowix/bot-toluca`
- Rama: `main`
- Archivo principal: `app.py`

En **Settings > Secrets** de la aplicación agrega:

```toml
APP_PASSWORD = "una-contrasena-nueva"
GROQ_API_KEY = "tu-clave-de-groq"
TELEGRAM_BOT_TOKEN = "token-entregado-por-botfather"
TELEGRAM_CHAT_ID = "id-numerico-del-administrador"
```

Nunca subas las credenciales reales al repositorio. Al guardar cambios en la rama `main`, Streamlit Community Cloud vuelve a publicar la aplicación automáticamente.

Si `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` están configurados, la aplicación sustituye la contraseña por solicitudes de acceso aprobadas o rechazadas mediante botones privados de Telegram. Mientras falte esa configuración, `APP_PASSWORD` funciona como respaldo temporal.

## Ejecución local

1. Copia `.streamlit/secrets.toml.example` como `.streamlit/secrets.toml`.
2. Completa las dos credenciales.
3. Instala `requirements.txt`.
4. Ejecuta `streamlit run app.py`.
