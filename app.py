import hmac

import streamlit as st
from google import genai


MODEL_NAME = "gemini-3.5-flash-lite"

st.set_page_config(
    page_title="Comunicación Pública Toluca",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed",
)

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.stApp {
    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
}
h1 {
    font-weight: 600 !important;
    color: #2c3e50 !important;
    font-size: 1.8rem !important;
}
.stButton>button {
    background-color: #2980b9;
    color: white;
    border-radius: 4px;
    border: none;
    font-weight: 500;
}
.stButton>button:hover {
    background-color: #3498db;
}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Las credenciales se configuran en los Secrets de Streamlit Cloud.
try:
    clave_secreta = str(st.secrets["APP_PASSWORD"])
    api_key = str(st.secrets["GEMINI_API_KEY"])
except KeyError as error:
    st.error(
        f"Falta configurar el secreto '{error.args[0]}' en Streamlit Cloud."
    )
    st.stop()

st.markdown("### Acceso al Sistema")
password_usuario = st.text_input(
    "Ingrese contraseña de autorización:",
    type="password",
)

if not hmac.compare_digest(password_usuario, clave_secreta):
    st.info("Autenticación requerida para continuar.")
    st.stop()

client = genai.Client(api_key=api_key)

st.title("Panel de Comunicación Pública")
st.success("Credenciales verificadas. Sistema listo.")
st.markdown("Configure los parámetros de salida.")

with st.container():
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        tema = st.selectbox(
            "Parámetro A (Categoría)",
            [
                "General",
                "Seguridad y Orden",
                "Bacheo y Calles",
                "Agua y Servicios",
                "Luminarias",
                "Futuro y Familia",
                "Recuperación de Espacios",
            ],
        )

    with col2:
        estilo = st.selectbox(
            "Parámetro B (Tono)",
            [
                "Institucional y claro",
                "Joven e informativo",
                "Cercano y familiar",
                "Breve y directo",
                "Crítico constructivo",
            ],
        )

    longitud = st.select_slider(
        "Longitud de salida",
        options=[
            "Corta (1 frase)",
            "Media (2 frases)",
            "Larga (Párrafo)",
        ],
    )
    cantidad = st.slider(
        "Volumen de generación (Cantidad)",
        1,
        5,
        3,
    )

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Ejecutar proceso", type="primary", use_container_width=True):
    with st.spinner("Procesando solicitud..."):
        try:
            prompt = f"""
            Actúa como redactor de comunicación pública del municipio de Toluca,
            Estado de México. Escribe borradores informativos para una publicación
            institucional relacionada con el 1er Informe de Gobierno.

            PARÁMETROS OBLIGATORIOS:
            - TEMA: {tema}
            - TONO: {estilo}

            INSTRUCCIONES DE FORMATO:
            1. Genera exactamente {cantidad} opciones diferentes.
            2. La longitud seleccionada es "{longitud}".
               - Corta: máximo 10-15 palabras por opción.
               - Media: entre 20-30 palabras por opción.
               - Larga: un párrafo de al menos 40 palabras por opción.

            REGLAS DE CONTENIDO:
            - Presenta cada texto como comunicación institucional, no como una
              opinión espontánea de un ciudadano.
            - No inventes cifras, obras, resultados ni testimonios.
            - No suplantes personas ni simules apoyo ciudadano orgánico.
            - Mantén un tono claro, verificable y respetuoso.

            SALIDA:
            Devuelve solo los borradores, separados por un guion o doble salto
            de línea.
            """

            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError("Gemini no devolvió texto en esta solicitud.")

            st.markdown("### Resultados del proceso")
            st.code(response.text, language=None)
        except Exception as error:
            st.error(f"Error de ejecución: {error}")
