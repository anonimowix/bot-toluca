import streamlit as st
from groq import Groq

# 1. Configuración de la página
st.set_page_config(
    page_title="Sistema App2", 
    page_icon=None, 
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- ESTILOS CSS ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stApp { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
            h1 { color: #2c3e50 !important; font-size: 1.8rem !important; }
            .stButton>button { background-color: #2980b9; color: white; border: none; }
            .stButton>button:hover { background-color: #3498db; }
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

# --- GESTIÓN API KEY (GROQ) ---
try:
    # Ahora buscamos la clave GROQ_API_KEY
    api_key = st.secrets["GROQ_API_KEY"]
except:
    st.error("Error: Credencial API no configurada.")
    st.stop()

client = Groq(api_key=api_key)

# --- INTERFAZ PRINCIPAL ---
st.title("Panel de Control - Generador de Texto")
st.success("Credenciales verificadas. Sistema Llama-3 Activo.")
st.markdown("Configure los parámetros de salida.")

with st.container():
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        tema = st.selectbox("Parámetro A (Categoría)", 
                           ["General", "Seguridad y Orden", "Bacheo y Calles", 
                            "Agua y Servicios", "Luminarias", "Futuro y Familia", "Recuperación de Espacios"])
    with col2:
        estilo = st.selectbox("Parámetro B (Segmento)", 
                             ["Ciudadano Promedio", "Joven/Informal", "Emotivo/Familiar", 
                              "Breve/Directo", "Crítico Constructivo"])

    longitud = st.select_slider("Longitud de salida", options=["Corta (1 frase)", "Media (2 frases)", "Larga (Párrafo)"])
    cantidad = st.slider("Volumen de generación", 1, 5, 3)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Ejecutar proceso", type="primary", use_container_width=True):
    with st.spinner("Procesando solicitud..."):
        try:
            prompt = f"""
            Actúa como un habitante real de Toluca, Estado de México. 
            Escribe comentarios de Facebook apoyando el 1er Informe de Gobierno de Ricardo Moreno.

            PARAMETROS:
            - TEMA: {tema}
            - PERSONALIDAD: {estilo}
            
            INSTRUCCIONES:
            1. Genera EXACTAMENTE {cantidad} opciones.
            2. LONGITUD: {longitud}.
            3. REALISMO SUCIO: Usa minúsculas, falta de acentos, 'q' por 'que'.
            4. LOCALISMOS: "la neta", "chido", "vientos".
            
            SALIDA:
            Dame solo los textos de los comentarios separados por un guion.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "user", "content": prompt}
                ],
               model="llama-3.1-8b-instant", # Modelo muy rápido y eficiente
            )
            
            st.markdown("### Resultados del proceso")
            st.code(chat_completion.choices[0].message.content, language=None)
            
        except Exception as e:
            st.error(f"Error de ejecución: {e}")

