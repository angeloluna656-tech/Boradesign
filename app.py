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
# CONFIGURACION Y SEGURIDAD BORA DESIGN // ENTERPRISE FLEET MANAGEMENT
# ==============================================================================
FIREBASE_URL = os.environ.get("BORA_FIREBASE_URL", "https://bora-design-nestpro-default-rtdb.firebaseio.com")
SECRETO_MAESTRO_BORA = b"BoraDesign_Angelo_SecretKey_2026_Pro_V3_Monthly"
EPOCA_BASE_DIAS = 19723
FIREBASE_SECRET_DEFAULT = "UKSc4y38ZoRp0WSJ4eA3ub9nlXIefv4WDDHv2tvz"

PRESETS_ETIQUETAS = ["Poseidon", "Ocampo", "Heidy lee Sport", "Sublimacion Express", "Taller Central"]
CLAVE_ADMINISTRADOR = os.environ.get("BORA_ADMIN_PASSWORD", "Bora2026Admin*")
MAX_INTENTOS_LOGIN = 5
SEGUNDOS_BLOQUEO_LOGIN = 60

# Logo Oficial Completo Bora Design (903x380 px, 100% integro en Base64)
LOGO_BORA_BASE64 = "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"

st.set_page_config(
    page_title="Bora Design NestPro | Fleet Cloud",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# PAQUETE VECTORIAL DE ICONOS SVG (100% CERO EMOJIS // WCAG ACCESSIBLE)
# ==============================================================================
ICONS = {
    "logo": '<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#F43F5E" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>',
    "server": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="2" width="20" height="8" rx="2" ry="2"/><rect x="2" y="14" width="20" height="8" rx="2" ry="2"/><line x1="6" y1="6" x2="6.01" y2="6"/><line x1="6" y1="18" x2="6.01" y2="18"/></svg>',
    "pc": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    "key": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 2l-2 2m-1.5 1.5L16 7l-1.5-1.5-1.5 1.5-1.5-1.5-2 2a5 5 0 1 0 7 7l2-2 1.5 1.5 1.5-1.5 1.5 1.5 1.5-1.5 2-2z"/><circle cx="7.5" cy="16.5" r="1.5"/></svg>',
    "whatsapp": '<svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.311.045-.698.076-2.18-.537-1.748-.72-2.884-2.493-2.97-2.61-.088-.117-.714-.951-.714-1.815 0-.865.452-1.29.613-1.465.161-.174.351-.218.468-.218.117 0 .234.001.336.006.107.006.251-.04.392.3.144.348.494 1.205.538 1.293.044.088.073.191.015.305-.059.117-.088.191-.176.293-.088.103-.186.23-.266.309-.088.088-.18.184-.077.361.103.176.458.756.983 1.224.677.603 1.248.789 1.425.877.175.088.278.073.38-.044.103-.117.439-.513.556-.689.117-.176.234-.147.392-.088.161.059 1.02.481 1.196.569.175.088.292.132.336.205.044.074.044.428-.1 1.002z"/></svg>',
    "check": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="20 6 9 17 4 12"/></svg>',
    "alert": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "shield": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "refresh": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>',
    "logout": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>',
    "search": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "clock": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
    "chart": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
    "broadcast": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4.9 19.1C1 15.2 1 8.8 4.9 4.9"/><path d="M7.8 16.2c-2.3-2.3-2.3-6.1 0-8.5"/><circle cx="12" cy="12" r="2"/><path d="M16.2 7.8c2.3 2.3 2.3 6.1 0 8.5"/><path d="M19.1 4.9C23 8.8 23 15.2 19.1 19.1"/></svg>',
    "cloud": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 10h-1.26A8 8 0 1 0 9 20h9a5 5 0 0 0 0-10z"/></svg>',
    "pause": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>',
    "play": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
    "copy": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>',
    "trash": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>',
    "settings": '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "plus": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
    "user": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
    "filter": '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>'
}

# ==============================================================================
# CSS MODERNO BASADO EN GOOGLE CHROME MODERN WEB GUIDANCE (BASELINE 2026)
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

    /* 1. NUKEO DE STREAMLIT COMMUNITY CLOUD CHROME Y MARCAS DE AGUA */
    header,
    header[data-testid="stHeader"],
    .stApp > header,
    #MainMenu,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"],
    .stDeployButton,
    [data-testid="manage-app-button"],
    button[data-testid="manage-app-button"],
    [data-testid="appCreatorAvatar"],
    div[class*="_viewerBadge_"],
    div[class*="viewerBadge"],
    div[class*="styles_viewerBadge"],
    div[class*="embeddedAppMetaInfoBar"],
    div[class*="ProfileBadge"],
    div[class*="profileImage"],
    div[class*="manageAppButton"],
    div[class*="ManageAppButton"],
    div[class*="FloatingActionButton"],
    div[class*="floatingActionButton"],
    div[class*="FloatingButton"],
    div[class*="bottomBar"],
    div[class*="BottomBar"],
    iframe[title="streamlit_viewer"],
    a[href*="streamlit.io"],
    a[href*="streamlit.app"],
    .stActionButton,
    div[data-testid="stToolbarActions"],
    button[data-testid="baseButton-header"],
    div[class*="StyledHeader"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        width: 0 !important;
        height: 0 !important;
        max-width: 0 !important;
        max-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        position: fixed !important;
        top: -99999px !important;
        left: -99999px !important;
        z-index: -99999 !important;
    }

    .stApp > header {
        height: 0px !important;
        min-height: 0px !important;
    }

    /* 2. BASELINE DESIGN SYSTEM: UNIDADES FLUIDAS Y DYNAMIC VIEWPORT (DVH) */
    html, body {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        box-sizing: border-box;
        overflow-x: hidden;
    }

    *, *:before, *:after {
        box-sizing: inherit;
    }

    .stApp {
        background-color: #0A0D14 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(225, 29, 72, 0.12) 0px, transparent 45%),
            radial-gradient(at 100% 0%, rgba(56, 189, 248, 0.08) 0px, transparent 40%),
            radial-gradient(at 50% 100%, rgba(15, 23, 42, 0.95) 0px, transparent 60%) !important;
        color: #F8FAFC !important;
        min-height: 100dvh !important;
    }

    /* 3. CONTENEDOR PRINCIPAL FLUIDO CON SAFE-AREA-INSETS (NOTCHES & BARS) */
    .block-container {
        padding-top: max(1.0rem, env(safe-area-inset-top, 16px)) !important;
        padding-bottom: max(2.5rem, env(safe-area-inset-bottom, 24px)) !important;
        padding-left: clamp(0.75rem, 2vw, 1.25rem) !important;
        padding-right: clamp(0.75rem, 2vw, 1.25rem) !important;
        max-width: 980px !important;
        width: 100% !important;
    }

    /* 4. CABECERA MODERNA CON ASPECT-RATIO INTRÍNSECO */
    .bora-topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(17, 22, 34, 0.92);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: clamp(8px, 1.5vw, 12px) clamp(10px, 2vw, 16px);
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        width: 100%;
    }

    .bora-brand-wrapper {
        display: flex;
        align-items: center;
        gap: clamp(8px, 1.5vw, 12px);
        min-width: 0;
    }

    .bora-main-logo {
        aspect-ratio: 903 / 380;
        height: clamp(30px, 5vw, 38px);
        width: auto;
        max-width: 155px;
        object-fit: contain;
        display: block;
        flex-shrink: 0;
        filter: drop-shadow(0 0 10px rgba(244, 63, 94, 0.35));
    }

    .bora-cloud-pill {
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        background: rgba(244, 63, 94, 0.15);
        color: #FB7185;
        border: 1px solid rgba(244, 63, 94, 0.3);
        padding: 2px 7px;
        border-radius: 6px;
        white-space: nowrap;
    }

    .bora-status-wrapper {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        font-size: 0.72rem;
        font-weight: 700;
        padding: 4px 10px;
        border-radius: 20px;
        white-space: nowrap;
        flex-shrink: 0;
    }

    .bora-pulse-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
        animation: pulse-ring 2s infinite ease-in-out;
    }

    @keyframes pulse-ring {
        0% { transform: scale(0.9); opacity: 0.7; }
        50% { transform: scale(1.3); opacity: 1; }
        100% { transform: scale(0.9); opacity: 0.7; }
    }

    /* 5. RESUMEN DE SALA (KPI GRID CON MINMAX INTRÍNSECO) */
    .fleet-kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: clamp(6px, 1.5vw, 10px);
        margin-bottom: 12px;
        width: 100%;
    }

    .fleet-kpi-card {
        background: rgba(17, 22, 34, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 12px;
        padding: clamp(8px, 1.5vw, 12px) clamp(10px, 1.8vw, 14px);
        display: flex;
        flex-direction: column;
        justify-content: center;
        min-width: 0;
    }

    .kpi-lbl {
        font-size: clamp(0.60rem, 1vw, 0.68rem);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #64748B;
        margin-bottom: 3px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }

    .kpi-val {
        font-size: clamp(1.2rem, 3vw, 1.5rem);
        font-weight: 800;
        color: #FFFFFF;
        line-height: 1.1;
        font-family: 'JetBrains Mono', Consolas, monospace;
    }

    /* 6. CARD PATTERN CON ARQUITECTURA SEMÁNTICA (MODERN WEB GUIDANCE) */
    .asset-card {
        background: rgba(17, 22, 34, 0.92);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: clamp(12px, 2vw, 16px);
        margin-bottom: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        position: relative;
        overflow: hidden;
        width: 100%;
    }

    .asset-card.activa { border-left: 5px solid #10B981; }
    .asset-card.vencida { border-left: 5px solid #F59E0B; }
    .asset-card.bloqueada { border-left: 5px solid #F43F5E; }

    .asset-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 8px;
    }

    .asset-id-group {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        min-width: 0;
    }

    .prod-tag {
        font-size: 0.65rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%);
        color: #FFFFFF;
        padding: 3px 7px;
        border-radius: 5px;
    }

    .asset-name {
        font-size: clamp(0.95rem, 2vw, 1.10rem);
        font-weight: 800;
        color: #FFFFFF;
        letter-spacing: -0.01em;
        word-break: break-word;
    }

    .taller-pill {
        font-size: 0.70rem;
        font-weight: 700;
        background: rgba(245, 158, 11, 0.12);
        color: #FBBF24;
        border: 1px solid rgba(245, 158, 11, 0.25);
        padding: 2px 7px;
        border-radius: 5px;
    }

    .asset-meta-row {
        font-size: clamp(0.72rem, 1.5vw, 0.80rem);
        color: #94A3B8;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
    }

    .mono-pill-box {
        font-family: 'JetBrains Mono', Consolas, monospace;
        font-size: clamp(0.72rem, 1.5vw, 0.80rem);
        font-weight: 600;
        background: #090D15;
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 8px;
        padding: 6px 10px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 6px;
        word-break: break-all;
    }

    /* 7. PESTAÑAS TOUCH-ACCESSIBLES CON INERTIA SCROLL */
    .stTabs [data-baseweb="tab-list"] {
        display: flex !important;
        overflow-x: auto !important;
        white-space: nowrap !important;
        -webkit-overflow-scrolling: touch !important;
        background-color: rgba(17, 22, 34, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        gap: 4px !important;
        margin-bottom: 12px !important;
        scrollbar-width: none !important;
    }
    .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
        display: none !important;
    }

    .stTabs [data-baseweb="tab"] {
        flex-shrink: 0 !important;
        color: #94A3B8 !important;
        background: transparent !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        padding: 8px 14px !important;
        border: none !important;
        transition: all 0.15s ease !important;
        min-height: 42px !important;
        display: inline-flex !important;
        align-items: center !important;
    }

    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        background: linear-gradient(135deg, #F43F5E 0%, #E11D48 100%) !important;
        box-shadow: 0 2px 10px rgba(225, 29, 72, 0.35) !important;
    }

    /* 8. TOUCH TARGETS (WCAG 2.2 / MODERN WEB: MIN 42px HIT AREA) */
    .stButton>button {
        background: #1E293B !important;
        color: #F8FAFC !important;
        font-weight: 700 !important;
        font-size: 0.82rem !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        padding: 8px 12px !important;
        min-height: 42px !important;
        transition: all 0.15s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        width: 100% !important;
    }

    .stButton>button:hover {
        background: #334155 !important;
    }

    /* 9. INPUTS SEGUROS: 16px PARA PREVENIR ZOOM ACCIDENTAL EN IOS */
    .stTextInput input, .stSelectbox [data-baseweb="select"], .stTextArea textarea, .stNumberInput input {
        background-color: #0E1420 !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        min-height: 44px !important;
        font-size: 16px !important;
    }

    /* 10. MEDIA QUERIES SEGÚN MODERN WEB GUIDANCE (MOBILE ADAPTATION) */
    @media (max-width: 640px) {
        .fleet-kpi-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 6px !important;
        }
        .bora-topbar {
            padding: 8px 10px !important;
        }
        .bora-main-logo {
            height: 30px !important;
            max-width: 125px !important;
        }
        .bora-cloud-pill {
            display: none !important;
        }
        .asset-card {
            padding: 12px 10px !important;
        }
        .kpi-val {
            font-size: 1.15rem !important;
        }
    }

    @media (max-width: 380px) {
        .fleet-kpi-grid {
            grid-template-columns: repeat(2, 1fr) !important;
        }
        .bora-main-logo {
            height: 26px !important;
            max-width: 105px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Limpieza activa y triple-redundante del DOM host (Streamlit Cloud shell)
st.markdown("""
<img src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7" style="display:none;position:fixed;top:-9999px;left:-9999px;width:0;height:0;" onload="
(function() {
    function purge() {
        var sel = [
            'div[class*='_viewerBadge_']',
            'div[class*='viewerBadge']',
            'div[class*='styles_viewerBadge']',
            'div[class*='profileImage']',
            'div[class*='_profileImage_']',
            'div[class*='streamlitLogoWrapper']',
            'div[class*='_streamlitLogoWrapper_']',
            'div[class*='embeddedAppMetaInfoBar']',
            'div[class*='ProfileBadge']',
            'div[class*='manageAppButton']',
            'button[data-testid='manage-app-button']',
            '[data-testid='appCreatorAvatar']',
            'img[alt='App Creator Avatar']',
            'header[data-testid='stHeader']',
            'header',
            'footer',
            '#MainMenu',
            '[data-testid='stToolbar']',
            '[data-testid='stDecoration']',
            '.stDeployButton'
        ];
        function removeIn(d) {
            if (!d) return;
            try {
                if (!d.getElementById('bora-parent-nuke-style')) {
                    var s = d.createElement('style');
                    s.id = 'bora-parent-nuke-style';
                    s.textContent = sel.join(',') + ' { display: none !important; visibility: hidden !important; opacity: 0 !important; pointer-events: none !important; width: 0 !important; height: 0 !important; position: fixed !important; top: -9999px !important; }';
                    (d.head || d.body || d.documentElement).appendChild(s);
                }
            } catch(e) {}
            for (var i = 0; i < sel.length; i++) {
                try {
                    var els = d.querySelectorAll(sel[i]);
                    for (var j = 0; j < els.length; j++) {
                        els[j].style.setProperty('display', 'none', 'important');
                        els[j].style.setProperty('visibility', 'hidden', 'important');
                        els[j].remove();
                    }
                } catch(e) {}
            }
        }
        removeIn(document);
        try { if (window.parent && window.parent.document) removeIn(window.parent.document); } catch(e) {}
        try { if (window.top && window.top.document) removeIn(window.top.document); } catch(e) {}
    }
    purge();
    setInterval(purge, 200);
})();
" onerror="this.onload();" />
""", unsafe_allow_html=True)

try:
    import streamlit.components.v1 as _components
    _components.html("""
    <script>
    (function() {
        var sel = [
            'div[class*="_viewerBadge_"]',
            'div[class*="viewerBadge"]',
            'div[class*="styles_viewerBadge"]',
            'div[class*="profileImage"]',
            'div[class*="_profileImage_"]',
            'div[class*="streamlitLogoWrapper"]',
            'div[class*="_streamlitLogoWrapper_"]',
            'div[class*="embeddedAppMetaInfoBar"]',
            'div[class*="ProfileBadge"]',
            'div[class*="manageAppButton"]',
            'button[data-testid="manage-app-button"]',
            '[data-testid="appCreatorAvatar"]',
            'img[alt="App Creator Avatar"]',
            'header[data-testid="stHeader"]',
            'header',
            'footer',
            '#MainMenu',
            '[data-testid="stToolbar"]',
            '[data-testid="stDecoration"]',
            '.stDeployButton'
        ];
        function kill(doc) {
            if (!doc) return;
            try {
                if (!doc.getElementById('bora-host-nuke-style')) {
                    var s = doc.createElement('style');
                    s.id = 'bora-host-nuke-style';
                    s.textContent = sel.join(',') + ' { display: none !important; visibility: hidden !important; opacity: 0 !important; pointer-events: none !important; width: 0 !important; height: 0 !important; position: fixed !important; top: -9999px !important; }';
                    (doc.head || doc.body || doc.documentElement).appendChild(s);
                }
                sel.forEach(function(s) {
                    var els = doc.querySelectorAll(s);
                    for (var i = 0; i < els.length; i++) els[i].remove();
                });
            } catch(e) {}
        }
        function loop() {
            try { kill(window.parent.document); } catch(e) {}
            try { kill(window.top.document); } catch(e) {}
        }
        loop();
        setInterval(loop, 200);
    })();
    </script>
    """, height=0, width=0)
except Exception:
    pass

# ------------------------------------------------------------------------------
# LOGIN SEGURO CON LOGO OFICIAL (100% RESPONSIVE EN MÓVILES)
# ------------------------------------------------------------------------------
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "intentos_fallidos" not in st.session_state:
    st.session_state.intentos_fallidos = 0
if "bloqueado_hasta" not in st.session_state:
    st.session_state.bloqueado_hasta = 0.0

if not st.session_state.autenticado:
    # Contenedor centrado max-width: fluido en moviles y centrado en PC
    st.markdown(f"""
        <div style="max-width: 440px; margin: 20px auto 14px auto; background: rgba(17, 22, 34, 0.95); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 18px; padding: clamp(16px, 4vw, 26px); text-align: center; box-shadow: 0 12px 35px rgba(0,0,0,0.5); width: 100%;">
            <img src="data:image/png;base64,{LOGO_BORA_BASE64}" style="width: min(220px, 75%); height: auto; aspect-ratio: 903 / 380; object-fit: contain; display: block; margin: 0 auto 16px auto; filter: drop-shadow(0 4px 18px rgba(244,63,94,0.45));" alt="Bora Design" />
            <h3 style="margin: 0; font-weight: 800; color: #FFFFFF; font-size: clamp(1.05rem, 2.5vw, 1.20rem); letter-spacing: -0.01em;">PANEL DE LICENCIAS CLOUD</h3>
            <p style="color: #94A3B8; font-size: 0.78rem; margin-top: 4px; margin-bottom: 16px;">Ingresa tu clave maestra para administrar equipos</p>
            <div style="height: 1px; background: rgba(255,255,255,0.08); margin-bottom: 14px;"></div>
        </div>
    """, unsafe_allow_html=True)

    col_l1, col_login, col_l2 = st.columns([0.05, 0.9, 0.05])
    with col_login:
        ahora_login = time.time()
        if ahora_login < st.session_state.bloqueado_hasta:
            restante = int(st.session_state.bloqueado_hasta - ahora_login)
            st.error(f"Acceso bloqueado temporalmente ({restante}s restantes).")
            st.stop()

        pwd = st.text_input("Contrasena Maestra", type="password", placeholder="••••••••••••")
        if st.button("ACCEDER AL PANEL", use_container_width=True):
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
                    st.error(f"Contrasena incorrecta ({rest} intentos restantes).")
    st.stop()

# ------------------------------------------------------------------------------
# SERVICIO CRIPTOGRÁFICO Y FIREBASE
# ------------------------------------------------------------------------------
def obtener_token_firebase():
    """Obtiene el token de autenticacion para Firebase RTDB."""
    try:
        if hasattr(st, "secrets"):
            if "BORA_FIREBASE_AUTH" in st.secrets:
                return str(st.secrets["BORA_FIREBASE_AUTH"]).strip()
            if "BORA_FIREBASE_SECRET" in st.secrets:
                return str(st.secrets["BORA_FIREBASE_SECRET"]).strip()
    except Exception:
        pass

    token = os.environ.get("BORA_FIREBASE_AUTH", os.environ.get("BORA_FIREBASE_SECRET", "")).strip()
    if token:
        return token

    candidatos = [
        "admin_secret.txt",
        "firebase_secret.key",
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "admin_secret.txt"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "firebase_secret.key"),
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "admin_secret.txt"),
    ]
    for f_sec in candidatos:
        if f_sec and os.path.isfile(f_sec):
            try:
                with open(f_sec, "r", encoding="utf-8") as _f:
                    t = _f.read().strip()
                    if t: return t
            except Exception:
                pass

    return FIREBASE_SECRET_DEFAULT


def peticion_firebase(metodo, ruta, datos=None, timeout=8):
    """Realiza peticiones REST autenticadas a Firebase Realtime Database."""
    base = FIREBASE_URL.rstrip('/')
    url = f"{base}/{ruta}.json"
    token = obtener_token_firebase()
    if token:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}auth={token}"

    body = json.dumps(datos).encode("utf-8") if datos is not None else None
    req = urllib.request.Request(url, data=body, method=metodo, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as he:
        msg_err = f"Firebase HTTP {he.code}: {he.reason}"
        st.session_state["ultimo_error_firebase"] = msg_err
        raise RuntimeError(msg_err) from he
    except Exception as e:
        st.session_state["ultimo_error_firebase"] = str(e)
        raise e


def generar_clave_firmada_universal(hwid_cliente, dias_vigencia=30):
    """Genera clave en Formato Universal de 4 Bloques (XXXX-XXXX-XXXX-XXXX)."""
    hwid_limpio = hwid_cliente.strip().upper()
    dia_actual_utc = int(time.time() // 86400)
    dia_vencimiento = dia_actual_utc + int(dias_vigencia)
    offset_dias = max(1, min(65535, dia_vencimiento - EPOCA_BASE_DIAS))
    hex_vencimiento = f"{offset_dias:04X}"
    hex_salt = f"{int(time.time() * 10) & 0xFFFF:04X}"

    mensaje = f"{hwid_limpio}|{hex_vencimiento}|{hex_salt}".encode("utf-8")
    firma = hmac.new(SECRETO_MAESTRO_BORA, mensaje, hashlib.sha256).hexdigest().upper()
    clave_4b = f"{hex_vencimiento}-{hex_salt}-{firma[0:4]}-{firma[4:8]}"
    return clave_4b, dia_vencimiento


def generar_clave_firmada_v3(hwid_cliente, dias_vigencia=30, producto="NEST"):
    """Genera clave en Formato V3 de 5 Bloques (PROD-XXXX-XXXX-XXXX-XXXX)."""
    hwid_limpio = hwid_cliente.strip().upper()
    dia_actual_utc = int(time.time() // 86400)
    dia_vencimiento = dia_actual_utc + int(dias_vigencia)
    offset_dias = max(1, min(65535, dia_vencimiento - EPOCA_BASE_DIAS))
    hex_vencimiento = f"{offset_dias:04X}"
    hex_salt = f"{int(time.time() * 10) & 0xFFFF:04X}"
    prod = str(producto or "NEST").strip().upper()

    mensaje = f"{prod}|{hwid_limpio}|{hex_vencimiento}|{hex_salt}".encode("utf-8")
    firma = hmac.new(SECRETO_MAESTRO_BORA, mensaje, hashlib.sha256).hexdigest().upper()
    clave_5b = f"{prod}-{hex_vencimiento}-{hex_salt}-{firma[0:4]}-{firma[4:8]}"
    return clave_5b, dia_vencimiento


def extraer_dia_vencimiento_de_clave(clave_str):
    """Extrae el dia de vencimiento de una clave."""
    try:
        partes = str(clave_str).strip().upper().split("-")
        if len(partes) == 5 and len(partes[1]) == 4:
            return EPOCA_BASE_DIAS + int(partes[1], 16)
        if len(partes) == 4 and len(partes[0]) == 4:
            return EPOCA_BASE_DIAS + int(partes[0], 16)
    except Exception:
        pass
    return 0


def detectar_formato_clave(clave_str):
    """Detecta si una clave es 4b o 5b."""
    partes = str(clave_str or "").strip().upper().split("-")
    return "5b" if len(partes) == 5 else "4b"


def detectar_producto_de_equipo_o_clave(info_equipo):
    """Detecta el modulo de software."""
    if isinstance(info_equipo, dict):
        p = str(info_equipo.get("producto") or "").strip().upper()
        if p in ("NEST", "REST", "BORA", "SUITE"): return p
        c = str(info_equipo.get("clave") or "").strip().upper()
        if c.startswith("REST-"): return "REST"
        if c.startswith("NEST-"): return "NEST"
        if c.startswith("BORA-") or c.startswith("SUITE-"): return "BORA"
    return "NEST"


def redactar_mensaje_whatsapp(destinatario, dias_rest, pc_nom, hwid, clave_activa=""):
    """Genera mensaje formal de renovacion para WhatsApp (Sin emojis)."""
    saludo = f"Hola, {destinatario}." if destinatario else "Hola."
    estado = f"vence en {dias_rest} dia(s)" if dias_rest > 0 else "se encuentra actualmente VENCIDA"
    equipo_info = f" ({pc_nom})" if pc_nom else f" ({hwid})"
    
    bloque_clave = ""
    if clave_activa and clave_activa != "---":
        bloque_clave = f"\n\nClave de Activacion Oficial:\n{clave_activa}\n(Copiala y pegala en la ventana de Bora Design en tu CorelDRAW)"

    return (
        f"{saludo}\n\n"
        f"Te saludamos del equipo de soporte de Bora Design.\n"
        f"Te confirmamos que tu licencia de Bora Design NestPro{equipo_info} {estado}.{bloque_clave}\n\n"
        f"Cualquier duda con tu optimizacion de tela, estamos a tu orden de inmediato.\n\n"
        f"Muchas gracias por confiar en Bora Design."
    )

# ------------------------------------------------------------------------------
# SINCRONIZACIÓN DE DATOS
# ------------------------------------------------------------------------------
try:
    raw_equipos = peticion_firebase("GET", "equipos") or {}
    equipos_data = raw_equipos if isinstance(raw_equipos, dict) else {}
    sync_ok = True
except Exception as e:
    equipos_data = {}
    sync_ok = False
    st.sidebar.error(f"Error Firebase: {e}")

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
# HEADER PRINCIPAL INTEGRADO (LOGO PROPORCIONADO + CONTROLES RAPIDOS)
# ------------------------------------------------------------------------------
st.markdown(f"""
    <div class="bora-topbar">
        <div class="bora-brand-wrapper">
            <img src="data:image/png;base64,{LOGO_BORA_BASE64}" class="bora-main-logo" alt="Bora Design" />
            <span class="bora-cloud-pill">FLEET CLOUD</span>
        </div>
        <div class="bora-status-wrapper">
            <span class="bora-pulse-dot"></span>
            <span>{online_pcs} Online</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# Controles de sesion adaptables (50% / 50%)
c_btn_ref, c_btn_exit = st.columns(2)
with c_btn_ref:
    if st.button("Actualizar Sala", key="top_btn_ref", use_container_width=True):
        st.rerun()
with c_btn_exit:
    if st.button("Cerrar Sesion", key="top_btn_exit", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()

# ------------------------------------------------------------------------------
# RESUMEN DE SALA (4 MINI-TILES COMPACTOS)
# ------------------------------------------------------------------------------
st.markdown(f"""
    <div class="fleet-kpi-grid">
        <div class="fleet-kpi-card" style="border-left: 3px solid #38BDF8;">
            <div class="kpi-lbl">Equipos Total</div>
            <div class="kpi-val" style="color: #38BDF8;">{total_pcs}</div>
        </div>
        <div class="fleet-kpi-card" style="border-left: 3px solid #10B981;">
            <div class="kpi-lbl">Activas</div>
            <div class="kpi-val" style="color: #34D399;">{activas_pcs}</div>
        </div>
        <div class="fleet-kpi-card" style="border-left: 3px solid #6366F1;">
            <div class="kpi-lbl">En Linea</div>
            <div class="kpi-val" style="color: #818CF8;">{online_pcs}</div>
        </div>
        <div class="fleet-kpi-card" style="border-left: 3px solid #F59E0B;">
            <div class="kpi-lbl">Por Vencer</div>
            <div class="kpi-val" style="color: #FBBF24;">{atencion_pcs}</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# PESTAÑAS PRINCIPALES DEL DASHBOARD (SIN EMOJIS, CON SCROLL MÓVIL)
# ------------------------------------------------------------------------------
tab_equipos, tab_activar, tab_catalogo, tab_metricas, tab_avisos, tab_seguridad, tab_ota = st.tabs([
    "Equipos",
    "Activar",
    "Catalogo",
    "Metricas",
    "Difusion",
    "Seguridad",
    "OTA"
])

todos_talleres = sorted(list({
    str(v.get("taller", "")).strip() for v in equipos_data.values()
    if isinstance(v, dict) and str(v.get("taller", "")).strip() and str(v.get("taller", "")).strip() != "Sin asignar"
} | set(PRESETS_ETIQUETAS)))

# ==============================================================================
# TAB 1: FLEET ASSETS (TARJETAS DE EQUIPOS ULTRA-COMPACTAS Y RESPONSIVAS)
# ==============================================================================
with tab_equipos:
    # Barra de busqueda y filtro de taller en columnas adaptables
    col_f1, col_f2 = st.columns([1.6, 1.2])
    with col_f1:
        busqueda_txt = st.text_input("Buscar", placeholder="Buscar por HWID, Taller, Operador, PC...", label_visibility="collapsed").strip().lower()
    with col_f2:
        filtro_taller = st.selectbox(
            "Taller",
            ["Todos los Talleres"] + todos_talleres + ["Sin asignar"],
            label_visibility="collapsed"
        )

    # Selector de estado compacto
    filtro_estado = st.selectbox(
        "Filtro Estado:",
        ["Todos los Estados", "Online", "Por Vencer (<=5d)", "Pausadas / Vencidas"],
        index=0,
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

        if filtro_estado == "Online" and not en_linea:
            continue
        elif filtro_estado == "Por Vencer (<=5d)" and not (not bloqueado and 0 < dias_rest <= 5):
            continue
        elif filtro_estado == "Pausadas / Vencidas" and not (bloqueado or dias_rest == 0):
            continue

        if filtro_taller != "Todos los Talleres":
            if filtro_taller == "Sin asignar" and taller != "Sin asignar":
                continue
            elif filtro_taller != "Sin asignar" and taller.lower() != filtro_taller.lower():
                continue

        equipos_filtrados[hwid] = info

    if not equipos_filtrados:
        st.info("No se encontraron equipos bajo estos filtros.")
    else:
        st.caption(f"Mostrando {len(equipos_filtrados)} de {total_pcs} licencias registradas.")

        for hwid, info in equipos_filtrados.items():
            taller = str(info.get("taller", "")).strip() or "Sin asignar"
            cliente = str(info.get("cliente", "")).strip() or "Sin asignar"
            pc = info.get("pc_nombre", "PC")
            usuario_win = info.get("usuario_pc", "")
            bloqueado = bool(info.get("bloqueado", False))
            dia_venc = int(info.get("dia_vencimiento", 0))
            clave_act = info.get("clave", "---") or "---"
            ultimo_ts = int(info.get("ultimo_ping", 0))
            prod_nom = detectar_producto_de_equipo_o_clave(info)
            formato_actual = detectar_formato_clave(clave_act)

            en_linea = (ahora_ts - ultimo_ts) <= 75 if ultimo_ts > 0 else False
            dias_rest = max(0, dia_venc - dia_hoy) if dia_venc > 0 else 0

            if bloqueado:
                card_cls = "bloqueada"
                badge_lic = "<span style='font-size: 0.70rem; font-weight: 700; background: rgba(244,63,94,0.15); color: #FDA4AF; border: 1px solid rgba(244,63,94,0.3); padding: 2px 7px; border-radius: 6px;'>PAUSADA</span>"
                vig_txt = f"<span style='color: #FDA4AF; font-weight: 700;'>Suspendida</span>"
            elif dias_rest > 0:
                card_cls = "activa"
                col_c = "#34D399" if dias_rest > 5 else "#FBBF24"
                badge_lic = f"<span style='font-size: 0.70rem; font-weight: 700; background: rgba(16,185,129,0.15); color: #34D399; border: 1px solid rgba(16,185,129,0.3); padding: 2px 7px; border-radius: 6px;'>ACTIVA</span>"
                vig_txt = f"<span style='color: {col_c}; font-weight: 700;'>{dias_rest} dia(s)</span>"
            else:
                card_cls = "vencida"
                badge_lic = "<span style='font-size: 0.70rem; font-weight: 700; background: rgba(245,158,11,0.15); color: #FBBF24; border: 1px solid rgba(245,158,11,0.3); padding: 2px 7px; border-radius: 6px;'>VENCIDA</span>"
                vig_txt = "<span style='color: #FBBF24; font-weight: 700;'>0 dias (Vencida)</span>"

            badge_online = "<span style='font-size: 0.70rem; font-weight: 700; background: rgba(16,185,129,0.12); color: #34D399; padding: 2px 7px; border-radius: 6px;'>ON</span>" if en_linea else "<span style='font-size: 0.70rem; font-weight: 700; background: rgba(100,116,139,0.15); color: #94A3B8; padding: 2px 7px; border-radius: 6px;'>OFF</span>"
            tag_formato = "<span style='font-size: 0.65rem; color: #34D399; background: #064E3B; padding: 2px 6px; border-radius: 4px; white-space: nowrap;'>4B Universal</span>" if formato_actual == "4b" else "<span style='font-size: 0.65rem; color: #60A5FA; background: #1E3A8A; padding: 2px 6px; border-radius: 4px; white-space: nowrap;'>5B Suite</span>"

            st.markdown(f"""
                <div class="asset-card {card_cls}">
                    <div class="asset-top">
                        <div class="asset-id-group">
                            <span class="prod-tag">{prod_nom}</span>
                            <span class="asset-name">{cliente}</span>
                            <span class="taller-pill">{taller}</span>
                        </div>
                        <div style="display: flex; gap: 5px; align-items: center;">
                            {badge_online}
                            {badge_lic}
                        </div>
                    </div>
                    <div class="asset-meta-row">
                        <span>{pc}</span> {f'({usuario_win})' if usuario_win else ''} • {vig_txt}
                    </div>
                    <div class="mono-pill-box">
                        <span style="color: #64748B; font-size: 0.68rem; font-weight: 700;">HWID</span>
                        <span style="color: #38BDF8; font-weight: 700;">{hwid}</span>
                    </div>
                    <div class="mono-pill-box">
                        <span style="color: #64748B; font-size: 0.68rem; font-weight: 700;">CLAVE</span>
                        <span style="color: #34D399; font-weight: 800;">{clave_act}</span>
                        {tag_formato}
                    </div>
                </div>
            """, unsafe_allow_html=True)

            # ACCIONES EN 2 FILAS LIMPIAS (2x2 GRID RESPONSIVO): CERO DESBORDES EN MÓVILES
            c_r1_1, c_r1_2 = st.columns(2)
            with c_r1_1:
                if st.button("+30 Dias", key=f"btn_30_{hwid}", use_container_width=True):
                    try:
                        dia_base = max(dia_hoy, dia_venc)
                        total_nuevos = (dia_base - dia_hoy) + 30
                        nueva_cl, nuevo_venc = generar_clave_firmada_universal(hwid, total_nuevos)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": nueva_cl,
                            "producto": prod_nom,
                            "dia_vencimiento": nuevo_venc,
                            "bloqueado": False,
                            "clave_bloqueada": ""
                        })
                        st.toast(f"+30 dias aplicados a {cliente}")
                        time.sleep(0.4)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

            with c_r1_2:
                dest_nombre = cliente if cliente != "Sin asignar" else taller
                msg_wsp = redactar_mensaje_whatsapp(dest_nombre, dias_rest, pc, hwid, clave_act)
                msg_enc = urllib.parse.quote(msg_wsp)
                link_wsp = f"https://api.whatsapp.com/send?text={msg_enc}"
                st.markdown(f"""
                    <a href="{link_wsp}" target="_blank" style="text-decoration: none; display: block; width: 100%;">
                        <button style="width: 100%; min-height: 42px; background: #064E3B; color: #34D399; font-weight: 700; font-size: 0.82rem; border: 1px solid #059669; border-radius: 8px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 6px; box-sizing: border-box;">
                            {ICONS['whatsapp']} WhatsApp
                        </button>
                    </a>
                """, unsafe_allow_html=True)

            c_r2_1, c_r2_2 = st.columns([1.3, 0.7])
            with c_r2_1:
                if st.button("Clave 4B Universal", key=f"c4b_{hwid}", help="Regenera clave Universal de 4 bloques compatible con todas las versiones", use_container_width=True):
                    try:
                        dias_fijos = max(3, dias_rest if dias_rest > 0 else 30)
                        nueva_cl_4b, nuevo_venc_4b = generar_clave_firmada_universal(hwid, dias_fijos)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": nueva_cl_4b,
                            "producto": prod_nom,
                            "dia_vencimiento": nuevo_venc_4b,
                            "bloqueado": False,
                            "clave_bloqueada": ""
                        })
                        st.toast(f"Clave 4B Universal: {nueva_cl_4b}")
                        time.sleep(0.4)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

            with c_r2_2:
                with st.popover("Ajustes", use_container_width=True):
                    st.write(f"**Gestion:** `{cliente}`")
                    ed_tal = st.text_input("Taller:", value="" if taller == "Sin asignar" else taller, key=f"t_{hwid}")
                    ed_cli = st.text_input("Operador:", value="" if cliente == "Sin asignar" else cliente, key=f"c_{hwid}")
                    if st.button("Guardar Datos", key=f"sv_{hwid}", use_container_width=True):
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "taller": ed_tal.strip() or "Sin asignar",
                            "cliente": ed_cli.strip() or "Sin asignar"
                        })
                        st.rerun()

                    st.divider()
                    if bloqueado:
                        if st.button("Reactivar", key=f"unb_{hwid}", use_container_width=True):
                            v_rest = dia_venc if dia_venc > dia_hoy else (extraer_dia_vencimiento_de_clave(clave_act) if clave_act != "---" else 0)
                            if v_rest <= dia_hoy:
                                cl_n, v_n = generar_clave_firmada_universal(hwid, 30)
                                peticion_firebase("PATCH", f"equipos/{hwid}", {"bloqueado": False, "clave_bloqueada": "", "clave": cl_n, "dia_vencimiento": v_n})
                            else:
                                peticion_firebase("PATCH", f"equipos/{hwid}", {"bloqueado": False, "clave_bloqueada": "", "dia_vencimiento": v_rest})
                            st.rerun()
                    else:
                        if st.button("Suspender", key=f"blk_{hwid}", use_container_width=True):
                            peticion_firebase("PATCH", f"equipos/{hwid}", {"bloqueado": True, "clave_bloqueada": clave_act})
                            st.rerun()

                    st.divider()
                    d_fij = st.number_input("Dias Exactos:", min_value=1, max_value=365, value=30, key=f"df_{hwid}")
                    if st.button("Aplicar Dias", key=f"bdf_{hwid}", use_container_width=True):
                        cl_f, v_f = generar_clave_firmada_universal(hwid, d_fij)
                        peticion_firebase("PATCH", f"equipos/{hwid}", {
                            "clave": cl_f, "dia_vencimiento": v_f, "bloqueado": False, "clave_bloqueada": ""
                        })
                        st.rerun()

                    st.divider()
                    if st.button("Eliminar Asiento", key=f"del_{hwid}", use_container_width=True):
                        peticion_firebase("DELETE", f"equipos/{hwid}")
                        st.rerun()

            st.write("")

