import hashlib
import hmac
import secrets
import time
from datetime import datetime, timedelta

import extra_streamlit_components as stx
import requests
import streamlit as st
from groq import Groq


MODEL_NAME = "openai/gpt-oss-20b"
APP_URL = "https://bot-toluca-g6nmujs67kbesdeoen5gcx.streamlit.app"
ACCESS_TTL_SECONDS = 15 * 60
COOKIE_TTL_SECONDS = 24 * 60 * 60
ACCESS_COOKIE_NAME = "comuniquy_access_v1"

st.set_page_config(
    page_title="Comuniquy",
    page_icon="●",
    layout="wide",
    initial_sidebar_state="collapsed",
)


STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --paper: #f2f0e8;
    --sheet: #fbfaf5;
    --ink: #11110f;
    --muted: #68675f;
    --line: #c9c6bb;
    --acid: #c8ff45;
    --signal: #ff4a31;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}

.stApp {
    min-height: 100vh;
    color: var(--ink);
    background: var(--paper);
}

.stApp::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    opacity: .2;
    background-image: linear-gradient(90deg, transparent calc(100% - 1px), #8e8b80 1px);
    background-size: 8.333vw 100%;
}

#MainMenu, footer, [data-testid="stHeader"] {
    visibility: hidden;
}

[data-testid="stMainBlockContainer"] {
    position: relative;
    z-index: 1;
    max-width: 1180px;
    padding: 1.2rem 1.6rem 5rem;
}

.kinetic-hero {
    position: relative;
    overflow: hidden;
    margin-bottom: 2.8rem;
    color: var(--ink);
    border-top: 1px solid var(--ink);
    border-bottom: 1px solid var(--ink);
}

.brand-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    min-height: 64px;
    border-bottom: 1px solid var(--ink);
    font-family: 'DM Mono', monospace;
    font-size: .72rem;
    font-weight: 500;
    letter-spacing: .09em;
    text-transform: uppercase;
}

.brand-lockup,
.edition-mark {
    display: flex;
    align-items: center;
    gap: .7rem;
}

.brand-dot {
    width: 11px;
    height: 11px;
    border: 1px solid var(--ink);
    border-radius: 50%;
    background: var(--acid);
}

.hero-grid {
    display: grid;
    grid-template-columns: minmax(0, 1fr) 250px;
    gap: 2.5rem;
    padding: clamp(2rem, 5vw, 4.6rem) 0 3rem;
}

.title-mask {
    overflow: hidden;
    padding-bottom: .08em;
}

.kinetic-title {
    margin: 0;
    color: var(--ink);
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(3.35rem, 8.8vw, 7.8rem);
    font-weight: 700;
    line-height: .82;
    letter-spacing: -.075em;
    text-transform: uppercase;
}

.kinetic-title .outline {
    color: transparent;
    -webkit-text-stroke: 1.7px var(--ink);
}

.hero-side {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 100%;
    padding-top: .5rem;
}

.orbit-mark {
    position: relative;
    width: 152px;
    height: 152px;
    margin-left: auto;
    border: 1px solid var(--ink);
    border-radius: 50%;
}

.orbit-mark::before,
.orbit-mark::after {
    content: "";
    position: absolute;
    background: var(--ink);
}

.orbit-mark::before {
    top: 50%;
    left: -20px;
    width: 190px;
    height: 1px;
}

.orbit-mark::after {
    top: -20px;
    left: 50%;
    width: 1px;
    height: 190px;
}

.orbit-core {
    position: absolute;
    inset: 37px;
    display: grid;
    place-items: center;
    border-radius: 50%;
    color: var(--ink);
    background: var(--acid);
    font-size: 1.7rem;
}

.hero-copy {
    max-width: 230px;
    margin: 2rem 0 0;
    color: var(--muted);
    font-size: .98rem;
    line-height: 1.55;
}

.ticker {
    overflow: hidden;
    border-top: 1px solid var(--ink);
}

.ticker-track {
    display: flex;
    width: max-content;
    padding: .8rem 0;
    white-space: nowrap;
    will-change: transform;
}

.ticker-track span {
    display: inline-flex;
    align-items: center;
    gap: 1.2rem;
    padding-right: 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: .72rem;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.ticker-track i {
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--signal);
}

