import streamlit as st
import urllib.request
import json
import hmac
import hashlib
import time
import datetime

# ==============================================================================
# CONFIGURACIÓN Y SEGURIDAD BORA DESIGN ADMIN WEB
# ==============================================================================
FIREBASE_URL = "https://bora-design-nestpro-default-rtdb.firebaseio.com"
SECRETO_MAESTRO_BORA = b"BoraDesign_Angelo_SecretKey_2026_Pro_V3_Monthly"
EPOCA_BASE_DIAS = 19723
CLAVE_ADMINISTRADOR = "Bora2026Admin*"  # Cambia esta contraseña por la que prefieras

st.set_page_config(page_title="Bora Design Admin", page_icon="⚡", layout="centered")

# Estilos visuales corporativos en tonos oscuros y rojo Bora
st.markdown("""
    <style>
    .main { background-color: #0d0d0d; color: #ffffff; }
    h1, h2, h3 { color: #ffffff; }
    .stButton>button {
        background-color: #e60000;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        border: none;
        width: 100%;
        padding: 10px;
    }
    .stButton>button:hover { background-color: #8a0000; color: white; }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SISTEMA DE LOGIN SENCILLO
# ------------------------------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.markdown("<h2 style='text-align: center; color: #e60000;'>BORA DESIGN NESTPRO</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #b0b0b0;'>Panel de Administración Móvil</p>", unsafe_allow_html=True)
    password = st.text_input("Contraseña de Administrador", type="password")
    if st.button("Iniciar Sesión"):
        if password == CLAVE_ADMINISTRADOR:
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta")
    st.stop()

# ------------------------------------------------------------------------------
# FUNCIONES DE LICENCIAMIENTO Y FIREBASE
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

def peticion_firebase(metodo, ruta, datos=None):
    url = f"{FIREBASE_URL.rstrip('/')}/{ruta}.json"
    body = json.dumps(datos).encode("utf-8") if datos is not None else None
    req = urllib.request.Request(url, data=body, method=metodo, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=6) as resp:
        raw = resp.read().decode("utf-8")
        return json.loads(raw) if raw else None

# ------------------------------------------------------------------------------
# INTERFAZ MÓVIL DEL PANEL
# ------------------------------------------------------------------------------
st.markdown("### ⚡ Panel Admin - Bora Design")
if st.button("🚪 Cerrar Sesión"):
    st.session_state.autenticado = False
    st.rerun()

st.divider()

try:
    equipos_data = peticion_firebase("GET", "equipos") or {}
except Exception as e:
    st.error(f"Error al conectar con Firebase: {e}")
    equipos_data = {}

if not equipos_data:
    st.info("No hay equipos registrados en la base de datos todavía.")
else:
    st.markdown(f"**Total de equipos registrados:** {len(equipos_data)}")
    
    # Selector de equipos
    hwid_lista = list(equipos_data.keys())
    hwid_seleccionado = st.selectbox("Seleccionar Taller / Equipo (HWID)", hwid_lista)

    if hwid_seleccionado:
        info = equipos_data[hwid_seleccionado]
        cliente = info.get("cliente", "Sin asignar")
        pc = info.get("pc_nombre", "Desconocido")
        bloqueado = info.get("bloqueado", False)
        clave = info.get("clave", "---")
        dia_venc = int(info.get("dia_vencimiento", 0))
        
        dia_hoy = int(time.time() // 86400)
        dias_restantes = max(0, dia_venc - dia_hoy)

        st.markdown(f"""
        * **Cliente / Taller:** `{cliente}`
        * **Nombre PC:** `{pc}`
        * **Estado:** `{'🚫 BLOQUEADO' if bloqueado else ('✔ ACTIVA (' + str(dias_restantes) + ' días)' if dias_restantes > 0 else '⏳ VENCIDA')}`
        * **Clave Actual:** `{clave}`
        """)

        # Acciones rápidas desde el teléfono
        st.markdown("#### Gestionar Licencia:")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⚡ Añadir +30 Días"):
                dia_base = max(dia_hoy, dia_venc)
                total_nuevos = (dia_base - dia_hoy) + 30
                nueva_cl, nuevo_venc = generar_clave_firmada(hwid_seleccionado, total_nuevos)
                peticion_firebase("PATCH", f"equipos/{hwid_seleccionado}", {
                    "clave": nueva_cl, "dia_vencimiento": nuevo_venc, "bloqueado": False, "clave_bloqueada": ""
                })
                st.success(f"¡30 días sumados! Clave:\n`{nueva_cl}`")
                st.rerun()

        with col2:
            dias_manuales = st.number_input("Días totales exactos:", min_value=1, max_value=365, value=30)
            if st.button("✏️ Aplicar Días Fijos"):
                nueva_cl, nuevo_venc = generar_clave_firmada(hwid_seleccionado, dias_manuales)
                peticion_firebase("PATCH", f"equipos/{hwid_seleccionado}", {
                    "clave": nueva_cl, "dia_vencimiento": nuevo_venc, "bloqueado": False, "clave_bloqueada": ""
                })
                st.success(f"¡Actualizado a {dias_manuales} días!\n`{nueva_cl}`")
                st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            if bloqueado:
                if st.button("🔓 Desbloquear PC"):
                    peticion_firebase("PATCH", f"equipos/{hwid_seleccionado}", {"bloqueado": False, "clave_bloqueada": ""})
                    st.success("¡Equipo desbloqueado!")
                    st.rerun()
            else:
                if st.button("🚫 Bloquear PC"):
                    peticion_firebase("PATCH", f"equipos/{hwid_seleccionado}", {"bloqueado": True, "clave_bloqueada": clave})
                    st.error("¡Equipo bloqueado en vivo!")
                    st.rerun()

        with col4:
            if st.button("🗑️ Eliminar Registro"):
                peticion_firebase("DELETE", f"equipos/{hwid_seleccionado}")
                st.success("Registro eliminado.")
                st.rerun()