# ==============================================================================
# TAB 2: ACTIVADOR Y GENERADOR DE LICENCIAS
# ==============================================================================
with tab_activar:
    st.markdown("#### Activador de Licencias y Sincronizacion Cloud")
    st.markdown("Genera credenciales criptograficas universales compatibles con CorelDRAW y actualiza Firebase al instante.")

    col_ac1, col_ac2 = st.columns([1.2, 1.2])

    with col_ac1:
        sel_prod_reg = st.selectbox(
            "Modulo de Software:",
            ["NestPro (Industrial 2D)", "RestoPro (Patronaje)", "Suite Bora Completa"],
            index=0
        )
        nuevo_hwid = st.text_input("Hardware ID (HWID):", placeholder="BORA-XXXX-XXXX-XXXX").strip().upper()

        sel_tal = st.selectbox("Taller:", PRESETS_ETIQUETAS + ["Personalizado", "Sin asignar"])
        in_tal = st.text_input("Nombre Taller:") if sel_tal == "Personalizado" else sel_tal
        in_cli = st.text_input("Operador / Disenador:", placeholder="Ej: Manuel Monroy...").strip()

    with col_ac2:
        tipo_formato = st.radio(
            "Formato de Clave:",
            [
                "Universal (4 Bloques: XXXX-XXXX-XXXX-XXXX) [RECOMENDADO]",
                "Suite V3 (5 Bloques: NEST-XXXX-XXXX-XXXX-XXXX)"
            ],
            index=0
        )

        dias_reg = st.number_input("Dias de Vigencia:", min_value=1, max_value=730, value=30)
        st.write("Presets Rapidos:")
        cd1, cd2, cd3, cd4 = st.columns(4)
        with cd1:
            if st.button("7d Demo"): dias_reg = 7
        with cd2:
            if st.button("15d"): dias_reg = 15
        with cd3:
            if st.button("30d"): dias_reg = 30
        with cd4:
            if st.button("365d"): dias_reg = 365

        auto_nube = st.checkbox("Activar de inmediato en Firebase Cloud", value=True)

    st.markdown("---")
    if st.button("GENERAR LICENCIA Y REGISTRAR EN NUBE", use_container_width=True):
        if not nuevo_hwid.startswith("BORA-") or len(nuevo_hwid) < 15:
            st.error("Error: HWID invalido. Debe comenzar por 'BORA-' (Ej: BORA-FBD1-BB9B-E6C1).")
        else:
            try:
                prod_cod = "NEST" if "NestPro" in sel_prod_reg else ("REST" if "RestoPro" in sel_prod_reg else "BORA")
                es_universal = "Universal" in tipo_formato

                if es_universal:
                    cl_generada, venc_ts = generar_clave_firmada_universal(nuevo_hwid, int(dias_reg))
                else:
                    cl_generada, venc_ts = generar_clave_firmada_v3(nuevo_hwid, int(dias_reg), producto=prod_cod)

                if auto_nube:
                    peticion_firebase("PATCH", f"equipos/{nuevo_hwid}", {
                        "taller": in_tal or "Sin asignar",
                        "cliente": in_cli or "Sin asignar",
                        "producto": prod_cod,
                        "clave": cl_generada,
                        "dia_vencimiento": venc_ts,
                        "bloqueado": False,
                        "clave_bloqueada": "",
                        "fecha_registro": int(time.time())
                    })

                fecha_venc_str = datetime.datetime.fromtimestamp(venc_ts * 86400).strftime("%d/%m/%Y")
                st.success(f"Licencia generada con exito para {in_cli or nuevo_hwid}. Vence el {fecha_venc_str} ({dias_reg} dias).")

                st.markdown(f"""
                    <div style="background: #090D15; border: 1px solid #10B981; border-radius: 12px; padding: 14px; margin: 12px 0;">
                        <div style="font-size: 0.70rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px;">CLAVE OFICIAL GENERADA:</div>
                        <div style="font-family: 'JetBrains Mono', Consolas, monospace; font-size: 1.25rem; font-weight: 800; color: #34D399; letter-spacing: 0.06em; word-break: break-all;">
                            {cl_generada}
                        </div>
                    </div>
                """, unsafe_allow_html=True)

                st.code(cl_generada, language="text")

                # WhatsApp directo
                msg_wsp = redactar_mensaje_whatsapp(in_cli, int(dias_reg), "PC", nuevo_hwid, cl_generada)
                link_wsp = f"https://api.whatsapp.com/send?text={urllib.parse.quote(msg_wsp)}"
                st.markdown(f"""
                    <a href="{link_wsp}" target="_blank" style="text-decoration: none; display: block; width: 100%;">
                        <button style="width: 100%; min-height: 42px; background: #064E3B; color: #34D399; font-weight: 700; font-size: 0.85rem; border: 1px solid #059669; border-radius: 8px; cursor: pointer; margin-top: 8px; display: flex; align-items: center; justify-content: center; gap: 6px;">
                            {ICONS['whatsapp']} Enviar Clave a WhatsApp del Cliente
                        </button>
                    </a>
                """, unsafe_allow_html=True)

            except Exception as e:
                st.error(f"Error durante la generacion: {e}")