.workspace-header {
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    align-items: end;
    gap: 2rem;
    margin-bottom: 1.2rem;
    padding: 1rem 0 1.35rem;
    border-top: 1px solid var(--ink);
    border-bottom: 1px solid var(--ink);
    opacity: 1 !important;
    transform: none !important;
}

.workspace-brand {
    display: flex;
    align-items: center;
    gap: .7rem;
    margin-bottom: 1.35rem;
    font-family: 'DM Mono', monospace;
    font-size: .7rem;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.workspace-header h1 {
    margin: 0;
    color: var(--ink);
    font-size: clamp(2.5rem, 5.5vw, 5rem);
    font-weight: 700;
    line-height: .9;
    letter-spacing: -.065em;
}

.workspace-header h1 span {
    color: transparent;
    -webkit-text-stroke: 1.3px var(--ink);
}

.workspace-status {
    display: inline-flex;
    align-items: center;
    gap: .55rem;
    padding: .65rem .8rem;
    border: 1px solid var(--ink);
    font-family: 'DM Mono', monospace;
    font-size: .68rem;
    letter-spacing: .06em;
    text-transform: uppercase;
}

.workspace-status::before {
    content: "";
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: var(--acid);
    box-shadow: 0 0 0 1px var(--ink);
}

.section-kicker {
    display: grid;
    grid-template-columns: 52px auto 1fr;
    align-items: center;
    gap: .8rem;
    margin: 2rem 0 .85rem;
    color: var(--ink);
    font-family: 'DM Mono', monospace;
    font-size: .72rem;
    font-weight: 500;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.section-kicker::before {
    content: attr(data-index);
    display: grid;
    place-items: center;
    width: 32px;
    height: 32px;
    border: 1px solid var(--ink);
    border-radius: 50%;
}

.section-kicker::after {
    content: "";
    height: 1px;
    background: var(--line);
    transform-origin: left;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    background: rgba(251, 250, 245, .92) !important;
    box-shadow: 9px 9px 0 var(--ink);
}

[data-testid="stVerticalBlockBorderWrapper"] > div {
    padding: clamp(1.2rem, 3vw, 2rem) !important;
}

h1, h2, h3, h4, p, label,
[data-testid="stMarkdownContainer"] {
    color: var(--ink);
}

h3 {
    font-size: clamp(1.55rem, 3vw, 2.25rem) !important;
    letter-spacing: -.045em !important;
}

[data-testid="stCaptionContainer"] p {
    color: var(--muted) !important;
}

[data-testid="stWidgetLabel"] p,
.stSlider label p {
    color: var(--ink) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: .72rem !important;
    font-weight: 500 !important;
    letter-spacing: .04em !important;
    text-transform: uppercase;
}

.stSelectbox [data-baseweb="select"] > div,
[data-baseweb="select"] > div,
.stTextInput input {
    min-height: 52px;
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    color: var(--ink) !important;
    background: var(--sheet) !important;
    box-shadow: none !important;
}

.stSelectbox [data-baseweb="select"] *,
[data-baseweb="select"] * {
    color: var(--ink) !important;
}

.stTextInput input:focus,
[data-baseweb="select"] > div:focus-within {
    outline: 3px solid var(--acid) !important;
    outline-offset: 0;
}

[data-baseweb="popover"],
[role="listbox"],
[data-baseweb="menu"] {
    color: var(--ink) !important;
    background: var(--sheet) !important;
}

[role="listbox"] {
    border: 1px solid var(--ink) !important;
}

[role="option"],
[role="option"] *,
[data-baseweb="menu"] li,
[data-baseweb="menu"] li * {
    color: var(--ink) !important;
}

[role="option"],
[data-baseweb="menu"] li {
    background: var(--sheet) !important;
}

[role="option"]:hover,
[role="option"][aria-selected="true"],
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] li[aria-selected="true"] {
    color: var(--ink) !important;
    background: var(--acid) !important;
}

[role="option"]:hover *,
[role="option"][aria-selected="true"] *,
[data-baseweb="menu"] li:hover *,
[data-baseweb="menu"] li[aria-selected="true"] * {
    color: var(--ink) !important;
}

[data-testid="stSegmentedControl"] [role="radiogroup"] {
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    background: var(--sheet) !important;
}

[data-testid="stSegmentedControl"] button {
    border-color: var(--line) !important;
    border-radius: 0 !important;
    color: var(--ink) !important;
    background: var(--sheet) !important;
    box-shadow: none !important;
}

[data-testid="stSegmentedControl"] button[aria-pressed="true"],
[data-testid="stSegmentedControl"] button[data-active="true"] {
    border-color: var(--signal) !important;
    background: var(--acid) !important;
}

[data-testid="stSegmentedControl"] button,
[data-testid="stSegmentedControl"] button p {
    color: var(--ink) !important;
}

.stButton > button,
.stFormSubmitButton > button {
    min-height: 52px;
    border: 1px solid var(--ink);
    border-radius: 0;
    color: var(--ink) !important;
    background: var(--acid) !important;
    box-shadow: none;
    font-family: 'DM Mono', monospace;
    font-size: .78rem;
    font-weight: 500;
    letter-spacing: .06em;
    text-transform: uppercase;
    transition: color .18s ease, background .18s ease, transform .18s ease;
}

.stButton > button p,
.stFormSubmitButton > button p {
    color: var(--ink) !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    border-color: var(--ink);
    color: var(--ink);
    background: var(--signal) !important;
    transform: translate(-3px, -3px);
    box-shadow: 3px 3px 0 var(--ink);
}

.stButton > button:hover p,
.stFormSubmitButton > button:hover p,
.stButton > button:active p,
.stFormSubmitButton > button:active p {
    color: var(--ink) !important;
}

.stButton > button:active,
.stFormSubmitButton > button:active {
    border-color: var(--ink);
    color: var(--ink);
    background: var(--signal) !important;
}

.stButton > button:focus:not(:active),
.stFormSubmitButton > button:focus:not(:active) {
    border-color: var(--ink);
    color: var(--ink) !important;
    background: var(--acid) !important;
}

.stButton > button:focus:not(:active) p,
.stFormSubmitButton > button:focus:not(:active) p {
    color: var(--ink) !important;
}

.stSlider [role="slider"] {
    border-color: var(--ink) !important;
    background: var(--acid) !important;
}

[data-testid="stAlert"] {
    border: 1px solid var(--ink);
    border-radius: 0;
    color: var(--ink);
    background: var(--sheet);
}

[data-testid="stCode"] {
    border: 1px solid var(--ink) !important;
    border-radius: 0 !important;
    color: var(--ink) !important;
    background: var(--sheet) !important;
    box-shadow: 7px 7px 0 var(--acid);
}

[data-testid="stCode"] pre,
[data-testid="stCode"] code,
[data-testid="stCode"] span {
    color: var(--ink) !important;
    background: transparent !important;
}

[data-testid="stCode"] pre,
[data-testid="stCode"] code {
    white-space: pre-wrap !important;
    overflow-wrap: anywhere !important;
    line-height: 1.6 !important;
}

.waiting-shell {
    display: grid;
    grid-template-columns: 110px 1fr;
    align-items: center;
    gap: 1.6rem;
    min-height: 150px;
}

.wait-orbit {
    position: relative;
    width: 94px;
    height: 94px;
    border: 1px solid var(--ink);
    border-radius: 50%;
}

.wait-orbit::before {
    content: "";
    position: absolute;
    inset: 16px;
    border: 1px dashed var(--ink);
    border-radius: 50%;
}

.wait-dot {
    position: absolute;
    top: -5px;
    left: 50%;
    width: 11px;
    height: 11px;
    border: 1px solid var(--ink);
    border-radius: 50%;
    background: var(--acid);
    transform: translateX(-50%);
}

.waiting-copy small {
    font-family: 'DM Mono', monospace;
    font-size: .68rem;
    letter-spacing: .08em;
    text-transform: uppercase;
}

.waiting-copy h4 {
    margin: .35rem 0 .5rem;
    font-size: clamp(1.4rem, 3vw, 2rem);
    letter-spacing: -.045em;
}

.waiting-copy p {
    max-width: 470px;
    margin: 0;
    color: var(--muted);
    line-height: 1.55;
}

@media (max-width: 760px) {
    [data-testid="stMainBlockContainer"] {
        padding: .55rem .7rem 2.5rem;
    }

    .stApp::before {
        background-size: 52px 100%;
    }

    .kinetic-hero {
        margin-bottom: .8rem;
    }

    .brand-row {
        min-height: 46px;
        font-size: .6rem;
        letter-spacing: .055em;
    }

    .hero-grid {
        display: block;
        padding: 1.25rem 0 1.15rem;
    }

    .kinetic-title {
        font-size: clamp(2.8rem, 13.5vw, 3.45rem);
        line-height: .84;
        letter-spacing: -.07em;
    }

    .hero-side {
        display: none;
    }

    .ticker {
        display: none;
    }

    .section-kicker {
        grid-template-columns: 40px auto 1fr;
        gap: .55rem;
        margin: .85rem 0 .5rem;
        font-size: .64rem;
    }

    .section-kicker::before {
        width: 29px;
        height: 29px;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        box-shadow: 4px 4px 0 var(--ink);
    }

    [data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: .95rem !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: .7rem !important;
    }

    [data-testid="stHorizontalBlock"] {
        gap: .65rem !important;
    }

    h3 {
        font-size: 1.5rem !important;
    }

    [data-baseweb="select"] > div,
    .stTextInput input {
        min-height: 46px;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        min-height: 48px;
    }

    .waiting-shell {
        grid-template-columns: 58px 1fr;
        gap: .9rem;
        min-height: 108px;
    }

    .workspace-header {
        grid-template-columns: 1fr;
        gap: .65rem;
        margin-bottom: .45rem;
        padding: .65rem 0 .8rem;
    }

    .workspace-brand {
        margin-bottom: .65rem;
        font-size: .6rem;
    }

    .workspace-header h1 {
        font-size: clamp(2.3rem, 11vw, 3.1rem);
    }

    .workspace-status {
        justify-self: start;
        padding: .48rem .62rem;
        font-size: .6rem;
    }

    .wait-orbit {
        width: 54px;
        height: 54px;
    }

    .wait-orbit::before {
        inset: 9px;
    }

    .waiting-copy h4 {
        margin: .25rem 0 .35rem;
        font-size: 1.25rem;
    }

    .waiting-copy p {
        font-size: .83rem;
        line-height: 1.4;
    }
}

@media (max-width: 390px) {
    .edition-mark {
        max-width: 112px;
        text-align: right;
        line-height: 1.25;
    }

    .kinetic-title {
        font-size: 12.9vw;
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
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
    const start = () => {
        if (!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

        if (document.querySelector('.kinetic-hero')) {
            const tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
            tl.from('.brand-row', { scaleX: 0, transformOrigin: 'left', duration: .65 })
              .from('.title-mask > span', { yPercent: 112, duration: .9, stagger: .09 }, '-=.2')
              .from('.hero-side', { x: 30, opacity: 0, duration: .65 }, '-=.55')
              .from('.ticker', { scaleX: 0, transformOrigin: 'left', duration: .55 }, '-=.35');

            gsap.to('.orbit-mark', {
                rotation: 360,
                duration: 18,
                repeat: -1,
                ease: 'none'
            });

            gsap.to('.ticker-track', {
                xPercent: -50,
                duration: 16,
                repeat: -1,
                ease: 'none'
            });
        }

        const sectionLines = gsap.utils.toArray('.section-kicker');
        if (sectionLines.length) {
            gsap.from(sectionLines, { y: 12, opacity: 0, duration: .5, stagger: .08 });
        }
    };

    window.setTimeout(start, 100);
})();
</script>
"""

HERO = """
<section class="kinetic-hero">
    <div class="brand-row">
        <div class="brand-lockup"><span class="brand-dot"></span>Comuniquy</div>
        <div class="edition-mark">Mensajes con intención</div>
    </div>
    <div class="hero-grid">
        <h1 class="kinetic-title">
            <div class="title-mask"><span>Las palabras</span></div>
            <div class="title-mask"><span class="outline">también</span></div>
            <div class="title-mask"><span>construyen.</span></div>
        </h1>
        <aside class="hero-side">
            <div class="orbit-mark"><span class="orbit-core">↗</span></div>
            <p class="hero-copy">Define el enfoque y convierte una idea en propuestas claras, directas y listas para revisar.</p>
        </aside>
    </div>
    <div class="ticker">
        <div class="ticker-track">
            <span>Claro <i></i> Directo <i></i> Humano <i></i> Preciso <i></i></span>
            <span>Claro <i></i> Directo <i></i> Humano <i></i> Preciso <i></i></span>
        </div>
    </div>
</section>
"""

WORKSPACE_HEADER = """
<header class="workspace-header">
    <div>
        <div class="workspace-brand"><span class="brand-dot"></span>Comuniquy / Toluca</div>
        <h1>Crea un mensaje<span>.</span></h1>
    </div>
    <div class="workspace-status">Sesión activa</div>
</header>
"""

WAITING = """
<div class="waiting-shell">
    <div class="wait-orbit"><span class="wait-dot"></span></div>
    <div class="waiting-copy">
        <small>Solicitud enviada</small>
        <h4>Esperando autorización</h4>
        <p>No cierres esta ventana. El acceso se abrirá automáticamente cuando sea autorizado.</p>
    </div>
</div>
<script>
(() => {
    if (!window.gsap || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    gsap.to('.wait-orbit', { rotation: 360, duration: 1.8, repeat: -1, ease: 'none' });
    gsap.from('.waiting-copy > *', { y: 12, opacity: 0, duration: .5, stagger: .08, ease: 'power3.out' });
})();
</script>
"""


def secret_value(name, default=""):
    try:
        return str(st.secrets[name]).strip()
    except KeyError:
        return default


def create_access_cookie(signing_secret):
    expires_at = int(time.time()) + COOKIE_TTL_SECONDS
    nonce = secrets.token_urlsafe(12)
    payload = f"{expires_at}.{nonce}"
    signature = hmac.new(
        signing_secret.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return f"{payload}.{signature}"


def valid_access_cookie(cookie_value, signing_secret):
    if not cookie_value or not signing_secret:
        return False

    try:
        expires_at, nonce, supplied_signature = cookie_value.split(".", 2)
        payload = f"{expires_at}.{nonce}"
        expected_signature = hmac.new(
            signing_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return (
            int(expires_at) > int(time.time())
            and hmac.compare_digest(supplied_signature, expected_signature)
        )
    except (AttributeError, TypeError, ValueError):
        return False


def telegram_call(token, method, payload=None):
    response = requests.post(
        f"https://api.telegram.org/bot{token}/{method}",
        json=payload or {},
        timeout=12,
    )
    response.raise_for_status()
    data = response.json()
    if not data.get("ok"):
        raise RuntimeError("No fue posible completar la solicitud.")
    return data.get("result")


def check_access_decision(bot_token, chat_id, access_token):
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
            {"callback_query_id": callback.get("id"), "text": "Decisión registrada"},
        )
        return decision.startswith("approve:")
    return None


def clear_access_request():
    st.session_state.pop("access_token", None)
    st.session_state.pop("access_requested_at", None)


@st.fragment(run_every="2s", key="access_waiter")
def render_waiting_state(bot_token, chat_id):
    requested_at = st.session_state.get("access_requested_at", 0)
    if time.time() - requested_at > ACCESS_TTL_SECONDS:
        clear_access_request()
        st.session_state.access_notice = "expired"
        st.rerun(scope="app")

    st.html(WAITING, unsafe_allow_javascript=True)

    try:
        decision = check_access_decision(
            bot_token,
            chat_id,
            st.session_state.access_token,
        )
    except (requests.RequestException, RuntimeError):
        return

    if decision is True:
        st.session_state.authorized = True
        st.session_state.persist_access_cookie = True
        clear_access_request()
        st.rerun(scope="app")

    if decision is False:
        clear_access_request()
        st.session_state.access_notice = "denied"
        st.rerun(scope="app")


def render_access_gate():
    bot_token = secret_value("TELEGRAM_BOT_TOKEN")
    chat_id = secret_value("TELEGRAM_CHAT_ID")

    st.html('<div class="section-kicker" data-index="00">Acceso</div>')
    with st.container(border=True):
        if not bot_token or not chat_id:
            st.subheader("Acceso no disponible")
            st.caption("Intenta nuevamente dentro de unos minutos.")
            st.stop()

        if "access_token" in st.session_state:
            render_waiting_state(bot_token, chat_id)
            st.stop()

        notice = st.session_state.pop("access_notice", None)
        if notice == "denied":
            st.error("La solicitud no fue autorizada. Puedes enviar una nueva.")
        if notice == "expired":
            st.warning("La solicitud expiró. Envía una nueva para continuar.")

        st.subheader("Solicita entrada")
        st.caption(
            "Identifícate y envía tu solicitud. Esta pantalla se actualizará "
            "automáticamente cuando sea autorizada."
        )
        requester = st.text_input(
            "Nombre o referencia",
            max_chars=60,
            placeholder="Ej. Coordinación de Comunicación",
        )

        if st.button("Solicitar acceso", type="primary", use_container_width=True):
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
            try:
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
            except (requests.RequestException, RuntimeError):
                st.error("No pudimos enviar la solicitud. Intenta nuevamente.")
                st.stop()

            st.session_state.access_token = access_token
            st.session_state.access_requested_at = time.time()
            st.rerun()

    st.stop()


st.markdown(STYLES, unsafe_allow_html=True)

cookie_manager = stx.CookieManager(key="comuniquy_cookie_manager")
cookie_signing_secret = secret_value("TELEGRAM_BOT_TOKEN")
stored_access_cookie = cookie_manager.get(ACCESS_COOKIE_NAME)

if valid_access_cookie(stored_access_cookie, cookie_signing_secret):
    st.session_state.authorized = True

if st.session_state.pop("persist_access_cookie", False):
    cookie_manager.set(
        ACCESS_COOKIE_NAME,
        create_access_cookie(cookie_signing_secret),
        key="save_comuniquy_access",
        path="/",
        expires_at=datetime.now() + timedelta(days=1),
        max_age=COOKIE_TTL_SECONDS,
        secure=True,
        same_site="strict",
    )

if not st.session_state.get("authorized", False):
    st.html(HERO)
    st.html(MOTION, unsafe_allow_javascript=True)
    render_access_gate()

st.html(WORKSPACE_HEADER)
st.html(MOTION, unsafe_allow_javascript=True)

api_key = secret_value("GROQ_API_KEY")
if not api_key:
    st.error("El servicio no está disponible en este momento.")
    st.stop()

client = Groq(api_key=api_key)

st.html('<div class="section-kicker" data-index="01">Configuración</div>')
with st.container(border=True):
    st.subheader("Configura la propuesta")
    st.caption("Todo lo necesario está aquí. Ajusta y crea.")

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

    col3, col4 = st.columns([1.35, 1])
    with col3:
        longitud_corta = st.segmented_control(
            "Longitud",
            options=["Corta", "Media", "Larga"],
            default="Media",
            required=True,
            width="stretch",
        )

    with col4:
        cantidad = st.segmented_control(
            "Cantidad de opciones",
            options=[1, 2, 3, 4, 5],
            default=3,
            required=True,
            width="stretch",
        )

    longitud = {
        "Corta": "Corta (1 frase)",
        "Media": "Media (2 frases)",
        "Larga": "Larga (Párrafo)",
    }[longitud_corta]

    generate = st.button(
        "Crear propuestas",
        type="primary",
        use_container_width=True,
    )

if generate:
    with st.spinner("Preparando propuestas..."):
        try:
            prompt = f"""
            Actúa como redactor de opinion ciudadana del municipio de Toluca,
            Estado de México. Escribe comentario de publicaciones relacionadas a la administracion de Toluca actual

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
            - Presenta cada texto como una
              opinión espontánea de un ciudadano, dependiendo de la opcion que se elija
            - Simula testimonios.
            - Siempre muestra apoyo a la administración municipal de toluca y a Ricardo Moreno 
            - Mantén un tono claro y respetuoso.

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
                raise RuntimeError("No se recibió contenido en esta solicitud.")

            st.html('<div class="section-kicker" data-index="02">Propuestas</div>')
            with st.container(border=True):
                st.subheader("Listas para ajustar")
                st.code(resultado, language=None)
        except Exception:
            st.error("No pudimos crear las propuestas. Intenta nuevamente.")
