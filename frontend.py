import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="NexusAI — Intelligent Knowledge Assistant",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --white:       #ffffff;
    --grey-50:     #f9fafb;
    --grey-100:    #f3f4f6;
    --grey-200:    #e5e7eb;
    --grey-300:    #d1d5db;
    --grey-400:    #9ca3af;
    --grey-500:    #6b7280;
    --grey-600:    #4b5563;
    --grey-700:    #374151;
    --grey-800:    #1f2937;
    --grey-900:    #111827;

    --blue-50:     #eff6ff;
    --blue-100:    #dbeafe;
    --blue-500:    #3b82f6;
    --blue-600:    #2563eb;
    --blue-700:    #1d4ed8;

    --green-50:    #f0fdf4;
    --green-500:   #22c55e;
    --green-600:   #16a34a;

    --accent:      #2563eb;
    --accent-light:#eff6ff;
    --accent-hover:#1d4ed8;

    --shadow-sm:   0 1px 2px rgba(0,0,0,0.05);
    --shadow-md:   0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -1px rgba(0,0,0,0.04);
    --shadow-lg:   0 10px 15px -3px rgba(0,0,0,0.07), 0 4px 6px -2px rgba(0,0,0,0.04);
    --shadow-xl:   0 20px 25px -5px rgba(0,0,0,0.08), 0 10px 10px -5px rgba(0,0,0,0.03);

    --radius-sm:   6px;
    --radius-md:   10px;
    --radius-lg:   16px;
    --radius-xl:   24px;
}

* { box-sizing: border-box; }

html, body, [class*="css"], .stApp {
    background-color: var(--grey-50) !important;
    color: var(--grey-900) !important;
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--white) !important;
    border-right: 1px solid var(--grey-200) !important;
    box-shadow: var(--shadow-md) !important;
}
[data-testid="stSidebar"] > div {
    padding: 0 !important;
}
[data-testid="stSidebar"] * {
    color: var(--grey-800) !important;
}

/* ══════════════════════════════════════
   MAIN LAYOUT
══════════════════════════════════════ */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ══════════════════════════════════════
   SIDEBAR COMPONENTS
══════════════════════════════════════ */
.sidebar-header {
    padding: 28px 24px 20px;
    border-bottom: 1px solid var(--grey-100);
    background: var(--white);
}
.brand-mark {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 4px;
}
.brand-icon {
    width: 34px; height: 34px;
    background: var(--accent);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    color: white;
    font-weight: 700;
    font-family: 'Space Grotesk', sans-serif;
    flex-shrink: 0;
}
.brand-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.1rem;
    color: var(--grey-900);
    letter-spacing: -0.3px;
}
.brand-tagline {
    font-size: 0.72rem;
    color: var(--grey-400);
    letter-spacing: 0.3px;
    padding-left: 44px;
}

.sidebar-section {
    padding: 20px 24px;
    border-bottom: 1px solid var(--grey-100);
}
.sidebar-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    color: var(--grey-400);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.user-chip {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: var(--grey-50);
    border: 1px solid var(--grey-200);
    border-radius: var(--radius-md);
}
.user-avatar {
    width: 30px; height: 30px;
    background: linear-gradient(135deg, var(--blue-500), var(--blue-700));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 700;
    font-size: 0.75rem;
    flex-shrink: 0;
}
.user-info-name {
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--grey-800);
}
.user-info-role {
    font-size: 0.65rem;
    color: var(--grey-400);
    margin-top: 1px;
}

.source-active-card {
    background: var(--blue-50);
    border: 1px solid var(--blue-100);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-md);
    padding: 12px 14px;
    margin-top: 10px;
}
.source-status {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 6px;
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--green-500);
    box-shadow: 0 0 0 2px rgba(34,197,94,0.2);
    animation: blink 2s infinite;
}
@keyframes blink {
    0%,100% { opacity: 1; }
    50%      { opacity: 0.4; }
}
.status-text {
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--green-600);
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.source-url {
    font-size: 0.72rem;
    color: var(--blue-600);
    word-break: break-all;
    line-height: 1.4;
}

.source-empty-card {
    background: var(--grey-50);
    border: 1px dashed var(--grey-300);
    border-radius: var(--radius-md);
    padding: 16px;
    text-align: center;
    margin-top: 10px;
}
.source-empty-text {
    font-size: 0.75rem;
    color: var(--grey-400);
    line-height: 1.5;
}

