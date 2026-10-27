import os
import sys
import streamlit as st
import urllib.request
import urllib.parse
import json
import hmac
import hashlib
import time
import datetime

# ==============================================================================
# CONFIGURACIÓN Y SEGURIDAD BORA DESIGN ADMIN WEB 2030
# ==============================================================================
FIREBASE_URL = os.environ.get("BORA_FIREBASE_URL", "https://bora-design-nestpro-default-rtdb.firebaseio.com")
SECRETO_MAESTRO_BORA = b"BoraDesign_Angelo_SecretKey_2026_Pro_V3_Monthly"
EPOCA_BASE_DIAS = 19723
PRESETS_ETIQUETAS = ["Poseidon", "Ocampo", "Heidy lee Sport"]
CLAVE_ADMINISTRADOR = os.environ.get("BORA_ADMIN_PASSWORD", "Bora2026Admin*")
MAX_INTENTOS_LOGIN = 5
SEGUNDOS_BLOQUEO_LOGIN = 60

# Branding Oficial Bora Design en Base64
LOGO_BORA_BASE64 = (
    "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"
    "AAElFTkSuQmCC"
)

st.set_page_config(
    page_title="Bora Design — Cloud Command Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CSS 2030: OBSIDIAN VISIONOS & MOBILE-FIRST ULTRA RESPONSIVE
# ==============================================================================
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }}

    .stApp {{
        background: radial-gradient(circle at 50% 0%, #0F172A 0%, #070A10 60%, #030712 100%) !important;
        color: #F8FAFC !important;
    }}

    /* Header y contenedores */
    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1280px !important;
    }}

    /* Header Navbar 2030 */
    .bora-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 14px 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
    }}

    .bora-brand-box {{
        display: flex;
        align-items: center;
        gap: 16px;
    }}

    .bora-brand-title {{
        font-size: 1.15rem;
        font-weight: 800;
        letter-spacing: -0.02em;
        color: #FFFFFF;
        margin: 0;
        line-height: 1.2;
    }}

    .bora-brand-sub {{
        font-size: 0.75rem;
        font-weight: 600;
        color: #94A3B8;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        margin: 0;
    }}

    .bora-badge-online {{
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 6px 12px;
        border-radius: 20px;
        letter-spacing: 0.02em;
    }}

    .pulse-dot {{
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 10px #10B981;
        animation: pulse 2s infinite;
    }}

    @keyframes pulse {{
        0% {{ transform: scale(0.95); opacity: 0.8; }}
        50% {{ transform: scale(1.25); opacity: 1; }}
        100% {{ transform: scale(0.95); opacity: 0.8; }}
    }}

    /* Bento KPI Cards */
    .bento-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-bottom: 22px;
    }}

    .bento-card {{
        background: rgba(17, 24, 39, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }}

    .bento-card:hover {{
        transform: translateY(-2px);
        border-color: rgba(255, 255, 255, 0.18);
    }}

    .bento-card::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
    }}

    .bento-cyan::before {{ background: #38BDF8; }}
    .bento-emerald::before {{ background: #10B981; }}
    .bento-crimson::before {{ background: #E11D48; }}
    .bento-amber::before {{ background: #F59E0B; }}

    .bento-title {{
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 6px;
    }}

    .bento-value {{
        font-size: 1.85rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1;
        margin-bottom: 4px;
    }}

    .bento-sub {{
        font-size: 0.72rem;
        font-weight: 500;
        color: #64748B;
    }}

    /* Mobile Equipment Card */
    .mobile-eq-card {{
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.09);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
        position: relative;
    }}

    .mobile-eq-card.bloqueado {{
        border-left: 4px solid #E11D48;
    }}
    .mobile-eq-card.activa {{
        border-left: 4px solid #10B981;
    }}
    .mobile-eq-card.vencida {{
        border-left: 4px solid #F59E0B;
    }}

    .eq-header-row {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
    }}

    .eq-client-name {{
        font-size: 1.1rem;
        font-weight: 800;
        color: #FFFFFF;
    }}

    .tag-pill {{
        display: inline-block;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}

    .tag-taller {{
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }}

    .tag-online {{
        background: rgba(16, 185, 129, 0.15);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }}

    .tag-offline {{
        background: rgba(100, 116, 139, 0.15);
        color: #94A3B8;
        border: 1px solid rgba(100, 116, 139, 0.3);
    }}

    .code-box {{
        font-family: 'JetBrains Mono', Consolas, monospace;
        font-size: 0.85rem;
        font-weight: 700;
        background: #090D16;
        border: 1px solid #1E293B;
        border-radius: 8px;
        padding: 6px 10px;
        color: #38BDF8;
        letter-spacing: 0.04em;
        margin: 6px 0;
        word-break: break-all;
    }}

    .code-key {{
        color: #34D399 !important;
        background: #061811 !important;
        border-color: #059669 !important;
    }}

    /* Botones Táctiles Móviles */
    .stButton>button {{
        background: linear-gradient(180deg, #F43F5E 0%, #E11D48 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        border-radius: 10px !important;
        border: 1px solid #FB7185 !important;
        padding: 8px 14px !important;
        min-height: 42px !important;
        transition: all 0.16s ease !important;
        box-shadow: 0 4px 12px rgba(225, 29, 72, 0.25) !important;
    }}

    .stButton>button:hover {{
        background: linear-gradient(180deg, #FB7185 0%, #E11D48 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(225, 29, 72, 0.4) !important;
    }}

    .stButton>button:active {{
        transform: translateY(1px) !important;
    }}

    /* Inputs y Selects */
    div[data-baseweb="input"], div[data-baseweb="select"] {{
        background-color: #090D16 !important;
        border-color: #1E293B !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
    }}

    /* Estilos específicos para pantallas de móvil */
    @media (max-width: 768px) {{
        .bento-grid {{
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}
        .bora-header {{
            flex-direction: column;
            align-items: flex-start;
            gap: 12px;
            padding: 12px 14px;
        }}
        .block-container {{
            padding-left: 0.8rem !important;
            padding-right: 0.8rem !important;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# LOGIN ULTRA RESISTENTE A FUERZA BRUTA (HMAC + THROTTLING)
# ------------------------------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "intentos_fallidos" not in st.session_state:
    st.session_state.intentos_fallidos = 0
if "bloqueado_hasta" not in st.session_state:
    st.session_state.bloqueado_hasta = 0.0

if not st.session_state.autenticado:
    _, col_login, _ = st.columns([1, 2, 1])
    with col_login:
        st.markdown(f"""
            <div style="text-align: center; margin-top: 40px; margin-bottom: 24px;">
                <img src="data:image/png;base64,{LOGO_BORA_BASE64}" style="height: 48px; filter: drop-shadow(0 0 16px rgba(225,29,72,0.4));" />
                <h2 style="margin-top: 14px; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">CLOUD CONTROL CENTER</h2>
                <p style="color: #94A3B8; font-size: 0.85rem; font-weight: 600;">Panel de Administración Web y Móvil • 2030 Edition</p>
            </div>
        """, unsafe_allow_html=True)

        ahora_login = time.time()
        if ahora_login < st.session_state.bloqueado_hasta:
            restante = int(st.session_state.bloqueado_hasta - ahora_login)
            st.error(f"Demasiados intentos fallidos. Acceso bloqueado por seguridad ({restante}s restantes).")
            st.stop()

        pwd = st.text_input("Contraseña de Acceso Administrador", type="password", placeholder="Ingresa tu clave maestra")
        if st.button("INGRESAR AL PANEL DE CONTROL", use_container_width=True):
            if hmac.compare_digest(pwd.encode("utf-8"), CLAVE_ADMINISTRADOR.encode("utf-8")):
                st.session_state.autenticado = True
                st.session_state.intentos_fallidos = 0
                st.rerun()
            else:
                st.session_state.intentos_fallidos += 1
                if st.session_state.intentos_fallidos >= MAX_INTENTOS_LOGIN:
                    st.session_state.bloqueado_hasta = time.time() + SEGUNDOS_BLOQUEO_LOGIN
                    st.session_state.intentos_fallidos = 0
                    st.error(f"Demasiados intentos erróneos. Bloqueado temporalmente por {SEGUNDOS_BLOQUEO_LOGIN} segundos.")
                else:
                    rest = MAX_INTENTOS_LOGIN - st.session_state.intentos_fallidos
                    st.error(f"Contraseña incorrecta. {rest} intento(s) restante(s).")
    st.stop()

# ------------------------------------------------------------------------------
# FUNCIONES NATIVAS DE LICENCIAMIENTO BORA & FIREBASE RTDB
# ------------------------------------------------------------------------------
def generar_clave_firmada(hwid_cliente, dias_vigencia=30):
    """Genera la clave firmada con HMAC-SHA256 idéntica al Keygen y Desktop."""
    hwid_limpio = hwid_cliente.strip().upper()
    dia_actual_utc = int(time.time() // 86400)
    dia_vencimiento = dia_actual_utc + int(dias_vigencia)
    offset_dias = max(1, min(65535, dia_vencimiento - EPOCA_BASE_DIAS))
    hex_vencimiento = f"{offset_dias:04X}"
    hex_salt = f"{int(time.time() * 10) & 0xFFFF:04X}"

    mensaje = f"{hwid_limpio}|{hex_vencimiento}|{hex_salt}".encode("utf-8")
    firma = hmac.new(SECRETO_MAESTRO_BORA, mensaje, hashlib.sha256).hexdigest().upper()
    return f"{hex_vencimiento}-{hex_salt}-{firma[0:4]}-{firma[4:8]}", dia_vencimiento


def extraer_dia_vencimiento_de_clave(clave_str):
    try:
        partes = str(clave_str).strip().upper().split("-")
        if len(partes) == 4 and len(partes[0]) == 4:
            return EPOCA_BASE_DIAS + int(partes[0], 16)
    except Exception:
        pass
    return 0


def peticion_firebase(metodo, ruta, datos=None):
    url = f"{FIREBASE_URL.rstrip('/')}/{ruta}.json"
    body = json.dumps(datos).encode("utf-8") if datos is not None else None
    req = urllib.request.Request(url, data=body, method=metodo, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=7) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else None


def redactar_mensaje_whatsapp(destinatario, dias_rest, pc_nom, hwid):
    saludo = f"¡Hola, {destinatario}!" if destinatario else "¡Hola!"
    estado = f"vence en *{dias_rest} día(s)*" if dias_rest > 0 else "se encuentra actualmente *VENCIDA*"
    equipo_info = f" ({pc_nom})" if pc_nom else f" ({hwid})"
    texto = (
        f"{saludo}\n\n"
        f"Te recordamos que tu licencia de *Bora Design NestPro*{equipo_info} {estado}.\n\n"
        f"Si deseas renovar tu suscripción mensual para seguir optimizando tela y anidando sin interrupciones, "
        f"por favor indícanos para reactivar tu equipo de inmediato.\n\n"
        f"¡Muchas gracias por confiar en Bora Design!"
    )
    return texto

# ------------------------------------------------------------------------------
# DESCARGA DE DATOS EN TIEMPO REAL DESDE FIREBASE
# ------------------------------------------------------------------------------
try:
    raw_equipos = peticion_firebase("GET", "equipos") or {}
    equipos_data = raw_equipos if isinstance(raw_equipos, dict) else {}
    sync_ok = True
except Exception as e:
    equipos_data = {}
    sync_ok = False

ahora_ts = int(time.time())
dia_hoy = int(ahora_ts // 86400)
hora_actual_str = time.strftime("%H:%M:%S")

# Métricas Bento Globales
total_pcs = len(equipos_data)
online_pcs = sum(
    1 for v in equipos_data.values()
    if isinstance(v, dict) and int(v.get("ultimo_ping", 0)) > 0 and (ahora_ts - int(v.get("ultimo_ping", 0))) <= 75
)
activas_pcs = sum(
    1 for v in equipos_data.values()
    if isinstance(v, dict) and not v.get("bloqueado", False) and int(v.get("dia_vencimiento", 0)) > dia_hoy
)
atencion_pcs = sum(
    1 for v in equipos_data.values()
    if isinstance(v, dict) and (
        v.get("bloqueado", False)
        or int(v.get("dia_vencimiento", 0)) <= dia_hoy
        or (0 < int(v.get("dia_vencimiento", 0)) - dia_hoy <= 5)
    )
)

# ------------------------------------------------------------------------------
# HEADER PRINCIPAL
# ------------------------------------------------------------------------------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(f"""
        <div class="bora-header">
            <div class="bora-brand-box">
                <img src="data:image/png;base64,{LOGO_BORA_BASE64}" style="height: 36px; filter: drop-shadow(0 0 10px rgba(225,29,72,0.3));" />
                <div>
                    <h1 class="bora-brand-title">CLOUD COMMAND CENTER</h1>
                    <p class="bora-brand-sub">Panel de Control de Licencias Bora Design • 2030</p>
                </div>
            </div>
            <div class="bora-badge-online">
                <span class="pulse-dot"></span>
                <span>FIREBASE RTDB ({hora_actual_str}) • {total_pcs} PC(s)</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_h2:
    col_btn_ref, col_btn_out = st.columns(2)
    with col_btn_ref:
        if st.button("🔄 Refrescar", use_container_width=True):
            st.rerun()
    with col_btn_out:
        if st.button("🚪 Salir", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

# ------------------------------------------------------------------------------
# BENTO KPI CARDS (4 TILES DE ALTO IMPACTO)
# ------------------------------------------------------------------------------
st.markdown(f"""
    <div class="bento-grid">
        <div class="bento-card bento-cyan">
            <div class="bento-title">Total Equipos</div>
            <div class="bento-value">{total_pcs}</div>
            <div class="bento-sub">Registrados en la Nube</div>
        </div>
        <div class="bento-card bento-emerald">
            <div class="bento-title">En Línea Ahora</div>
            <div class="bento-value" style="color: #34D399;">{online_pcs}</div>
            <div class="bento-sub">Ping activo (&le; 75s)</div>
        </div>
        <div class="bento-card bento-crimson">
            <div class="bento-title">Licencias Activas</div>
            <div class="bento-value" style="color: #FB7185;">{activas_pcs}</div>
            <div class="bento-sub">Suscripción Vigente</div>
        </div>
        <div class="bento-card bento-amber">
            <div class="bento-title">Atención / Pausadas</div>
            <div class="bento-value" style="color: #FBBF24;">{atencion_pcs}</div>
            <div class="bento-sub">&le; 5 días o bloqueadas</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES DEL PANEL
# ------------------------------------------------------------------------------
tab_tarjetas, tab_tabla, tab_nuevo, tab_ota = st.tabs([
    "📱 Tarjetas de Equipos (Móvil)",
    "📊 Vista Tabla Completa",
    "➕ Activar Nuevo Equipo",
    "🚀 Publicar Actualización OTA"
])

# Recopilar todos los talleres para filtros
todos_talleres = sorted(list({
    str(v.get("taller", "")).strip() for v in equipos_data.values()
    if isinstance(v, dict) and str(v.get("taller", "")).strip() and str(v.get("taller", "")).strip() != "Sin asignar"
} | set(PRESETS_ETIQUETAS)))

# ==============================================================================
# TAB 1: TARJETAS RESPONSIVAS PARA TELÉFONO Y ESCRITORIO
# ==============================================================================
with tab_tarjetas:
    # Barra de Búsqueda y Filtros Rápidos
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        busqueda_txt = st.text_input("🔍 Búsqueda rápida", placeholder="Buscar por HWID, Taller, Operador, PC...", label_visibility="collapsed").strip().lower()
    with col_f2:
        filtro_estado = st.selectbox(
            "Filtrar Estado",
            ["Todos", "🟢 En Línea", "⚠️ Por Vencer (≤5d)", "🚫 Bloqueadas / Vencidas"],
            label_visibility="collapsed"
        )
    with col_f3:
        filtro_taller = st.selectbox(
            "Filtrar Taller",
            ["Todos los Talleres"] + todos_talleres + ["Sin asignar"],
            label_visibility="collapsed"
        )

    # Filtrar equipos según criterios
    equipos_filtrados = {}
    for hwid, info in sorted(equipos_data.items()):
        if not isinstance(info, dict):
            continue

        taller = str(info.get("taller", "")).strip() or "Sin asignar"
        cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
        pc = str(info.get("pc_nombre", "")).strip()
        bloqueado = bool(info.get("bloqueado", False))
        dia_venc = int(info.get("dia_vencimiento", 0))
        ultimo_ts = int(info.get("ultimo_ping", 0))

        en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
        dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0

        # Filtro de búsqueda texto
        if busqueda_txt:
            corpus = f"{hwid} {taller} {cliente} {pc}".lower()
            if busqueda_txt not in corpus:
                continue

        # Filtro de estado
        if filtro_estado == "🟢 En Línea" and not en_linea:
            continue
        elif filtro_estado == "⚠️ Por Vencer (≤5d)" and not (not bloqueado and 0 < dias_rest <= 5):
            continue
        elif filtro_estado == "🚫 Bloqueadas / Vencidas" and not (bloqueado or dias_rest == 0):
            continue

        # Filtro de taller
        if filtro_taller != "Todos los Talleres":
            if filtro_taller == "Sin asignar" and taller != "Sin asignar":
                continue
            elif filtro_taller != "Sin asignar" and taller.lower() != filtro_taller.lower():
                continue

        equipos_filtrados[hwid] = info

    if not equipos_filtrados:
        st.info("No se encontraron equipos que coincidan con los filtros seleccionados.")
    else:
        st.caption(f"Mostrando **{len(equipos_filtrados)}** de **{total_pcs}** equipos registrados.")

        # Renderizar cada equipo como una tarjeta táctil para móvil
        for hwid, info in equipos_filtrados.items():
            taller = str(info.get("taller", "")).strip() or "Sin asignar"
            cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
            pc = info.get("pc_nombre", "PC Desconocida")
            usuario_win = info.get("usuario_pc", "")
            bloqueado = bool(info.get("bloqueado", False))
            dia_venc = int(info.get("dia_vencimiento", 0))
            clave_act = info.get("clave", "---") or "---"
            ultimo_ts = int(info.get("ultimo_ping", 0))

            en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
            dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0

            # Clases y textos de estado
            if bloqueado:
                card_cls = "bloqueado"
                badge_lic = "<span class='tag-pill' style='background: rgba(225,29,72,0.2); color: #FDA4AF; border: 1px solid #E11D48;'>🚫 BLOQUEADO</span>"
                dias_badge = f"<span style='color: #FDA4AF; font-weight: 700;'>Pausado ({dias_rest}d restantes)</span>"
            elif dias_rest > 0:
                card_cls = "activa"
                col_b = "#34D399" if dias_rest > 5 else "#FBBF24"
                badge_lic = f"<span class='tag-pill' style='background: rgba(16,185,129,0.15); color: {col_b}; border: 1px solid {col_b};'>✔ ACTIVA</span>"
                dias_badge = f"<span style='color: {col_b}; font-weight: 700;'>{dias_rest} día(s) de vigencia</span>"
            else:
                card_cls = "vencida"
                badge_lic = "<span class='tag-pill' style='background: rgba(245,158,11,0.2); color: #FBBF24; border: 1px solid #F59E0B;'>⏳ VENCIDA</span>"
                dias_badge = "<span style='color: #FBBF24; font-weight: 700;'>0 días (Requiere renovación)</span>"

            badge_con = "<span class='tag-pill tag-online'>🟢 EN LÍNEA</span>" if en_linea else "<span class='tag-pill tag-offline'>⚫ DESCONECTADO</span>"
            badge_taller = f"<span class='tag-pill tag-taller'>🏷️ {taller}</span>"

            destinatario_nombre = cliente if cliente != "Sin asignar" else taller

            # Render de tarjeta HTML
            st.markdown(f"""
                <div class="mobile-eq-card {card_cls}">
                    <div class="eq-header-row">
                        <div>
                            {badge_taller}
                            <span class="eq-client-name" style="margin-left: 8px;">{cliente}</span>
                        </div>
                        <div>
                            {badge_con}
                            {badge_lic}
                        </div>
                    </div>
                    <div style="font-size: 0.8rem; color: #94A3B8; margin-bottom: 4px;">
                        🖥️ <b>{pc}</b> {f'• Win: <code>{usuario_win}</code>' if usuario_win else ''} • {dias_badge}
                    </div>
                    <div class="code-box">ID: {hwid}</div>
                    <div class="code-box code-key">CLAVE: {clave_act}</div>
                </div>
            """, unsafe_allow_html=True)

            # Barra de Acciones Móviles Directas
            col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns([1.2, 1, 1.4, 1.2, 0.8])

            with col_a1:
                if st.button("⚡ +30 Días", key=f"btn_30_{hwid}", use_container_width=True):
                    dia_base = max(dia_hoy, dia_venc)
                    total_nuevos = (dia_base - dia_hoy) + 30
                    nueva_cl, nuevo_venc = generar_clave_firmada(hwid, total_nuevos)
                    peticion_firebase("PATCH", f"equipos/{hwid}", {
                        "clave": nueva_cl, "dia_vencimiento": nuevo_venc, "bloqueado": False, "clave_bloqueada": ""
                    })
                    st.success(f"¡+30 días aplicados a {cliente}! Clave: {nueva_cl}")
                    st.rerun()

            with col_a2:
                if st.button("+15d", key=f"btn_15_{hwid}", use_container_width=True):
                    dia_base = max(dia_hoy, dia_venc)
                    total_nuevos = (dia_base - dia_hoy) + 15
                    nueva_cl, nuevo_venc = generar_clave_firmada(hwid, total_nuevos)
                    peticion_firebase("PATCH", f"equipos/{hwid}", {
                        "clave": nueva_cl, "dia_vencimiento": nuevo_venc, "bloqueado": False, "clave_bloqueada": ""
                    })
                    st.success(f"¡+15 días aplicados! Clave: {nueva_cl}")
                    st.rerun()

            with col_a3:
                # Generador de WhatsApp
                msg_wsp = redactar_mensaje_whatsapp(destinatario_nombre, dias_rest, pc, hwid)
                msg_encoded = urllib.parse.quote(msg_wsp)
                link_wsp = f"https://api.whatsapp.com/send?text={msg_encoded}"
                st.markdown(f"""
                    <a href="{link_wsp}" target="_blank" style="text-decoration: none;">
                        <button style="width: 100%; min-height: 42px; background: #064E3B; color: #34D399; font-weight: 700; border: 1px solid #059669; border-radius: 10px; cursor: pointer;">
                            💬 WhatsApp Cobro
                        </button>
                    </a>
                """, unsafe_allow_html=True)

            with col_a4:
                if bloqueado:
                    if st.button("🔓 Desbloquear", key=f"btn_unblk_{hwid}", use_container_width=True):
                        venc_rest = dia_venc
                        if venc_rest <= dia_hoy and clave_act and clave_act != "---":
                            venc_rest = extraer_dia_vencimiento_de_clave(clave_act)
                        if venc_rest <= dia_hoy:
                            nueva_cl, nuevo_venc = generar_clave_firmada(hwid, 30)
                            peticion_firebase("PATCH", f"equipos/{hwid}", {
                                "bloqueado": False, "clave_bloqueada": "", "clave": nueva_cl, "dia_vencimiento": nuevo_venc
                            })
                        else:
                            peticion_firebase("PATCH", f"equipos/{hwid}", {
                                "bloqueado": False, "clave_bloqueada": "", "dia_vencimiento": venc_rest
                            })
                        st.success(f"¡{cliente} desbloqueado!")
                        st.rerun()
                else:
                    if st.button("🚫 Bloquear", key=f"btn_blk_{hwid}", use_container_width=True):
                        peticion_firebase("PATCH", f"equipos/{hwid}", {"bloqueado": True, "clave_bloqueada": clave_act})
                        st.warning(f"¡{cliente} bloqueado en vivo!")
                        st.rerun()

            with col_a5:
                with st.popover("⚙️"):
                    st.write(f"**Gestión Avanzada:** `{hwid}`")
                    st.write("**Presets de Taller (1 Clic):**")
                    col_p1, col_p2, col_p3 = st.columns(3)
                    with col_p1:
                        if st.button("Poseidon", key=f"pos_{hwid}"):
                            peticion_firebase("PATCH", f"equipos/{hwid}", {"taller": "Poseidon"})
                            st.rerun()
                    with col_p2:
                        if st.button("Ocampo", key=f"oc_{hwid}"):
                            peticion_firebase("PATCH", f"equipos/{hwid}", {"taller": "Ocampo"})
                            st.rerun()
                    with col_p3:
                        if st.button("Heidy lee", key=f"hls_{hwid}"):
                            peticion_firebase("PATCH", f"equipos/{hwid}", {"taller": "Heidy lee Sport"})
                            st.rerun()

                    ed_tal = st.text_input("Taller:", value="" if taller == "Sin asignar" else taller, key=f"t_{hwid}")
                    ed_cli = st.text_input("Operador:", value="" if cliente == "Sin asignar" else cliente, key=f"c_{hwid}")
                    if st.button("Guardar Datos", key=f"sv_{hwid}"):
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "taller": ed_tal.strip() or "Sin asignar",
                            "cliente": ed_cli.strip() or "Sin asignar"
                        })
                        st.success("Guardado")
                        st.rerun()

                    st.divider()
                    dias_fijos = st.number_input("Días Exactos:", min_value=1, max_value=365, value=30, key=f"df_{hwid}")
                    if st.button("Aplicar Días Fijos", key=f"bdf_{hwid}"):
                        cl_f, v_f = generar_clave_firmada(hwid, dias_fijos)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": cl_f, "dia_vencimiento": v_f, "bloqueado": False, "clave_bloqueada": ""
                        })
                        st.success("Aplicado")
                        st.rerun()

                    st.divider()
                    if st.button("🗑️ Eliminar Equipo", key=f"del_{hwid}"):
                        peticion_firebase("DELETE", f"equipos/{hwid}")
                        st.rerun()

            st.write("")

# ==============================================================================
# TAB 2: VISTA TABLA COMPLETA (ESTILO DESKTOP / EXCEL)
# ==============================================================================
with tab_tabla:
    st.markdown("#### Registro Global de Equipos en Formato Tabla")
    filas_tabla = []
    for hwid, info in sorted(equipos_data.items()):
        if not isinstance(info, dict):
            continue
        taller = str(info.get("taller", "")).strip() or "Sin asignar"
        cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
        pc = info.get("pc_nombre", "Desconocido")
        bloqueado = bool(info.get("bloqueado", False))
        dia_venc = int(info.get("dia_vencimiento", 0))
        clave_act = info.get("clave", "---") or "---"
        ultimo_ts = int(info.get("ultimo_ping", 0))

        en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
        dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0
        ult_ping_str = datetime.datetime.fromtimestamp(ultimo_ts).strftime("%d/%m %H:%M") if ultimo_ts > 0 else "Nunca"

        if bloqueado:
            estado_str = "🚫 BLOQUEADO"
        elif dias_rest > 0:
            estado_str = f"✔ ACTIVA ({dias_rest}d)"
        else:
            estado_str = "⏳ VENCIDA"

        filas_tabla.append({
            "HWID": hwid,
            "Taller": taller,
            "Usuario": cliente,
            "PC": pc,
            "Conexión": "🟢 En Línea" if en_linea else "⚫ Desconectado",
            "Estado": estado_str,
            "Días": dias_rest,
            "Último Ping": ult_ping_str,
            "Clave Firmada": clave_act
        })

    if filas_tabla:
        st.dataframe(filas_tabla, use_container_width=True, hide_index=True)
    else:
        st.info("No hay datos para mostrar en la tabla.")

# ==============================================================================
# TAB 3: REGISTRAR Y ACTIVAR NUEVO EQUIPO
# ==============================================================================
with tab_nuevo:
    st.markdown("#### ⚡ Bóveda de Activación: Nuevo Equipo por HWID")
    st.write("Genera una licencia firmada criptográficamente e inscríbela directamente en Firebase.")

    col_n1, col_n2 = st.columns(2)
    with col_n1:
        nuevo_hwid = st.text_input("ID de Equipo (HWID)", placeholder="BORA-XXXX-XXXX-XXXX").strip().upper()
        col_nt1, col_nt2 = st.columns(2)
        with col_nt1:
            sel_taller = st.selectbox("Taller Predeterminado", PRESETS_ETIQUETAS + ["Otro (Escribir manual)", "Sin asignar"])
            if sel_taller.startswith("Otro"):
                in_taller = st.text_input("Nombre del Taller:", "").strip()
            else:
                in_taller = sel_taller
        with col_nt2:
            in_usuario = st.text_input("Usuario / Operador:", placeholder="Ej: Angelo, Robert...").strip()

    with col_n2:
        dias_reg = st.number_input("Días de Suscripción:", min_value=1, max_value=365, value=30)
        st.write("**Presets Rápidos:**")
        col_d1, col_d2, col_d3, col_d4 = st.columns(4)
        with col_d1:
            if st.button("15 Días"):
                dias_reg = 15
        with col_d2:
            if st.button("30 Días"):
                dias_reg = 30
        with col_d3:
            if st.button("90 Días"):
                dias_reg = 90
        with col_d4:
            if st.button("365 Días"):
                dias_reg = 365

    if st.button("⚡ GENERAR LICENCIA Y ACTIVAR EN FIREBASE", use_container_width=True):
        if not nuevo_hwid.startswith("BORA-") or len(nuevo_hwid) < 15:
            st.error("Ingresa un HWID con formato válido (Ej: BORA-XXXX-XXXX-XXXX).")
        else:
            cl_creada, venc_creado = generar_clave_firmada(nuevo_hwid, int(dias_reg))
            peticion_firebase("PATCH", f"equipos/{nuevo_hwid}", {
                "taller": in_taller or "Sin asignar",
                "cliente": in_usuario or "Sin asignar",
                "clave": cl_creada,
                "dia_vencimiento": venc_creado,
                "bloqueado": False,
                "clave_bloqueada": ""
            })
            st.success(f"¡Equipo `{nuevo_hwid}` activado exitosamente por {dias_reg} días!")
            st.code(cl_creada, language="text")
            st.balloons()

# ==============================================================================
# TAB 4: PUBLICADOR DE ACTUALIZACIONES OVER-THE-AIR (OTA)
# ==============================================================================
with tab_ota:
    st.markdown("#### 🚀 Publicador de Actualizaciones OTA (Google Drive / Firebase)")
    st.write("Notifica automáticamente a todas las computadoras Bora Design NestPro conectadas para que descarguen la última versión.")

    # Consultar versión actual en la nube
    try:
        ota_actual = peticion_firebase("GET", "actualizaciones/nestpro") or {}
    except Exception:
        ota_actual = {}

    v_act = ota_actual.get("version", "No configurada")
    b_act = ota_actual.get("build", "---")
    url_act = ota_actual.get("url_descarga", "---")
    nov_act = ota_actual.get("novedades", "---")

    st.markdown(f"""
        <div class="mobile-eq-card activa" style="margin-bottom: 20px;">
            <div style="font-size: 0.8rem; color: #94A3B8;">VERSIÓN ACTIVA EN LA NUBE:</div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #34D399;">{v_act} (Build {b_act})</div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 4px;">Link: {url_act}</div>
            <div style="font-size: 0.85rem; color: #E2E8F0; margin-top: 6px;"><b>Novedades:</b> {nov_act}</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("form_ota"):
        st.write("**Publicar Nueva Versión:**")
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            ota_nueva_v = st.text_input("Versión Oficial (ej. v4.6 Industrial Edition):", value=v_act)
            ota_nuevo_b = st.number_input("Número de Build (ej. 2026102701):", value=int(b_act) if str(b_act).isdigit() else 2026102701)
        with col_o2:
            ota_url = st.text_input("Enlace de Descarga Google Drive:", value=url_act)
            ota_nov = st.text_area("Novedades y Cambios (se mostrarán al cliente):", value=nov_act)

        btn_pub_ota = st.form_submit_button("🚀 PUBLICAR ACTUALIZACIÓN EN TIEMPO REAL")
        if btn_pub_ota:
            if not ota_nueva_v or not ota_url:
                st.error("Por favor completa al menos la versión y el enlace de descarga.")
            else:
                payload_ota = {
                    "version": ota_nueva_v.strip(),
                    "build": int(ota_nuevo_b),
                    "url_descarga": ota_url.strip(),
                    "novedades": ota_nov.strip(),
                    "fecha_publicacion": int(time.time()),
                    "publicado_por": "Bora Admin Web"
                }
                peticion_firebase("PATCH", "actualizaciones/nestpro", payload_ota)
                st.success(f"¡Actualización `{ota_nueva_v}` publicada en Firebase! Todas las PCs conectadas recibirán la notificación automática.")
                st.rerun()