# ==============================================================================
# TAB 3: CATÁLOGO E INVENTARIO GLOBAL
# ==============================================================================
with tab_catalogo:
    st.markdown("#### Catalogo Completo de Asientos")
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

        est_txt = "PAUSADA" if bloqueado else (f"ACTIVA ({dias_rest}d)" if dias_rest > 0 else "VENCIDA")

        filas_t.append({
            "HWID": hwid,
            "Taller": taller,
            "Usuario": cliente,
            "PC": pc,
            "Conexion": "Online" if en_linea else "Offline",
            "Estado": est_txt,
            "Dias": dias_rest,
            "Ultimo Ping": ult_ping_str,
            "Clave": clave_act
        })

    if filas_t:
        st.dataframe(filas_t, use_container_width=True, hide_index=True)
    else:
        st.info("No se registran datos en Firebase.")

# ==============================================================================
# TAB 4: MÉTRICAS Y TELEMETRÍA DE CORTE TEXTIL
# ==============================================================================
with tab_metricas:
    st.markdown("#### Analisis de Produccion Textil y Retorno de Inversion")
    st.markdown("Telemetria en tiempo real recibida directamente desde los talleres de corte.")

    tot_metros = 0.0
    tot_ahorro = 0.0
    tot_piezas = 0
    filas_tel = []

    for hw, v in equipos_data.items():
        if isinstance(v, dict):
            m = float(v.get("metros_procesados", 0.0))
            ah = float(v.get("metros_ahorrados", 0.0))
            pz = int(v.get("piezas_anidadas", 0))
            tot_metros += m
            tot_ahorro += ah
            tot_piezas += pz

            t_nom = v.get("taller", "Sin asignar")
            pc_nom = v.get("pc_nombre", "PC")
            ef_str = f"{float(v.get('ultimo_aprovechamiento', 0.0)):.1f}%" if v.get("ultimo_aprovechamiento") else "—"
            u_ts = int(v.get("ultimo_montaje_fecha", 0))
            u_str = datetime.datetime.fromtimestamp(u_ts).strftime("%d/%m %H:%M") if u_ts > 0 else "—"

            filas_tel.append({
                "Taller": t_nom,
                "Dispositivo": pc_nom,
                "HWID": hw,
                "Metros Cortados": f"{m:.2f} m",
                "Metros Ahorrados": f"{ah:.2f} m",
                "Prendas Anidadas": pz,
                "Eficiencia": ef_str,
                "Ultimo Montaje": u_str
            })

    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    with c_m1:
        st.metric("Metros Procesados", f"{tot_metros:.2f} m")
    with c_m2:
        st.metric("Metros Ahorrados", f"{tot_ahorro:.2f} m")
    with c_m3:
        st.metric("Prendas Montadas", f"{tot_piezas} uds")
    with c_m4:
        st.metric("Ahorro Estimado", f"${tot_ahorro * 3.0:.1f} USD")

    st.markdown("---")
    st.markdown("##### Detalle por Taller:")
    if filas_tel:
        st.dataframe(filas_tel, use_container_width=True, hide_index=True)
    else:
        st.info("Aun no se ha registrado telemetria de corte en los talleres.")