/* ══════════════════════════════════════
   TOP NAV BAR
══════════════════════════════════════ */
.top-nav {
    background: var(--white);
    border-bottom: 1px solid var(--grey-200);
    padding: 0 32px;
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    box-shadow: var(--shadow-sm);
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--grey-800);
}
.nav-mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.badge-website {
    background: var(--blue-50);
    color: var(--blue-600);
    border: 1px solid var(--blue-100);
}
.badge-general {
    background: var(--grey-100);
    color: var(--grey-600);
    border: 1px solid var(--grey-200);
}
.nav-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
}
.dot-blue  { background: var(--blue-500); }
.dot-grey  { background: var(--grey-400); }

/* ══════════════════════════════════════
   CHAT AREA
══════════════════════════════════════ */
.chat-wrapper {
    padding: 28px 32px;
    min-height: calc(100vh - 140px);
}
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 20px;
    max-width: 780px;
    margin: 0 auto;
}

/* User Message */
.msg-row-user {
    display: flex;
    justify-content: flex-end;
    align-items: flex-end;
    gap: 10px;
}
.msg-bubble-user {
    max-width: 68%;
    background: var(--accent);
    color: var(--white) !important;
    border-radius: 18px 18px 4px 18px;
    padding: 13px 18px;
    font-size: 0.9rem;
    line-height: 1.6;
    box-shadow: 0 4px 12px rgba(37,99,235,0.25);
}
.msg-meta-user {
    font-size: 0.62rem;
    color: rgba(255,255,255,0.7);
    margin-bottom: 5px;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* Bot Message */
.msg-row-bot {
    display: flex;
    justify-content: flex-start;
    align-items: flex-start;
    gap: 12px;
}
.bot-avatar {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, var(--grey-700), var(--grey-900));
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
    margin-top: 2px;
    box-shadow: var(--shadow-sm);
}
.msg-bubble-bot {
    max-width: 74%;
    background: var(--white);
    border: 1px solid var(--grey-200);
    border-radius: 4px 18px 18px 18px;
    padding: 13px 18px;
    font-size: 0.9rem;
    line-height: 1.7;
    color: var(--grey-800);
    box-shadow: var(--shadow-md);
}
.msg-meta-bot {
    font-size: 0.62rem;
    color: var(--grey-400);
    margin-bottom: 6px;
    font-weight: 500;
    letter-spacing: 0.3px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* Sources */
.sources-wrap {
    margin-top: 12px;
    padding-top: 10px;
    border-top: 1px solid var(--grey-100);
}
.sources-label {
    font-size: 0.62rem;
    font-weight: 600;
    color: var(--grey-400);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.source-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    margin: 3px 4px 0 0;
    padding: 4px 10px;
    background: var(--grey-50);
    border: 1px solid var(--grey-200);
    border-radius: 20px;
    font-size: 0.67rem;
    color: var(--grey-600);
    word-break: break-all;
    transition: all 0.15s;
}

/* ══════════════════════════════════════
   EMPTY STATE
══════════════════════════════════════ */
.empty-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px 20px;
    text-align: center;
}
.empty-graphic {
    width: 72px; height: 72px;
    background: var(--grey-100);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 32px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-md);
}
.empty-heading {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--grey-800);
    margin-bottom: 8px;
    letter-spacing: -0.3px;
}
.empty-body {
    font-size: 0.85rem;
    color: var(--grey-400);
    max-width: 340px;
    line-height: 1.6;
}
.suggestion-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    margin-top: 24px;
}
.chip {
    padding: 8px 16px;
    background: var(--white);
    border: 1px solid var(--grey-200);
    border-radius: 20px;
    font-size: 0.78rem;
    color: var(--grey-600);
    box-shadow: var(--shadow-sm);
}

/* ══════════════════════════════════════
   INPUT BAR
══════════════════════════════════════ */
.input-bar-wrap {
    background: var(--white);
    border-top: 1px solid var(--grey-200);
    padding: 16px 32px;
    position: sticky;
    bottom: 0;
}

/* ══════════════════════════════════════
   AUTH PAGE
══════════════════════════════════════ */
.auth-page {
    min-height: 100vh;
    background: var(--grey-50);
    display: flex;
    align-items: center;
    justify-content: center;
}
.auth-card {
    background: var(--white);
    border: 1px solid var(--grey-200);
    border-radius: var(--radius-xl);
    padding: 40px 44px;
    width: 100%;
    max-width: 440px;
    box-shadow: var(--shadow-xl);
}
.auth-logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 8px;
}
.auth-logo-icon {
    width: 42px; height: 42px;
    background: var(--accent);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 18px;
    color: white;
}
.auth-logo-name {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.4rem;
    color: var(--grey-900);
    letter-spacing: -0.5px;
}
.auth-subtitle {
    font-size: 0.82rem;
    color: var(--grey-400);
    margin-bottom: 28px;
    padding-left: 54px;
    margin-top: -2px;
}
.auth-divider {
    height: 1px;
    background: var(--grey-100);
    margin: 20px 0;
}
.form-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--grey-700);
    margin-bottom: 6px;
    display: block;
}

