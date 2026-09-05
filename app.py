import hmac
import secrets
import time

import requests
import streamlit as st
from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"
APP_URL = "https://bot-toluca-g6nmujs67kbesdeoen5gcx.streamlit.app"
ACCESS_TTL_SECONDS = 15 * 60

st.set_page_config(
    page_title="Comunicación Pública Toluca",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)


STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

:root {
    --navy-950: #06101f;
    --navy-900: #0a1728;
    --navy-800: #10233a;
    --cyan-400: #47d7e8;
    --blue-500: #4285ff;
    --mint-400: #64e6b1;
    --text-100: #f4f8ff;
    --text-300: #adc0d8;
    --line: rgba(150, 190, 226, 0.17);
    --glass: rgba(11, 28, 48, 0.74);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    color: var(--text-100);
    background:
        radial-gradient(circle at 12% 12%, rgba(66, 133, 255, 0.17), transparent 31rem),
        radial-gradient(circle at 88% 20%, rgba(71, 215, 232, 0.13), transparent 28rem),
        linear-gradient(150deg, var(--navy-950) 0%, #081525 48%, #06111d 100%);
    min-height: 100vh;
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    opacity: 0.32;
    background-image:
        linear-gradient(rgba(128, 180, 220, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(128, 180, 220, 0.035) 1px, transparent 1px);
    background-size: 42px 42px;
    mask-image: linear-gradient(to bottom, black, transparent 82%);
}

#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1120px;
    padding: 2.6rem 1.5rem 5rem;
}

.gsap-hero {
    position: relative;
    overflow: hidden;
    padding: clamp(2rem, 5vw, 4.2rem);
    margin-bottom: 1.25rem;
    border: 1px solid var(--line);
    border-radius: 30px;
    background:
        linear-gradient(135deg, rgba(17, 44, 72, 0.92), rgba(7, 22, 39, 0.82)),
        var(--navy-900);
    box-shadow: 0 30px 80px rgba(0, 0, 0, 0.34), inset 0 1px rgba(255, 255, 255, 0.05);
}

.hero-orb {
    position: absolute;
    border-radius: 999px;
    filter: blur(2px);
    pointer-events: none;
}

.orb-one {
    width: 250px;
    height: 250px;
    top: -120px;
    right: 6%;
    background: radial-gradient(circle, rgba(71, 215, 232, 0.36), transparent 68%);
}

.orb-two {
    width: 310px;
    height: 310px;
    right: -130px;
    bottom: -180px;
    background: radial-gradient(circle, rgba(66, 133, 255, 0.32), transparent 70%);
}

.eyebrow {
    display: inline-flex;
    align-items: center;
    gap: .55rem;
    padding: .52rem .8rem;
    margin-bottom: 1.35rem;
    border: 1px solid rgba(100, 230, 177, 0.24);
    border-radius: 999px;
    color: #a9f3d4;
    background: rgba(100, 230, 177, 0.07);
    font-size: .76rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.eyebrow-dot {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--mint-400);
    box-shadow: 0 0 14px var(--mint-400);
}

.hero-title {
    max-width: 780px;
    margin: 0;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(2.4rem, 6vw, 5.2rem);
    font-weight: 800;
    line-height: .98;
    letter-spacing: -.055em;
    color: var(--text-100);
}

.hero-title span {
    color: transparent;
    background: linear-gradient(90deg, var(--cyan-400), #85b6ff 58%, var(--mint-400));
    background-clip: text;
    -webkit-background-clip: text;
}

.hero-copy {
    max-width: 650px;
    margin: 1.45rem 0 0;
    color: var(--text-300);
    font-size: clamp(1rem, 2vw, 1.14rem);
    line-height: 1.72;
}

.hero-meta {
    display: flex;
    flex-wrap: wrap;
    gap: .7rem;
    margin-top: 1.8rem;
}

.meta-chip {
    padding: .58rem .78rem;
    border: 1px solid var(--line);
    border-radius: 11px;
    color: #c8d7ea;
    background: rgba(255, 255, 255, 0.035);
    font-size: .82rem;
    font-weight: 600;
}

.section-label {
    display: flex;
    align-items: center;
    gap: .65rem;
    margin: 1.7rem 0 .8rem;
    color: #c9d8ea;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
}

.section-label::before {
    content: "";
    width: 28px;
    height: 1px;
    background: linear-gradient(90deg, var(--cyan-400), transparent);
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--line) !important;
    border-radius: 22px !important;
    background: var(--glass) !important;
    box-shadow: 0 18px 54px rgba(0, 0, 0, 0.22), inset 0 1px rgba(255, 255, 255, 0.04);
    backdrop-filter: blur(18px);
}

[data-testid="stWidgetLabel"] p,
[data-testid="stMarkdownContainer"] p,
.stSlider label {
    color: #d9e5f4 !important;
}

[data-baseweb="select"] > div,
.stTextInput input {
    min-height: 50px;
    border-color: var(--line) !important;
    border-radius: 13px !important;
    color: var(--text-100) !important;
    background: rgba(3, 13, 25, 0.56) !important;
}

.stTextInput input:focus {
    border-color: rgba(71, 215, 232, .65) !important;
    box-shadow: 0 0 0 3px rgba(71, 215, 232, .1) !important;
}

.stButton > button,
.stFormSubmitButton > button {
    min-height: 50px;
    border: 1px solid rgba(115, 220, 240, .24);
    border-radius: 14px;
    color: #04111d;
    background: linear-gradient(100deg, var(--cyan-400), #79aaff 56%, var(--mint-400));
    box-shadow: 0 12px 32px rgba(47, 151, 226, .2);
    font-weight: 800;
    transition: transform .2s ease, box-shadow .2s ease, filter .2s ease;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    border-color: rgba(255, 255, 255, .34);
    color: #04111d;
    filter: brightness(1.06);
    transform: translateY(-2px);
    box-shadow: 0 18px 38px rgba(47, 151, 226, .3);
}

.stButton > button:focus:not(:active),
.stFormSubmitButton > button:focus:not(:active) {
    color: #04111d;
    border-color: rgba(255, 255, 255, .34);
}

[data-testid="stAlert"] {
    border: 1px solid var(--line);
    border-radius: 15px;
    background: rgba(11, 28, 48, .8);
}

[data-testid="stCode"] {
    border: 1px solid var(--line);
    border-radius: 18px;
    background: #071422;
    box-shadow: 0 18px 45px rgba(0, 0, 0, .22);
}

hr {
    border-color: var(--line) !important;
}

@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1rem .8rem 3rem;
    }

    .gsap-hero {
        padding: 1.7rem 1.35rem 2rem;
        border-radius: 22px;
    }

    .hero-title {
        font-size: 2.45rem;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        scroll-behavior: auto !important;
        animation-duration: .01ms !important;
        transition-duration: .01ms !important;
    }
}
</style>
"""

MOTION = """
<script src="https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js"></script>
<script>
(() => {
    const runMotion = () => {
        if (!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        gsap.from('.gsap-hero .reveal', {
            y: 28,
            opacity: 0,
            duration: 0.85,
            stagger: 0.11,
            ease: 'power3.out'
        });
        gsap.to('.orb-one', {
            x: 24,
            y: -16,
            duration: 5.2,
            repeat: -1,
            yoyo: true,
            ease: 'sine.inOut'
        });
        gsap.to('.orb-two', {
            x: -20,
            y: 18,
            duration: 6.4,
            repeat: -1,
            yoyo: true,
            ease: 'sine.inOut'
        });
        const cards = gsap.utils.toArray('[data-testid="stVerticalBlockBorderWrapper"]');
        if (cards.length) {
            gsap.from(cards, {
                y: 18,
                opacity: 0,
                duration: 0.7,
                delay: 0.22,
                ease: 'power2.out'
            });
        }
    };
    window.setTimeout(runMotion, 120);
})();
</script>
"""

HERO = """
<section class="gsap-hero">
    <div class="hero-orb orb-one"></div>
    <div class="hero-orb orb-two"></div>
    <div class="eyebrow reveal"><span class="eyebrow-dot"></span>Sistema operativo</div>
    <h1 class="hero-title reveal">Comunicación pública,<br><span>clara y precisa.</span></h1>
    <p class="hero-copy reveal">
        Configura el enfoque, el tono y la extensión. El sistema prepara borradores
        institucionales listos para revisar, ajustar y publicar.
    </p>
    <div class="hero-meta reveal">
        <span class="meta-chip">◇ Toluca, Estado de México</span>
        <span class="meta-chip">◇ Generación asistida</span>
        <span class="meta-chip">◇ Acceso controlado</span>
    </div>
</section>
"""


def secret_value(name, default=""):
    try:
        return str(st.secrets[name]).strip()
    except KeyError:
        return default


def telegram_call(token, method, payload=None):
    response = requests.post(
        f"https://api.telegram.org/bot{token}/{method}",
        json=payload or {},
        timeout=12,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError(data.get("description", "Telegram rechazó la solicitud."))
    return data.get("result")


def check_telegram_decision(bot_token, chat_id, access_token):
    updates = telegram_call(
        bot_token,
        "getUpdates",
        {"timeout": 0, "limit": 100, "allowed_updates": ["callback_query"]},
    )
    for update in reversed(updates):
        callback = update.get("callback_query") or {}
        message = callback.get("message") or {}
        callback_chat = str((message.get("chat") or {}).get("id", ""))
        decision = callback.get("data", "")
        if callback_chat != chat_id or not decision.endswith(f":{access_token}"):
            continue

        telegram_call(
            bot_token,
            "answerCallbackQuery",
            {
                "callback_query_id": callback.get("id"),
                "text": "Decisión registrada",
            },
        )
        return decision.startswith("approve:")
    return None


def render_access_gate():
    bot_token = secret_value("TELEGRAM_BOT_TOKEN")
    chat_id = secret_value("TELEGRAM_CHAT_ID")

    if bot_token and chat_id:
        with st.container(border=True):
            st.html('<div class="section-label">Acceso privado</div>')
            st.subheader("Solicita autorización")
            st.caption(
                "Envía una solicitud al administrador. Cuando la apruebe desde "
                "Telegram, podrás entrar desde esta misma sesión."
            )

            if "access_token" not in st.session_state:
                requester = st.text_input(
                    "Tu nombre o referencia",
                    max_chars=60,
                    placeholder="Ej. Coordinación de Comunicación",
                )
                st.caption(
                    "Este dato se enviará al Telegram privado del administrador "
                    "únicamente para identificar la solicitud."
                )
                if st.button(
                    "Solicitar acceso",
                    type="primary",
                    use_container_width=True,
                ):
                    access_token = secrets.token_urlsafe(16)
                    keyboard = {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "✅ Aprobar",
                                    "callback_data": f"approve:{access_token}",
                                },
                                {
                                    "text": "❌ Denegar",
                                    "callback_data": f"deny:{access_token}",
                                },
                            ]
                        ]
                    }
                    telegram_call(
                        bot_token,
                        "sendMessage",
                        {
                            "chat_id": chat_id,
                            "text": (
                                "🔐 Nueva solicitud de acceso\n\n"
                                f"Referencia: {requester.strip() or 'Sin nombre'}\n"
                                f"Aplicación: {APP_URL}\n\n"
                                "Aprueba o deniega esta sesión:"
                            ),
                            "reply_markup": keyboard,
                        },
                    )
                    st.session_state.access_token = access_token
                    st.session_state.access_requested_at = time.time()
                    st.rerun()
            else:
                elapsed = time.time() - st.session_state.access_requested_at
                if elapsed > ACCESS_TTL_SECONDS:
                    st.warning("La solicitud expiró. Envía una nueva.")
                    if st.button("Crear nueva solicitud", use_container_width=True):
                        del st.session_state.access_token
                        del st.session_state.access_requested_at
                        st.rerun()
                else:
                    st.info("Solicitud enviada. Esperando la decisión del administrador.")
                    if st.button(
                        "Comprobar autorización",
                        type="primary",
                        use_container_width=True,
                    ):
                        decision = check_telegram_decision(
                            bot_token,
                            chat_id,
                            st.session_state.access_token,
                        )
                        if decision is True:
                            st.session_state.authorized = True
                            st.rerun()
                        if decision is False:
                            st.error("La solicitud fue denegada.")
                        if decision is None:
                            st.toast("La solicitud sigue pendiente.")
        st.stop()

    # Respaldo temporal hasta completar la configuración de Telegram.
    fallback_password = secret_value("APP_PASSWORD")
    with st.container(border=True):
        st.html('<div class="section-label">Acceso privado</div>')
        st.subheader("Acceso temporal")
        st.caption("La aprobación móvil está pendiente de configuración.")
        entered_password = st.text_input("Contraseña", type="password")
        if not (
            fallback_password
            and hmac.compare_digest(entered_password, fallback_password)
        ):
            st.stop()


st.markdown(STYLES, unsafe_allow_html=True)
st.html(MOTION, unsafe_allow_javascript=True)
st.html(HERO)

if not st.session_state.get("authorized", False):
    render_access_gate()

api_key = secret_value("GROQ_API_KEY")
if not api_key:
    st.error("Falta configurar GROQ_API_KEY en los secretos de Streamlit.")
    st.stop()

client = Groq(api_key=api_key)

st.html('<div class="section-label">Configuración</div>')
with st.container(border=True):
    st.subheader("Define el mensaje")
    st.caption("Selecciona los parámetros. La generación conserva las reglas actuales.")

    col1, col2 = st.columns(2)
    with col1:
        tema = st.selectbox(
            "Categoría",
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
            "Tono",
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
    cantidad = st.slider("Cantidad de opciones", 1, 5, 3)

    generate = st.button(
        "Generar borradores",
        type="primary",
        use_container_width=True,
    )

if generate:
    with st.spinner("Preparando borradores..."):
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

            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": prompt}],
            )

            resultado = response.choices[0].message.content
            if not resultado:
                raise RuntimeError("Groq no devolvió texto en esta solicitud.")

            st.html('<div class="section-label">Resultado</div>')
            with st.container(border=True):
                st.subheader("Borradores generados")
                st.code(resultado, language=None)
        except Exception as error:
            st.error(f"Error de ejecución: {error}")