# ==============================================================================
# TAB 5: DIFUSIÓN COREL (BROADCAST)
# ==============================================================================
with tab_avisos:
    st.markdown("#### Transmisor de Comunicados a CorelDRAW")
    st.markdown("Emite ventanas emergentes oficiales que aparecen instantaneamente en la interfaz de los talleres.")

    try:
        an_actual = peticion_firebase("GET", "anuncios/general") or {}
    except Exception:
        an_actual = {}

    if an_actual.get("activo"):
        st.success(f"COMUNICADO ACTIVO EN LA NUBE:\n\n{an_actual.get('titulo', 'Aviso')}: {an_actual.get('mensaje', '')}")
        if st.button("RETIRAR COMUNICADO DE TODAS LAS PANTALLAS", use_container_width=True):
            peticion_firebase("PUT", "anuncios/general", {"activo": False, "mensaje": "", "fecha": int(time.time())})
            st.warning("El comunicado ha sido desactivado en la nube.")
            st.rerun()
    else:
        st.info("No hay comunicados activos en este momento.")

    with st.form("form_anuncio_central"):
        tit_an = st.text_input("Titulo del Comunicado:", value=an_actual.get("titulo", "Aviso de Bora Design"))
        msg_an = st.text_area("Cuerpo del Mensaje (se mostrara al iniciar CorelDRAW):", value=an_actual.get("mensaje", ""))
        
        if st.form_submit_button("TRANSMITIR A TODOS LOS TALLERES EN TIEMPO REAL", use_container_width=True):
            if msg_an.strip():
                ts = int(time.time())
                peticion_firebase("PUT", "anuncios/general", {
                    "activo": True,
                    "titulo": tit_an.strip(),
                    "mensaje": msg_an.strip(),
                    "fecha": ts,
                    "id": str(ts)
                })
                st.success("Comunicado emitido a todas las pantallas.")
                st.rerun()
            else:
                st.error("Por favor ingresa un mensaje valido.")