/* ══════════════════════════════════════
   STREAMLIT OVERRIDES
══════════════════════════════════════ */
.stTextInput > label { display: none !important; }
.stTextInput > div > div > input {
    background: var(--white) !important;
    border: 1.5px solid var(--grey-200) !important;
    border-radius: var(--radius-md) !important;
    color: var(--grey-900) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.88rem !important;
    padding: 10px 14px !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,0.1) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder {
    color: var(--grey-400) !important;
}

.stButton > button {
    background: var(--accent) !important;
    color: var(--white) !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 10px 20px !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 1px 3px rgba(37,99,235,0.3) !important;
    letter-spacing: 0.2px !important;
}
.stButton > button:hover {
    background: var(--accent-hover) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(37,99,235,0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary buttons */
div[data-testid="stSidebar"] .stButton > button {
    background: var(--grey-100) !important;
    color: var(--grey-700) !important;
    box-shadow: none !important;
    border: 1px solid var(--grey-200) !important;
    font-size: 0.78rem !important;
}
div[data-testid="stSidebar"] .stButton > button:hover {
    background: var(--grey-200) !important;
    transform: none !important;
    box-shadow: none !important;
}

.stTabs [data-baseweb="tab-list"] {
    background: var(--grey-100) !important;
    border-radius: var(--radius-md) !important;
    padding: 4px !important;
    gap: 2px !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--grey-500) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    border-radius: 6px !important;
    padding: 7px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: var(--white) !important;
    color: var(--grey-900) !important;
    font-weight: 600 !important;
    box-shadow: var(--shadow-sm) !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

.stAlert {
    border-radius: var(--radius-md) !important;
    font-size: 0.82rem !important;
}

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--grey-300); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: var(--grey-400); }

