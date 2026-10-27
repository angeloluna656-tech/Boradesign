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
import base64

# ==============================================================================
# CONFIGURACIÓN Y SEGURIDAD BORA DESIGN ADMIN WEB
# ==============================================================================
FIREBASE_URL = os.environ.get("BORA_FIREBASE_URL", "https://bora-design-nestpro-default-rtdb.firebaseio.com")
SECRETO_MAESTRO_BORA = b"BoraDesign_Angelo_SecretKey_2026_Pro_V3_Monthly"
EPOCA_BASE_DIAS = 19723
PRESETS_ETIQUETAS = ["Poseidon", "Ocampo", "Heidy lee Sport"]
CLAVE_ADMINISTRADOR = os.environ.get("BORA_ADMIN_PASSWORD", "Bora2026Admin*")
MAX_INTENTOS_LOGIN = 5
SEGUNDOS_BLOQUEO_LOGIN = 60

# Logo Oficial Bora Design (Blanco alta resolución)
LOGO_BORA_BASE64 = "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"

st.set_page_config(
    page_title="Bora Design — Panel de Control",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# CSS 100% RESPONSIVE: DARK STUDIO & MOBILE-FIRST ULTRA COMPACT
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .stApp {
        background: radial-gradient(circle at 50% 0%, #0F172A 0%, #070A10 70%, #030712 100%) !important;
        color: #F8FAFC !important;
    }

    /* Contenedor principal sin bordes gigantes */
    .block-container {
        padding-top: 0.8rem !important;
        padding-bottom: 2rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 1200px !important;
    }

    /* Navbar Superior Compacta y Responsiva */
    .bora-navbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 10px 16px;
        margin-bottom: 14px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
    }

    .bora-nav-left {
        display: flex;
        align-items: center;
        gap: 14px;
    }

    .bora-nav-logo {
        height: 32px;
        max-width: 135px;
        object-fit: contain;
        filter: drop-shadow(0 0 8px rgba(225, 29, 72, 0.3));
    }

    .bora-nav-title {
        font-size: 0.95rem;
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.01em;
        margin: 0;
        line-height: 1.1;
    }

    .bora-nav-sub {
        font-size: 0.70rem;
        font-weight: 600;
        color: #94A3B8;
        margin: 0;
    }

    .bora-live-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 16px;
    }

    .pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(0.95); opacity: 0.8; }
        50% { transform: scale(1.2); opacity: 1; }
        100% { transform: scale(0.95); opacity: 0.8; }
    }

    /* Bento KPI Grid Ultra Compacto */
    .bento-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-bottom: 16px;
    }

    .bento-item {
        background: rgba(17, 24, 39, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        padding: 10px 14px;
        position: relative;
        overflow: hidden;
    }

    .bento-item::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
    }

    .b-cyan::before { background: #38BDF8; }
    .b-emerald::before { background: #10B981; }
    .b-crimson::before { background: #E11D48; }
    .b-amber::before { background: #F59E0B; }

    .bento-label {
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #94A3B8;
        margin-bottom: 2px;
    }

    .bento-num {
        font-size: 1.45rem;
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
    }

    .bento-desc {
        font-size: 0.68rem;
        font-weight: 500;
        color: #64748B;
    }

    /* Tarjeta de Equipo Móvil */
    .eq-card {
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }

    .eq-card.activa { border-left: 4px solid #10B981; }
    .eq-card.bloqueada { border-left: 4px solid #E11D48; }
    .eq-card.vencida { border-left: 4px solid #F59E0B; }

    .eq-title-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        margin-bottom: 6px;
    }

    .eq-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #FFFFFF;
    }

    .eq-tag {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 5px;
        font-size: 0.68rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }

    .eq-tag-taller { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .eq-tag-online { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .eq-tag-offline { background: rgba(100, 116, 139, 0.15); color: #94A3B8; border: 1px solid rgba(100, 116, 139, 0.3); }
    .eq-tag-activa { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .eq-tag-bloq { background: rgba(225, 29, 72, 0.15); color: #FDA4AF; border: 1px solid rgba(225, 29, 72, 0.3); }
    .eq-tag-venc { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }

    .eq-info-line {
        font-size: 0.78rem;
        color: #94A3B8;
        margin-bottom: 4px;
    }

    .code-box {
        font-family: 'JetBrains Mono', Consolas, monospace;
        font-size: 0.80rem;
        font-weight: 700;
        background: #090D16;
        border: 1px solid #1E293B;
        border-radius: 6px;
        padding: 5px 8px;
        color: #38BDF8;
        letter-spacing: 0.03em;
        margin: 4px 0;
        word-break: break-all;
    }

    .code-key {
        color: #34D399 !important;
        background: #05140D !important;
        border-color: #059669 !important;
    }

    /* Botones Táctiles */
    .stButton>button {
        background: linear-gradient(180deg, #F43F5E 0%, #E11D48 100%) !important;
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        border-radius: 8px !important;
        border: 1px solid #FB7185 !important;
        padding: 6px 10px !important;
        min-height: 38px !important;
        transition: all 0.15s ease !important;
    }

    .stButton>button:hover {
        background: linear-gradient(180deg, #FB7185 0%, #E11D48 100%) !important;
        transform: translateY(-1px) !important;
    }

    /* Media Queries para Teléfonos */
    @media (max-width: 680px) {
        .bento-row {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 8px !important;
        }
        .bora-navbar {
            padding: 8px 12px !important;
        }
        .bora-nav-title {
            font-size: 0.85rem !important;
        }
        .bora-nav-logo {
            height: 24px !important;
        }
        .block-container {
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# LOGIN SEGURO CON HMAC
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
            <div style="text-align: center; margin-top: 30px; margin-bottom: 20px;">
                <img src="data:image/png;base64,{LOGO_BORA_BASE64}" style="max-height: 52px; width: auto; object-fit: contain; filter: drop-shadow(0 0 12px rgba(225,29,72,0.35));" />
                <h3 style="margin-top: 12px; font-weight: 800; color: #FFFFFF;">Panel de Licencias</h3>
                <p style="color: #94A3B8; font-size: 0.82rem;">Ingresa la clave maestra para administrar equipos</p>
            </div>
        """, unsafe_allow_html=True)

        ahora_login = time.time()
        if ahora_login < st.session_state.bloqueado_hasta:
            restante = int(st.session_state.bloqueado_hasta - ahora_login)
            st.error(f"Acceso bloqueado por seguridad ({restante}s restantes).")
            st.stop()

        pwd = st.text_input("Contraseña de Administrador", type="password", placeholder="••••••••••••")
        if st.button("INGRESAR AL PANEL", use_container_width=True):
            if hmac.compare_digest(pwd.encode("utf-8"), CLAVE_ADMINISTRADOR.encode("utf-8")):
                st.session_state.autenticado = True
                st.session_state.intentos_fallidos = 0
                st.rerun()
            else:
                st.session_state.intentos_fallidos += 1
                if st.session_state.intentos_fallidos >= MAX_INTENTOS_LOGIN:
                    st.session_state.bloqueado_hasta = time.time() + SEGUNDOS_BLOQUEO_LOGIN
                    st.session_state.intentos_fallidos = 0
                    st.error(f"Bloqueado temporalmente por {SEGUNDOS_BLOQUEO_LOGIN}s.")
                else:
                    rest = MAX_INTENTOS_LOGIN - st.session_state.intentos_fallidos
                    st.error(f"Contraseña incorrecta ({rest} intentos restantes).")
    st.stop()

# ------------------------------------------------------------------------------
# FUNCIONES CRIPTOGRÁFICAS Y FIREBASE
# ------------------------------------------------------------------------------
def generar_clave_firmada(hwid_cliente, dias_vigencia=30):
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
    return (
        f"{saludo}\n\n"
        f"Te recordamos que tu licencia de *Bora Design NestPro*{equipo_info} {estado}.\n\n"
        f"Si deseas renovar tu suscripción mensual para seguir optimizando tela y anidando sin interrupciones, "
        f"por favor indícanos para reactivar tu equipo de inmediato.\n\n"
        f"¡Muchas gracias por confiar en Bora Design!"
    )

# ------------------------------------------------------------------------------
# DATOS EN VIVO DESDE FIREBASE
# ------------------------------------------------------------------------------
try:
    raw_equipos = peticion_firebase("GET", "equipos") or {}
    equipos_data = raw_equipos if isinstance(raw_equipos, dict) else {}
    sync_ok = True
except Exception:
    equipos_data = {}
    sync_ok = False

ahora_ts = int(time.time())
dia_hoy = int(ahora_ts // 86400)
hora_actual_str = time.strftime("%H:%M:%S")

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
# NAVBAR SUPERIOR COMPACTA Y MODERNA
# ------------------------------------------------------------------------------
col_nav_brand, col_nav_act = st.columns([4, 1.2])

with col_nav_brand:
    st.markdown(f"""
        <div class="bora-navbar">
            <div class="bora-nav-left">
                <img src="data:image/png;base64,{LOGO_BORA_BASE64}" class="bora-nav-logo" />
                <div>
                    <div class="bora-nav-title">BORA DESIGN NESTPRO</div>
                    <div class="bora-nav-sub">Panel de Licencias Cloud</div>
                </div>
            </div>
            <div class="bora-live-pill">
                <span class="pulse-dot"></span>
                <span>{total_pcs} PCs • {hora_actual_str}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_nav_act:
    col_rf, col_so = st.columns(2)
    with col_rf:
        if st.button("🔄", help="Actualizar datos", use_container_width=True):
            st.rerun()
    with col_so:
        if st.button("🚪", help="Cerrar sesión", use_container_width=True):
            st.session_state.autenticado = False
            st.rerun()

# ------------------------------------------------------------------------------
# BENTO KPI CARDS (4 TILES COMPACTOS)
# ------------------------------------------------------------------------------
st.markdown(f"""
    <div class="bento-row">
        <div class="bento-item b-cyan">
            <div class="bento-label">Total Equipos</div>
            <div class="bento-num">{total_pcs}</div>
            <div class="bento-desc">Registrados</div>
        </div>
        <div class="bento-item b-emerald">
            <div class="bento-label">En Línea</div>
            <div class="bento-num" style="color: #34D399;">{online_pcs}</div>
            <div class="bento-desc">Ping activo</div>
        </div>
        <div class="bento-item b-crimson">
            <div class="bento-label">Activas</div>
            <div class="bento-num" style="color: #FB7185;">{activas_pcs}</div>
            <div class="bento-desc">Con licencia</div>
        </div>
        <div class="bento-item b-amber">
            <div class="bento-label">Atención</div>
            <div class="bento-num" style="color: #FBBF24;">{atencion_pcs}</div>
            <div class="bento-desc">&le;5d o pausadas</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES
# ------------------------------------------------------------------------------
tab_tarjetas, tab_tabla, tab_nuevo, tab_ota = st.tabs([
    "📱 Equipos",
    "📊 Tabla Global",
    "➕ Activar Equipo",
    "🚀 Actualizaciones OTA"
])

todos_talleres = sorted(list({
    str(v.get("taller", "")).strip() for v in equipos_data.values()
    if isinstance(v, dict) and str(v.get("taller", "")).strip() and str(v.get("taller", "")).strip() != "Sin asignar"
} | set(PRESETS_ETIQUETAS)))

# ==============================================================================
# TAB 1: TARJETAS DE EQUIPOS (RESPONSIVE MÓVIL Y ESCRITORIO)
# ==============================================================================
with tab_tarjetas:
    col_s1, col_s2, col_s3 = st.columns([2, 1.2, 1.2])
    with col_s1:
        busqueda_txt = st.text_input("Buscar", placeholder="Buscar por HWID, Taller, Cliente, PC...", label_visibility="collapsed").strip().lower()
    with col_s2:
        filtro_estado = st.selectbox(
            "Estado",
            ["Todos", "🟢 En Línea", "⚠️ Por Vencer (≤5d)", "🚫 Bloqueadas / Vencidas"],
            label_visibility="collapsed"
        )
    with col_s3:
        filtro_taller = st.selectbox(
            "Taller",
            ["Todos los Talleres"] + todos_talleres + ["Sin asignar"],
            label_visibility="collapsed"
        )

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

        if busqueda_txt:
            corpus = f"{hwid} {taller} {cliente} {pc}".lower()
            if busqueda_txt not in corpus:
                continue

        if filtro_estado == "🟢 En Línea" and not en_linea:
            continue
        elif filtro_estado == "⚠️ Por Vencer (≤5d)" and not (not bloqueado and 0 < dias_rest <= 5):
            continue
        elif filtro_estado == "🚫 Bloqueadas / Vencidas" and not (bloqueado or dias_rest == 0):
            continue

        if filtro_taller != "Todos los Talleres":
            if filtro_taller == "Sin asignar" and taller != "Sin asignar":
                continue
            elif filtro_taller != "Sin asignar" and taller.lower() != filtro_taller.lower():
                continue

        equipos_filtrados[hwid] = info

    if not equipos_filtrados:
        st.info("No se encontraron equipos con los filtros seleccionados.")
    else:
        st.caption(f"Mostrando **{len(equipos_filtrados)}** de **{total_pcs}** equipos.")

        for hwid, info in equipos_filtrados.items():
            taller = str(info.get("taller", "")).strip() or "Sin asignar"
            cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
            pc = info.get("pc_nombre", "PC")
            usuario_win = info.get("usuario_pc", "")
            bloqueado = bool(info.get("bloqueado", False))
            dia_venc = int(info.get("dia_vencimiento", 0))
            clave_act = info.get("clave", "---") or "---"
            ultimo_ts = int(info.get("ultimo_ping", 0))

            en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
            dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0

            if bloqueado:
                card_cls = "bloqueada"
                tag_lic = "<span class='eq-tag eq-tag-bloq'>🚫 BLOQUEADA</span>"
                vig_txt = f"<span style='color: #FDA4AF; font-weight: 700;'>Pausada ({dias_rest}d)</span>"
            elif dias_rest > 0:
                card_cls = "activa"
                col_c = "#34D399" if dias_rest > 5 else "#FBBF24"
                tag_lic = f"<span class='eq-tag eq-tag-activa'>✔ ACTIVA</span>"
                vig_txt = f"<span style='color: {col_c}; font-weight: 700;'>{dias_rest} día(s)</span>"
            else:
                card_cls = "vencida"
                tag_lic = "<span class='eq-tag eq-tag-venc'>⏳ VENCIDA</span>"
                vig_txt = "<span style='color: #FBBF24; font-weight: 700;'>0 días (Vencida)</span>"

            tag_con = "<span class='eq-tag eq-tag-online'>🟢 ONLINE</span>" if en_linea else "<span class='eq-tag eq-tag-offline'>⚫ OFFLINE</span>"
            tag_taller = f"<span class='eq-tag eq-tag-taller'>🏷️ {taller}</span>"
            dest_nombre = cliente if cliente != "Sin asignar" else taller

            st.markdown(f"""
                <div class="eq-card {card_cls}">
                    <div class="eq-title-row">
                        <div>
                            {tag_taller}
                            <span class="eq-name" style="margin-left: 6px;">{cliente}</span>
                        </div>
                        <div style="display: flex; gap: 6px;">
                            {tag_con}
                            {tag_lic}
                        </div>
                    </div>
                    <div class="eq-info-line">
                        🖥️ <b>{pc}</b> {f'({usuario_win})' if usuario_win else ''} • {vig_txt}
                    </div>
                    <div class="code-box">ID: {hwid}</div>
                    <div class="code-box code-key">CLAVE: {clave_act}</div>
                </div>
            """, unsafe_allow_html=True)

            # Botones en fila compacta
            c_b1, c_b2, c_b3, c_b4, c_b5 = st.columns([1.2, 1.4, 1.2, 0.8, 0.6])

            with c_b1:
                if st.button("⚡ +30 Días", key=f"b30_{hwid}", use_container_width=True):
                    dia_base = max(dia_hoy, dia_venc)
                    total_nuevos = (dia_base - dia_hoy) + 30
                    nueva_cl, nuevo_venc = generar_clave_firmada(hwid, total_nuevos)
                    peticion_firebase("PATCH", f"equipos/{hwid}", {
                        "clave": nueva_cl, "dia_vencimiento": nuevo_venc, "bloqueado": False, "clave_bloqueada": ""
                    })
                    st.success("¡+30 días aplicados!")
                    st.rerun()

            with c_b2:
                msg_wsp = redactar_mensaje_whatsapp(dest_nombre, dias_rest, pc, hwid)
                msg_enc = urllib.parse.quote(msg_wsp)
                link_wsp = f"https://api.whatsapp.com/send?text={msg_enc}"
                st.markdown(f"""
                    <a href="{link_wsp}" target="_blank" style="text-decoration: none;">
                        <button style="width: 100%; min-height: 38px; background: #064E3B; color: #34D399; font-weight: 700; font-size: 0.82rem; border: 1px solid #059669; border-radius: 8px; cursor: pointer;">
                            💬 WhatsApp
                        </button>
                    </a>
                """, unsafe_allow_html=True)

            with c_b3:
                if bloqueado:
                    if st.button("🔓 Desbloq", key=f"unb_{hwid}", use_container_width=True):
                        v_rest = dia_venc
                        if v_rest <= dia_hoy and clave_act and clave_act != "---":
                            v_rest = extraer_dia_vencimiento_de_clave(clave_act)
                        if v_rest <= dia_hoy:
                            nueva_cl, nuevo_venc = generar_clave_firmada(hwid, 30)
                            peticion_firebase("PATCH", f"equipos/{hwid}", {
                                "bloqueado": False, "clave_bloqueada": "", "clave": nueva_cl, "dia_vencimiento": nuevo_venc
                            })
                        else:
                            peticion_firebase("PATCH", f"equipos/{hwid}", {
                                "bloqueado": False, "clave_bloqueada": "", "dia_vencimiento": v_rest
                            })
                        st.success("Desbloqueado")
                        st.rerun()
                else:
                    if st.button("🚫 Bloquear", key=f"blk_{hwid}", use_container_width=True):
                        peticion_firebase("PATCH", f"equipos/{hwid}", {"bloqueado": True, "clave_bloqueada": clave_act})
                        st.warning("Bloqueado")
                        st.rerun()

            with c_b4:
                if st.button("+15d", key=f"b15_{hwid}", use_container_width=True):
                    dia_base = max(dia_hoy, dia_venc)
                    total_nuevos = (dia_base - dia_hoy) + 15
                    nueva_cl, nuevo_venc = generar_clave_firmada(hwid, total_nuevos)
                    peticion_firebase("PATCH", f"equipos/{hwid}", {
                        "clave": nueva_cl, "dia_vencimiento": nuevo_venc, "bloqueado": False, "clave_bloqueada": ""
                    })
                    st.success("+15d aplicados")
                    st.rerun()

            with c_b5:
                with st.popover("⚙️"):
                    st.write(f"**Editar:** `{cliente}`")
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
                        if st.button("Heidy", key=f"hls_{hwid}"):
                            peticion_firebase("PATCH", f"equipos/{hwid}", {"taller": "Heidy lee Sport"})
                            st.rerun()

                    ed_tal = st.text_input("Taller:", value="" if taller == "Sin asignar" else taller, key=f"t_{hwid}")
                    ed_cli = st.text_input("Operador:", value="" if cliente == "Sin asignar" else cliente, key=f"c_{hwid}")
                    if st.button("Guardar", key=f"sv_{hwid}"):
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "taller": ed_tal.strip() or "Sin asignar",
                            "cliente": ed_cli.strip() or "Sin asignar"
                        })
                        st.rerun()

                    st.divider()
                    d_fij = st.number_input("Días Fijos:", min_value=1, max_value=365, value=30, key=f"df_{hwid}")
                    if st.button("Aplicar Días", key=f"bdf_{hwid}"):
                        cl_f, v_f = generar_clave_firmada(hwid, d_fij)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": cl_f, "dia_vencimiento": v_f, "bloqueado": False, "clave_bloqueada": ""
                        })
                        st.rerun()

                    st.divider()
                    if st.button("🗑️ Eliminar", key=f"del_{hwid}"):
                        peticion_firebase("DELETE", f"equipos/{hwid}")
                        st.rerun()

            st.write("")

# ==============================================================================
# TAB 2: VISTA TABLA GLOBAL
# ==============================================================================
with tab_tabla:
    filas_t = []
    for hwid, info in sorted(equipos_data.items()):
        if not isinstance(info, dict):
            continue
        taller = str(info.get("taller", "")).strip() or "Sin asignar"
        cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
        pc = info.get("pc_nombre", "PC")
        bloqueado = bool(info.get("bloqueado", False))
        dia_venc = int(info.get("dia_vencimiento", 0))
        clave_act = info.get("clave", "---") or "---"
        ultimo_ts = int(info.get("ultimo_ping", 0))

        en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
        dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0
        ult_ping_str = datetime.datetime.fromtimestamp(ultimo_ts).strftime("%d/%m %H:%M") if ultimo_ts > 0 else "Nunca"

        if bloqueado:
            est_txt = "🚫 BLOQUEADO"
        elif dias_rest > 0:
            est_txt = f"✔ ACTIVA ({dias_rest}d)"
        else:
            est_txt = "⏳ VENCIDA"

        filas_t.append({
            "HWID": hwid,
            "Taller": taller,
            "Usuario": cliente,
            "PC": pc,
            "Conexión": "🟢 Online" if en_linea else "⚫ Offline",
            "Estado": est_txt,
            "Días": dias_rest,
            "Último Ping": ult_ping_str,
            "Clave": clave_act
        })

    if filas_t:
        st.dataframe(filas_t, use_container_width=True, hide_index=True)
    else:
        st.info("No hay datos registrados en Firebase.")

# ==============================================================================
# TAB 3: ACTIVAR NUEVO EQUIPO
# ==============================================================================
with tab_nuevo:
    st.markdown("#### ⚡ Activación de Licencia por HWID")
    col_n1, col_n2 = st.columns(2)
    with col_n1:
        nuevo_hwid = st.text_input("ID de Equipo (HWID)", placeholder="BORA-XXXX-XXXX-XXXX").strip().upper()
        col_nt1, col_nt2 = st.columns(2)
        with col_nt1:
            sel_tal = st.selectbox("Taller", PRESETS_ETIQUETAS + ["Otro", "Sin asignar"])
            in_tal = st.text_input("Nombre Taller:") if sel_tal == "Otro" else sel_tal
        with col_nt2:
            in_cli = st.text_input("Usuario / Operador:", placeholder="Ej: Angelo, Robert...").strip()

    with col_n2:
        dias_reg = st.number_input("Días de Vigencia:", min_value=1, max_value=365, value=30)
        st.write("Presets Rápidos:")
        cd1, cd2, cd3, cd4 = st.columns(4)
        with cd1:
            if st.button("15d"): dias_reg = 15
        with cd2:
            if st.button("30d"): dias_reg = 30
        with cd3:
            if st.button("90d"): dias_reg = 90
        with cd4:
            if st.button("365d"): dias_reg = 365

    if st.button("⚡ GENERAR Y ACTIVAR EN NUBE", use_container_width=True):
        if not nuevo_hwid.startswith("BORA-") or len(nuevo_hwid) < 15:
            st.error("Formato inválido. Debe ser BORA-XXXX-XXXX-XXXX.")
        else:
            cl_creada, venc_creado = generar_clave_firmada(nuevo_hwid, int(dias_reg))
            peticion_firebase("PATCH", f"equipos/{nuevo_hwid}", {
                "taller": in_tal or "Sin asignar",
                "cliente": in_cli or "Sin asignar",
                "clave": cl_creada,
                "dia_vencimiento": venc_creado,
                "bloqueado": False,
                "clave_bloqueada": ""
            })
            st.success(f"¡Equipo {nuevo_hwid} activado por {dias_reg} días!")
            st.code(cl_creada, language="text")

# ==============================================================================
# TAB 4: ACTUALIZACIONES OTA
# ==============================================================================
with tab_ota:
    st.markdown("#### 🚀 Publicar Actualización OTA")
    try:
        ota_act = peticion_firebase("GET", "actualizaciones/nestpro") or {}
    except Exception:
        ota_act = {}

    v_a = ota_act.get("version", "---")
    b_a = ota_act.get("build", "---")
    u_a = ota_act.get("url_descarga", "---")
    n_a = ota_act.get("novedades", "---")

    st.markdown(f"""
        <div class="eq-card activa" style="margin-bottom: 16px;">
            <div style="font-size: 0.75rem; color: #94A3B8;">VERSIÓN EN LA NUBE:</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #34D399;">{v_a} (Build {b_a})</div>
            <div style="font-size: 0.75rem; color: #64748B;">Link: {u_a}</div>
            <div style="font-size: 0.8rem; color: #E2E8F0; margin-top: 4px;"><b>Novedades:</b> {n_a}</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("form_ota_pub"):
        co1, co2 = st.columns(2)
        with co1:
            nv_v = st.text_input("Versión Oficial:", value=v_a)
            nv_b = st.number_input("Número de Build:", value=int(b_a) if str(b_a).isdigit() else 2026102701)
        with co2:
            nv_u = st.text_input("Enlace Google Drive:", value=u_a)
            nv_n = st.text_area("Novedades:", value=n_a)

        if st.form_submit_button("🚀 PUBLICAR EN TIEMPO REAL"):
            if nv_v and nv_u:
                peticion_firebase("PATCH", "actualizaciones/nestpro", {
                    "version": nv_v.strip(),
                    "build": int(nv_b),
                    "url_descarga": nv_u.strip(),
                    "novedades": nv_n.strip(),
                    "fecha_publicacion": int(time.time()),
                    "publicado_por": "Admin Web"
                })
                st.success("¡Actualización publicada en Firebase!")
                st.rerun()