# ==============================================================================
# TAB 6: SEGURIDAD Y KILL-SWITCH
# ==============================================================================
with tab_seguridad:
    st.markdown("#### Centro de Control de Integridad y Kill-Switch")
    st.markdown("Monitorea intentos de alteracion de reloj y permite el corte inmediato de licencias.")

    try:
        alertas_data = peticion_firebase("GET", "alertas_seguridad") or {}
    except Exception:
        alertas_data = {}

    filas_al = []
    for k, v in alertas_data.items():
        if isinstance(v, dict):
            f_ts = int(v.get("fecha", 0))
            f_str = datetime.datetime.fromtimestamp(f_ts).strftime("%d/%m/%Y %H:%M") if f_ts > 0 else "—"
            filas_al.append({
                "Fecha": f_str,
                "Tipo de Alerta": v.get("tipo", "SEGURIDAD"),
                "HWID": v.get("hwid", k),
                "Dispositivo": v.get("pc_nombre", "PC"),
                "Operador": v.get("usuario_pc", "—"),
                "Detalle Tecnico": v.get("detalle", "—")
            })

    if filas_al:
        st.warning(f"{len(filas_al)} evento(s) de seguridad detectados:")
        st.dataframe(filas_al, use_container_width=True, hide_index=True)
        if st.button("Limpiar Bitacora de Alertas", use_container_width=True):
            peticion_firebase("DELETE", "alertas_seguridad")
            st.success("Historial depurado.")
            st.rerun()
    else:
        st.success("Estado Seguro: No se registran manipulaciones de reloj ni intentos de acceso no autorizados.")

    st.markdown("---")
    st.markdown("##### Kill-Switch de Emergencia por Dispositivo:")
    col_ks1, col_ks2 = st.columns(2)
    with col_ks1:
        opciones_hwid = list(equipos_data.keys())
        hwid_sel_ks = st.selectbox(
            "Seleccionar Asiento para Suspension Inmediata:",
            opciones_hwid,
            format_func=lambda h: f"{equipos_data[h].get('taller', 'Sin taller')} • {equipos_data[h].get('cliente', 'Usuario')} ({h})"
        )
    with col_ks2:
        info_ks = equipos_data.get(hwid_sel_ks, {})
        est_actual = "PAUSADA" if info_ks.get("bloqueado") else "AUTORIZADA"
        st.markdown(f"**Estado del Asiento:** `{est_actual}`")

        c_btn_b, c_btn_d = st.columns(2)
        with c_btn_b:
            if st.button("SUSPENDER ACCESO", use_container_width=True, disabled=bool(info_ks.get("bloqueado"))):
                peticion_firebase("PATCH", f"equipos/{hwid_sel_ks}", {
                    "bloqueado": True,
                    "clave_bloqueada": info_ks.get("clave", "")
                })
                st.error(f"Equipo {hwid_sel_ks} suspendido de inmediato.")
                st.rerun()
        with c_btn_d:
            if st.button("RESTAURAR ACCESO", use_container_width=True, disabled=not bool(info_ks.get("bloqueado"))):
                peticion_firebase("PATCH", f"equipos/{hwid_sel_ks}", {
                    "bloqueado": False,
                    "clave_bloqueada": ""
                })
                st.success(f"Equipo {hwid_sel_ks} restaurado.")
                st.rerun()