hr { border: none !important; border-top: 1px solid var(--grey-200) !important; margin: 12px 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ─────────────────────────────────────────
for key, val in {
    "logged_in": False, "user_id": None, "token": None,
    "username": "", "messages": [], "website_id": None, "website_url": None
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

def now_time():
    return datetime.now().strftime("%I:%M %p")

# ─── API Helper ────────────────────────────────────────────
def api_post(endpoint, data):
    try:
        r = requests.post(f"{API_URL}{endpoint}", json=data, timeout=120)
        return {"ok": r.status_code < 300, "data": r.json(), "status": r.status_code}
    except requests.exceptions.ConnectionError:
        return {"ok": False, "data": {"detail": "Server unreachable. Please start the FastAPI backend."}, "status": 0}
    except Exception as e:
        return {"ok": False, "data": {"detail": str(e)}, "status": 0}

# ════════════════════════════════════════════════════════════
#  AUTH PAGE
# ════════════════════════════════════════════════════════════
def auth_page():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("""
        <div style="padding: 2rem 0;">
            <div class="auth-logo">
                <div class="auth-logo-icon">N</div>
                <div class="auth-logo-name">NexusAI</div>
            </div>
            <div class="auth-subtitle">Intelligent Knowledge Assistant</div>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["Sign In", "Create Account"])

        with tab1:
            with st.form("login_form"):
                st.markdown('<span class="form-label">Username</span>', unsafe_allow_html=True)
                username = st.text_input("u", placeholder="Enter your username", label_visibility="collapsed")
                st.markdown('<span class="form-label" style="margin-top:12px;display:block">Password</span>', unsafe_allow_html=True)
                password = st.text_input("p", type="password", placeholder="Enter your password", label_visibility="collapsed")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                submit = st.form_submit_button("Sign In →")
            if submit:
                if not username or not password:
                    st.error("Please fill in all fields.")
                else:
                    with st.spinner("Authenticating..."):
                        res = api_post("/auth/login", {"email": username, "password": password})
                    if res["ok"]:
                        st.session_state.logged_in = True
                        st.session_state.user_id   = username
                        st.session_state.username  = username
                        st.session_state.token     = res["data"]["access_token"]
                        st.rerun()
                    else:
                        st.error(res['data'].get('detail', 'Authentication failed.'))

        with tab2:
            with st.form("register_form"):
                st.markdown('<span class="form-label">Full Name</span>', unsafe_allow_html=True)
                name = st.text_input("fn", placeholder="e.g. Ahmed Khan", label_visibility="collapsed")
                st.markdown('<span class="form-label" style="margin-top:12px;display:block">Username</span>', unsafe_allow_html=True)
                username_r = st.text_input("un", placeholder="Choose a username", label_visibility="collapsed")
                st.markdown('<span class="form-label" style="margin-top:12px;display:block">Password</span>', unsafe_allow_html=True)
                pass_r = st.text_input("pr", type="password", placeholder="Min. 6 characters", label_visibility="collapsed")
                st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
                submit_r = st.form_submit_button("Create Account →")
            if submit_r:
                if not name or not username_r or not pass_r:
                    st.error("Please fill in all fields.")
                elif len(pass_r) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    with st.spinner("Creating your account..."):
                        res = api_post("/auth/register", {"name": name, "email": username_r, "password": pass_r})
                    if res["ok"]:
                        st.success("Account created successfully. Please sign in.")
                    else:
                        st.error(res['data'].get('detail', 'Registration failed.'))

        st.markdown("""
        <div style="text-align:center; margin-top: 24px; padding: 16px;
                    background: var(--grey-50); border-radius: 10px;
                    border: 1px solid var(--grey-200);">
            <div style="font-size:0.72rem; color: var(--grey-400); line-height:1.6;">
                Powered by <strong style="color:var(--grey-600)">Gemini AI</strong> ·
                <strong style="color:var(--grey-600)">ChromaDB</strong> ·
                <strong style="color:var(--grey-600)">MongoDB</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
#  MAIN APP
# ════════════════════════════════════════════════════════════
def chat_page():
    initials = st.session_state.username[:2].upper() if st.session_state.username else "U"

    # ── SIDEBAR ──────────────────────────────────────────
    with st.sidebar:
        # Brand
        st.markdown(f"""
        <div class="sidebar-header">
            <div class="brand-mark">
                <div class="brand-icon">N</div>
                <div class="brand-name">NexusAI</div>
            </div>
            <div class="brand-tagline">Intelligent Knowledge Assistant</div>
        </div>
        """, unsafe_allow_html=True)

        # User info
        st.markdown(f"""
        <div class="sidebar-section">
            <div class="sidebar-label">👤 Account</div>
            <div class="user-chip">
                <div class="user-avatar">{initials}</div>
                <div>
                    <div class="user-info-name">{st.session_state.username}</div>
                    <div class="user-info-role">Standard User</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Knowledge source
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">🌐 Knowledge Source</div>', unsafe_allow_html=True)

        website_url = st.text_input(
            "website_url_input",
            placeholder="https://yourwebsite.com",
            label_visibility="collapsed"
        )

        if st.button("⚡  Index Website"):
            if not website_url:
                st.error("Please enter a URL.")
            elif not website_url.startswith(("http://", "https://")):
                st.error("URL must start with http:// or https://")
            else:
                with st.spinner("Indexing website content..."):
                    res = api_post("/website/add", {
                        "url": website_url,
                        "user_id": st.session_state.user_id
                    })
                if res["ok"]:
                    st.session_state.website_id  = res["data"]["website_id"]
                    st.session_state.website_url = website_url
                    st.session_state.messages    = []
                    st.success(f"Indexed {res['data']['pages_scraped']} pages successfully.")
                    st.rerun()
                else:
                    st.error(res['data'].get('detail', 'Indexing failed.'))

        if st.session_state.website_id:
            st.markdown(f"""
            <div class="source-active-card">
                <div class="source-status">
                    <div class="status-dot"></div>
                    <div class="status-text">Active Source</div>
                </div>
                <div class="source-url">{st.session_state.website_url}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Remove Source"):
                st.session_state.website_id  = None
                st.session_state.website_url = None
                st.session_state.messages    = []
                st.rerun()
        else:
            st.markdown("""
            <div class="source-empty-card">
                <div class="source-empty-text">
                    No source indexed.<br>Add a URL to enable website Q&A mode.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Actions
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-label">⚙ Actions</div>', unsafe_allow_html=True)
        if st.button("🗑  Clear Conversation"):
            st.session_state.messages = []
            st.rerun()
        if st.button("← Sign Out"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # Footer
        st.markdown("""
        <div style="padding: 16px 24px; margin-top: auto;">
            <div style="font-size:0.65rem; color: var(--grey-300); line-height:1.8;">
                <div style="font-weight:600; color:var(--grey-400); margin-bottom:4px;">NexusAI v1.0</div>
                Gemini · ChromaDB · MongoDB<br>
                FastAPI · Streamlit
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── TOP NAV ──────────────────────────────────────────
    if st.session_state.website_id:
        mode_badge = f'<span class="nav-mode-badge badge-website"><span class="nav-dot dot-blue"></span>Website Mode</span>'
        nav_title  = "Website Q&A"
    else:
        mode_badge = f'<span class="nav-mode-badge badge-general"><span class="nav-dot dot-grey"></span>General Mode</span>'
        nav_title  = "General Assistant"

    st.markdown(f"""
    <div class="top-nav">
        <div class="nav-title">{nav_title}</div>
        <div style="display:flex;align-items:center;gap:12px;">
            {mode_badge}
            <div style="font-size:0.72rem;color:var(--grey-400);">
                {len(st.session_state.messages) // 2} messages
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CHAT MESSAGES ─────────────────────────────────────
    st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

    if not st.session_state.messages:
        suggestions = (
            ["What services does this company offer?",
             "Who are the key team members?",
             "What are the pricing plans?",
             "How do I contact support?"]
            if st.session_state.website_id else
            ["How can AI help my business?",
             "What is RAG technology?",
             "Explain machine learning",
             "What is a vector database?"]
        )
        chips_html = "".join(f'<div class="chip">{s}</div>' for s in suggestions)
        st.markdown(f"""
        <div class="empty-wrap">
            <div class="empty-graphic">◈</div>
            <div class="empty-heading">How can I help you today?</div>
            <div class="empty-body">
                {"Ask questions about the indexed website content using AI-powered search."
                  if st.session_state.website_id else
                  "Start a conversation or index a website from the sidebar to enable knowledge base Q&A."}
            </div>
            <div class="suggestion-chips">{chips_html}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        html = '<div class="chat-container">'
        for msg in st.session_state.messages:
            t = msg.get("time", "")
            if msg["role"] == "user":
                html += f"""
                <div class="msg-row-user">
                    <div class="msg-bubble-user">
                        <div class="msg-meta-user">You · {t}</div>
                        {msg['content']}
                    </div>
                </div>"""
            else:
                src_html = ""
                if msg.get("sources"):
                    pills = "".join(f'<span class="source-pill">↗ {s}</span>' for s in msg["sources"])
                    src_html = f'<div class="sources-wrap"><div class="sources-label">Sources</div>{pills}</div>'
                mode_tag = ""
                if msg.get("mode") == "website":
                    mode_tag = '<span style="background:var(--blue-50);color:var(--blue-600);padding:1px 7px;border-radius:10px;font-size:0.6rem;font-weight:600;border:1px solid var(--blue-100);">RAG</span>'
                html += f"""
                <div class="msg-row-bot">
                    <div class="bot-avatar">◈</div>
                    <div class="msg-bubble-bot">
                        <div class="msg-meta-bot">NexusAI · {t} {mode_tag}</div>
                        {msg['content']}{src_html}
                    </div>
                </div>"""
        html += '</div>'
        st.markdown(html, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ── INPUT BAR ─────────────────────────────────────────
    st.markdown('<div class="input-bar-wrap">', unsafe_allow_html=True)
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input(
                "chat_input",
                placeholder="Ask a question..." if not st.session_state.website_id
                            else "Ask about the website content...",
                label_visibility="collapsed"
            )
        with col2:
            send = st.form_submit_button("Send →")
    st.markdown('</div>', unsafe_allow_html=True)

    if send and user_input.strip():
        st.session_state.messages.append({
            "role": "user", "content": user_input, "time": now_time()
        })
        with st.spinner("Generating response..."):
            payload = {"message": user_input, "user_id": st.session_state.user_id}
            if st.session_state.website_id:
                payload["website_id"] = st.session_state.website_id
            res = api_post("/chat/", payload)

        if res["ok"]:
            st.session_state.messages.append({
                "role":    "assistant",
                "content": res["data"]["response"],
                "sources": res["data"].get("sources", []),
                "mode":    res["data"]["mode"],
                "time":    now_time(),
            })
        else:
            st.session_state.messages.append({
                "role":    "assistant",
                "content": f"Error: {res['data'].get('detail', 'Something went wrong. Please try again.')}",
                "sources": [], "mode": "error", "time": now_time(),
            })
        st.rerun()

# ─── ROUTER ───────────────────────────────────────────────
if st.session_state.logged_in:
    chat_page()
else:
    auth_page()