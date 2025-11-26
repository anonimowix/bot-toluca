import streamlit as st
import google.generativeai as genai

# 1. Configuración de la página (Sobria y discreta)
st.set_page_config(
    page_title="Sistema App2", 
    page_icon=None, 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS PARA LOOK CORPORATIVO ---
# Oculta menús de Streamlit y ajusta fuentes
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

# --- 🔒 BLOQUE DE SEGURIDAD ---
clave_secreta = "T0lu25*" 

st.markdown("### Acceso al Sistema")
password_usuario = st.text_input("Ingrese contraseña de autorización:", type="password")

if password_usuario != clave_secreta:
    st.info("Autenticación requerida para continuar.")
    st.stop() 
# ------------------------------

# --- GESTIÓN API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Error de configuración: Credencial API no encontrada.")
    st.stop()

genai.configure(api_key=api_key)

# --- INTERFAZ PRINCIPAL ---
st.title("Panel de Control - Generador de Texto")
st.success("Credenciales verificadas. Sistema listo.")

st.markdown("Configure los parámetros de salida.")

with st.container():
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        tema = st.selectbox("Parámetro A (Categoría)", 
                           ["General", 
                            "Seguridad y Orden", 
                            "Bacheo y Calles", 
                            "Agua y Servicios", 
                            "Luminarias", 
                            "Futuro y Familia",
                            "Recuperación de Espacios"])
    
    with col2:
        estilo = st.selectbox("Parámetro B (Segmento)", 
                             ["Ciudadano Promedio", 
                              "Joven/Informal", 
                              "Emotivo/Familiar", 
                              "Breve/Directo",
                              "Crítico Constructivo"])

    # Sliders
    longitud = st.select_slider("Longitud de salida", options=["Corta (1 frase)", "Media (2 frases)", "Larga (Párrafo)"])
    cantidad = st.slider("Volumen de generación (Cantidad)", 1, 5, 3)

st.markdown("<br>", unsafe_allow_html=True)

# Botón
if st.button("Ejecutar proceso", type="primary", use_container_width=True):
    with st.spinner("Procesando solicitud..."):
        try:
            model = genai.GenerativeModel('gemini-1.5-flash') 
            
            # --- PROMPT REFORZADO ---
            prompt = f"""
            Actúa como un habitante real de Toluca, Estado de México. 
            Tu tarea es escribir comentarios de Facebook apoyando el 1er Informe de Gobierno de Ricardo Moreno.

            PARAMETROS OBLIGATORIOS:
            - TEMA: {tema}
            - PERSONALIDAD: {estilo}
            
            INSTRUCCIONES DE FORMATO ESTRICTAS:
            1. CANTIDAD: Debes generar EXACTAMENTE {cantidad} opciones diferentes. Ni una más, ni una menos.
            2. LONGITUD: La longitud seleccionada es "{longitud}".
               - Si es "Corta", escribe máximo 10-15 palabras por opción.
               - Si es "Media", escribe entre 20-30 palabras.
               - Si es "Larga", escribe un párrafo reflexivo de al menos 40 palabras.
            
            REGLAS DE ESTILO (REALISMO):
            - No escribas perfecto. Usa minúsculas a veces, omite tildes.
            - Usa localismos suaves ("la neta", "chido").
            - ACTITUD: Genuina, de apoyo.

            SALIDA:
            Dame solo los textos de los comentarios, separados claramente por un guion o doble salto de línea.
            """
            
            response = model.generate_content(prompt)
            
            st.markdown("### Resultados del proceso")
            st.code(response.text, language=None)
            
        except Exception as e:

            st.error(f"Error de ejecución: {e}")