# ==============================================================================
# TAB 7: ACTUALIZACIONES OTA CLOUD
# ==============================================================================
with tab_ota:
    st.markdown("#### Servidor de Despliegue de Actualizaciones OTA")
    try:
        ota_act = peticion_firebase("GET", "actualizaciones/nestpro") or {}
    except Exception:
        ota_act = {}

    v_a = ota_act.get("version", "v4.6 Industrial Edition")
    b_a = ota_act.get("build", "2026102718")
    u_a = ota_act.get("url_descarga", "---")
    n_a = ota_act.get("novedades", "---")

    st.markdown(f"""
        <div class="asset-card activa" style="margin-bottom: 14px;">
            <div style="font-size: 0.70rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.06em;">VERSION OFICIAL DISTRIBUIDA:</div>
            <div style="font-size: 1.15rem; font-weight: 800; color: #34D399; margin: 2px 0;">{v_a} (Build {b_a})</div>
            <div style="font-size: 0.72rem; color: #38BDF8; word-break: break-all;">Google Drive: {u_a}</div>
            <div style="font-size: 0.76rem; color: #CBD5E1; margin-top: 4px;"><b>Novedades:</b> {n_a}</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("form_ota_pub"):
        co1, co2 = st.columns(2)
        with co1:
            nv_v = st.text_input("Version Comercial:", value=v_a)
            nv_b = st.number_input("Numero de Build:", value=int(b_a) if str(b_a).isdigit() else 2026102718)
        with co2:
            nv_u = st.text_input("Enlace Google Drive del .exe:", value=u_a)
            nv_n = st.text_area("Registro de Cambios:", value=n_a)

        if st.form_submit_button("PUBLICAR ACTUALIZACION EN FIREBASE", use_container_width=True):
            if nv_v and nv_u:
                peticion_firebase("PATCH", "actualizaciones/nestpro", {
                    "version": nv_v.strip(),
                    "build": int(nv_b),
                    "url_descarga": nv_u.strip(),
                    "novedades": nv_n.strip(),
                    "fecha_publicacion": int(time.time()),
                    "publicado_por": "Admin Web Fleet"
                })
                st.success("Nueva version publicada en Firebase Cloud.")
                st.rerun()
