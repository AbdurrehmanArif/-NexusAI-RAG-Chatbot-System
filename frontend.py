import streamlit as st
import requests
from datetime import datetime

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NexusAI", page_icon="⚡", layout="wide")

# -----------------------------
# Modern SaaS Dashboard Styling
# -----------------------------
st.markdown("""
<style>

/* App background */
.stApp{
background:#f8fafc;
color:#0f172a;
font-family:Inter, sans-serif;
}

#MainMenu, footer, header{visibility:hidden;}

/* Sidebar */
section[data-testid="stSidebar"]{
background:#ffffff;
border-right:1px solid #e2e8f0;
}

/* Buttons */
.stButton>button{
background:#4f46e5;
border:none;
color:white;
border-radius:8px;
padding:8px 16px;
font-weight:600;
}

.stButton>button:hover{
background:#4338ca;
}

/* Inputs */
.stTextInput input{
background:#ffffff;
border:1px solid #cbd5f5;
color:#0f172a;
border-radius:8px;
}

/* Chat bubbles */
.user-msg{
background:#4f46e5;
color:white;
padding:10px 14px;
border-radius:12px 12px 4px 12px;
margin:10px 0;
width:fit-content;
margin-left:auto;
max-width:60%;
}

.bot-msg{
background:#ffffff;
border:1px solid #e2e8f0;
padding:10px 14px;
border-radius:12px 12px 12px 4px;
margin:10px 0;
max-width:65%;
color:#0f172a;
}

.source-pill{
display:inline-block;
background:#f1f5f9;
border:1px solid #e2e8f0;
padding:3px 8px;
border-radius:6px;
font-size:11px;
margin-right:5px;
margin-top:6px;
}

.metric-card{
background:#ffffff;
padding:16px;
border-radius:12px;
border:1px solid #e2e8f0;
}

</style>
""", unsafe_allow_html=True)


# -----------------------------
# Session State
# -----------------------------

def init_state():

    defaults={
        "logged_in":False,
        "username":"",
        "messages":[],
        "website_id":None,
        "website_url":None
    }

    for k,v in defaults.items():
        if k not in st.session_state:
            st.session_state[k]=v

init_state()


# -----------------------------
# API Helper
# -----------------------------

def api_post(endpoint,data):

    try:
        r=requests.post(f"{API_URL}{endpoint}",json=data)
        return r.json(), r.status_code

    except:
        return {"detail":"Backend not reachable"},500


def ts():
    return datetime.now().strftime("%H:%M")


# -----------------------------
# Login Page
# -----------------------------

def login_page():

    col1,col2,col3 = st.columns([1,1,1])

    with col2:

        st.markdown("## ⚡ NexusAI")
        st.caption("Modern AI Knowledge Assistant")

        tab1,tab2 = st.tabs(["Login","Register"])

        with tab1:

            user=st.text_input("Username")
            pwd=st.text_input("Password",type="password")

            if st.button("Login",use_container_width=True):

                data,code = api_post("/auth/login",{
                    "email":user,
                    "password":pwd
                })

                if code<300:
                    st.session_state.logged_in=True
                    st.session_state.username=user
                    st.rerun()
                else:
                    st.error(data.get("detail","Login failed"))


        with tab2:

            name=st.text_input("Name")
            user=st.text_input("Username ")
            pwd=st.text_input("Password ",type="password")

            if st.button("Create Account",use_container_width=True):

                data,code=api_post("/auth/register",{
                    "name":name,
                    "email":user,
                    "password":pwd
                })

                if code<300:
                    st.success("Account created")
                else:
                    st.error(data.get("detail","Registration failed"))


# -----------------------------
# Sidebar
# -----------------------------

def sidebar():

    with st.sidebar:

        st.markdown("# ⚡ NexusAI")

        st.write(f"User: **{st.session_state.username}**")

        st.divider()

        st.markdown("### Knowledge Source")

        url = st.text_input("Website URL")

        if st.button("Index Website",use_container_width=True):

            if not url:
                st.warning("Enter URL")

            else:

                with st.spinner("Indexing website..."):

                    data,code=api_post("/website/add",{
                        "url":url,
                        "user_id":st.session_state.username
                    })

                if code<300:

                    st.session_state.website_id=data["website_id"]
                    st.session_state.website_url=url

                    st.success("Website indexed")

                else:
                    st.error(data.get("detail","Indexing failed"))


        if st.session_state.website_id:

            st.success("Website active")
            st.caption(st.session_state.website_url)

            if st.button("Remove Source",use_container_width=True):

                st.session_state.website_id=None
                st.session_state.website_url=None


        st.divider()

        if st.button("Clear Chat",use_container_width=True):
            st.session_state.messages=[]

        if st.button("Logout",use_container_width=True):

            for k in list(st.session_state.keys()):
                del st.session_state[k]

            st.rerun()


# -----------------------------
# Dashboard Header
# -----------------------------

def dashboard_header():

    st.markdown("## AI Assistant Dashboard")

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown("<div class='metric-card'><b>Messages</b><br>"+str(len(st.session_state.messages))+"</div>",unsafe_allow_html=True)

    with c2:
        mode = "Website RAG" if st.session_state.website_id else "General AI"
        st.markdown("<div class='metric-card'><b>Mode</b><br>"+mode+"</div>",unsafe_allow_html=True)

    with c3:
        src = st.session_state.website_url if st.session_state.website_url else "None"
        st.markdown("<div class='metric-card'><b>Source</b><br>"+src[:40]+"</div>",unsafe_allow_html=True)


# -----------------------------
# Chat Interface
# -----------------------------

def chat_interface():

    dashboard_header()

    st.divider()

    for m in st.session_state.messages:

        if m["role"]=="user":

            st.markdown(
                f"<div class='user-msg'>{m['content']}</div>",
                unsafe_allow_html=True
            )

        else:

            src_html=""

            if m.get("sources"):

                pills="".join(
                    f"<span class='source-pill'>{s}</span>"
                    for s in m["sources"]
                )

                src_html=f"<div>{pills}</div>"


            st.markdown(
                f"<div class='bot-msg'>{m['content']}{src_html}</div>",
                unsafe_allow_html=True
            )


    with st.form("chat",clear_on_submit=True):

        col1,col2 = st.columns([8,1])

        with col1:
            msg=st.text_input("Message")

        with col2:
            send=st.form_submit_button("Send")


    if send and msg:

        st.session_state.messages.append({
            "role":"user",
            "content":msg
        })

        payload={
            "message":msg,
            "user_id":st.session_state.username
        }

        if st.session_state.website_id:
            payload["website_id"] = st.session_state.website_id


        with st.spinner("Thinking..."):

            data,code = api_post("/chat/",payload)

        if code<300:

            st.session_state.messages.append({
                "role":"assistant",
                "content":data["response"],
                "sources":data.get("sources",[])
            })

        else:

            st.session_state.messages.append({
                "role":"assistant",
                "content":data.get("detail","Error")
            })

        st.rerun()


# -----------------------------
# Router
# -----------------------------

if st.session_state.logged_in:

    sidebar()

    chat_interface()

else:

    login_page()
