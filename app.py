import streamlit as st
import pandas as pd
import re
import json
import os

try:
    import plotly.graph_objects as go
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

DATA_FILE = "polls_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                return data.get("polls", []), data.get("next_poll_id", 1)
        except Exception:
            return [], 1
    return [], 1

def save_data(polls, next_id):
    with open(DATA_FILE, "w") as f:
        json.dump({"polls": polls, "next_poll_id": next_id}, f, indent=4)

# ----------------------------------------------------
# Page Configuration
# ----------------------------------------------------
st.set_page_config(
    page_title="Pollex | Jigyasa Poll",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ----------------------------------------------------
# Dense CSS styling for Dark SaaS Landing Page
# ----------------------------------------------------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
    
    /* Fade-in animation */
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .block-container { animation: fadeInUp 0.8s ease-in-out; }
    * { transition: all 0.3s ease-in-out; }
    
    /* Title glow animation */
    @keyframes glow {
        0% { text-shadow: 0 0 5px rgba(138,43,226,0.3); }
        50% { text-shadow: 0 0 20px rgba(138,43,226,0.8); }
        100% { text-shadow: 0 0 5px rgba(138,43,226,0.3); }
    }
    h1 { animation: glow 3s infinite !important; }
    
    /* Pulse animation */
    @keyframes pulse { 0% { opacity: 0.6; } 50% { opacity: 1; } 100% { opacity: 0.6; } }
    .live-pulse { animation: pulse 1.5s infinite; color: #ff4b4b !important; font-weight: bold; margin-bottom: -5px; font-size: 0.95rem; text-transform: uppercase; letter-spacing: 1px; display: inline-block; padding: 5px 15px; background: rgba(255, 75, 75, 0.1); border-radius: 20px; border: 1px solid rgba(255, 75, 75, 0.3); }

    
    /* CSS PARTICLES BACKGROUND */
    .particles-layer-1 { position: fixed; top: 0; left: 0; width: 3px; height: 3px; border-radius: 50%; background: transparent; box-shadow: 6vw 94vh 3px #10b981, 91vw 100vh 3px #ffffff, 22vw 16vh 3px #ffffff, 68vw 66vh 3px #8b5cf6, 35vw 85vh 3px #ffffff, 42vw 46vh 3px #8b5cf6, 63vw 64vh 3px #3b82f6, 66vw 73vh 3px #10b981, 34vw 89vh 3px #10b981, 51vw 15vh 3px #10b981, 63vw 52vh 3px #3b82f6, 3vw 53vh 3px #10b981, 36vw 67vh 3px #10b981, 92vw 33vh 3px #10b981, 45vw 43vh 3px #8b5cf6, 5vw 23vh 3px #3b82f6, 46vw 71vh 3px #10b981, 70vw 77vh 3px #8b5cf6, 80vw 64vh 3px #3b82f6, 80vw 57vh 3px #10b981, 4vw 46vh 3px #8b5cf6, 7vw 60vh 3px #3b82f6, 70vw 74vh 3px #ffffff, 66vw 21vh 3px #3b82f6, 71vw 33vh 3px #ffffff, 3vw 68vh 3px #3b82f6, 98vw 27vh 3px #3b82f6, 18vw 58vh 3px #ffffff, 35vw 94vh 3px #3b82f6, 25vw 78vh 3px #3b82f6, 66vw 96vh 3px #10b981, 7vw 90vh 3px #ffffff, 24vw 38vh 3px #3b82f6, 26vw 91vh 3px #8b5cf6, 77vw 45vh 3px #10b981, 40vw 35vh 3px #8b5cf6, 33vw 52vh 3px #8b5cf6, 27vw 59vh 3px #ffffff, 25vw 63vh 3px #ffffff, 70vw 68vh 3px #ffffff, 15vw 7vh 3px #10b981, 29vw 78vh 3px #10b981, 21vw 2vh 3px #10b981, 14vw 1vh 3px #10b981, 56vw 47vh 3px #ffffff, 94vw 44vh 3px #ffffff, 33vw 85vh 3px #3b82f6, 15vw 26vh 3px #3b82f6, 34vw 41vh 3px #10b981, 30vw 16vh 3px #3b82f6, 34vw 68vh 3px #3b82f6, 62vw 51vh 3px #10b981, 72vw 6vh 3px #ffffff, 40vw 43vh 3px #8b5cf6, 82vw 3vh 3px #10b981, 74vw 84vh 3px #8b5cf6, 44vw 33vh 3px #ffffff, 28vw 82vh 3px #10b981, 66vw 40vh 3px #10b981, 19vw 24vh 3px #8b5cf6; animation: animParticle 30s linear infinite; opacity: 1.0; pointer-events: none; z-index: 0; }
    .particles-layer-2 { position: fixed; top: 0; left: 0; width: 4px; height: 4px; border-radius: 50%; background: transparent; box-shadow: 22vw 65vh 3px #ffffff, 23vw 9vh 3px #ffffff, 15vw 78vh 3px #3b82f6, 24vw 74vh 3px #10b981, 62vw 31vh 3px #3b82f6, 66vw 27vh 3px #3b82f6, 28vw 76vh 3px #8b5cf6, 69vw 81vh 3px #8b5cf6, 19vw 96vh 3px #3b82f6, 12vw 38vh 3px #3b82f6, 93vw 63vh 3px #3b82f6, 43vw 70vh 3px #8b5cf6, 100vw 28vh 3px #8b5cf6, 42vw 95vh 3px #10b981, 58vw 3vh 3px #8b5cf6, 92vw 31vh 3px #8b5cf6, 76vw 97vh 3px #10b981, 15vw 45vh 3px #3b82f6, 15vw 2vh 3px #10b981, 86vw 41vh 3px #3b82f6, 14vw 2vh 3px #ffffff, 64vw 39vh 3px #ffffff, 5vw 42vh 3px #10b981, 75vw 10vh 3px #3b82f6, 82vw 89vh 3px #8b5cf6, 55vw 56vh 3px #8b5cf6, 37vw 99vh 3px #ffffff, 84vw 23vh 3px #10b981, 52vw 70vh 3px #10b981, 32vw 64vh 3px #10b981, 95vw 41vh 3px #8b5cf6, 32vw 84vh 3px #3b82f6, 83vw 39vh 3px #8b5cf6, 87vw 67vh 3px #ffffff, 33vw 99vh 3px #8b5cf6, 3vw 33vh 3px #ffffff, 89vw 100vh 3px #3b82f6, 99vw 68vh 3px #ffffff, 76vw 44vh 3px #8b5cf6, 57vw 62vh 3px #10b981; animation: animParticle 45s linear infinite; opacity: 0.8; pointer-events: none; z-index: 0; }
    .particles-layer-3 { position: fixed; top: 0; left: 0; width: 6px; height: 6px; border-radius: 50%; background: transparent; box-shadow: 28vw 4vh 3px #8b5cf6, 81vw 90vh 3px #ffffff, 80vw 50vh 3px #3b82f6, 37vw 10vh 3px #8b5cf6, 32vw 83vh 3px #ffffff, 67vw 70vh 3px #ffffff, 16vw 19vh 3px #3b82f6, 87vw 73vh 3px #ffffff, 93vw 32vh 3px #ffffff, 74vw 57vh 3px #10b981, 64vw 50vh 3px #8b5cf6, 14vw 99vh 3px #10b981, 4vw 17vh 3px #8b5cf6, 74vw 42vh 3px #3b82f6, 77vw 12vh 3px #3b82f6, 65vw 70vh 3px #3b82f6, 40vw 53vh 3px #8b5cf6, 37vw 65vh 3px #10b981, 2vw 76vh 3px #8b5cf6, 11vw 97vh 3px #8b5cf6, 39vw 35vh 3px #3b82f6, 9vw 46vh 3px #3b82f6, 27vw 70vh 3px #8b5cf6, 57vw 36vh 3px #10b981, 63vw 38vh 3px #8b5cf6, 48vw 83vh 3px #8b5cf6, 64vw 4vh 3px #ffffff, 22vw 47vh 3px #8b5cf6, 12vw 9vh 3px #ffffff, 70vw 71vh 3px #8b5cf6; animation: animParticle 60s linear infinite; opacity: 0.6; pointer-events: none; z-index: 0; }
    .particles-layer-1::after, .particles-layer-2::after, .particles-layer-3::after { content: ' '; position: absolute; top: 100vh; width: 100%; height: 100%; border-radius: 50%; background: transparent; box-shadow: inherit; }

    @keyframes animParticle { 0% { transform: translateY(0); } 100% { transform: translateY(-100vh); } }
/* Base typography and background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        background-color: #050505 !important;
        color: #f8fafc !important;
    }
    
    .stApp {
        background-color: #050505 !important;
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(67, 56, 202, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 90% 80%, rgba(124, 58, 237, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 50% 50%, rgba(20, 184, 166, 0.02) 0%, transparent 60%);
    }
    
    [data-testid="collapsedControl"], header, footer, #MainMenu, a.header-anchor { display: none !important; }
    
    .top-logo {
        font-weight: 800; font-size: 1.4rem; letter-spacing: -0.5px;
        background: linear-gradient(90deg, #c4b5fd, #e9d5ff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-top: 0rem; margin-bottom: 2rem; display: inline-block;
    }

    .hero-title {
        font-size: clamp(3rem, 5vw, 4.5rem); font-weight: 800; color: #ffffff;
        text-align: center; line-height: 1.1; letter-spacing: -2px;
        margin-top: 2rem; margin-bottom: 1.5rem;
    }

    .hero-subtitle {
        font-size: clamp(1rem, 2vw, 1.15rem); color: #94A3B8;
        text-align: center; font-weight: 500; max-width: 650px;
        margin: 0 auto 3rem auto; line-height: 1.6;
        animation: fadeUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
    }
    
    @keyframes fadeDown { 0% { opacity: 0; transform: translateY(-20px); filter: blur(5px); } 100% { opacity: 1; transform: translateY(0); filter: blur(0px); } }
    @keyframes fadeUp { 0% { opacity: 0; transform: translateY(20px); filter: blur(5px); } 100% { opacity: 1; transform: translateY(0); filter: blur(0px); } }
    
    .block-container { max-width: 950px !important; padding-top: 2rem !important; padding-bottom: 4rem !important; }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: linear-gradient(180deg, rgba(30, 27, 75, 0.3), rgba(15, 23, 42, 0.4)) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(139, 92, 246, 0.15) !important;
        border-top: 1px solid rgba(139, 92, 246, 0.3) !important;
        border-radius: 32px !important;
        box-shadow: 0 20px 40px rgba(0,0,0,0.5), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        padding: 2.5rem !important; transition: all 0.3s ease-in-out !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover { 
        border-color: rgba(167, 139, 250, 0.3) !important; transform: translateY(-5px) !important;
        box-shadow: 0px 10px 25px rgba(0,0,0,0.5) !important;
    }
    
    .stButton button { 
        border-radius: 25px !important; font-weight: 600 !important; font-size: 0.95rem !important; 
        padding: 0.7rem 2rem !important; transition: all 0.3s ease-in-out !important;
        letter-spacing: 0.3px; border: 1px solid transparent !important;
    }
    .stButton button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0px 0px 15px rgba(138, 43, 226, 0.6) !important;
    }
    
    .stButton button[kind^="primary"], [data-testid="stFormSubmitButton"] button { 
        background: linear-gradient(135deg, #6d28d9 0%, #4c1d95 100%) !important; color: #ffffff !important; 
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.4), inset 0 1px 0 rgba(255,255,255,0.2) !important; 
    }
    .stButton button[kind^="primary"]:hover, [data-testid="stFormSubmitButton"] button:hover { 
        transform: scale(1.05) !important; 
        box-shadow: 0px 0px 25px rgba(138, 43, 226, 0.8), inset 0 1px 0 rgba(255,255,255,0.3) !important;
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important; 
    }
    
    .stButton button[kind="secondary"] { 
        background-color: rgba(30, 41, 59, 0.4) !important; backdrop-filter: blur(8px) !important;
        color: #cbd5e1 !important; border-color: rgba(255, 255, 255, 0.08) !important; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.05) !important; 
    }
    .stButton button[kind="secondary"]:hover { 
        background-color: rgba(51, 65, 85, 0.6) !important; color: #ffffff !important; 
        border-color: rgba(138, 43, 226, 0.6) !important; transform: scale(1.05) !important;
        box-shadow: 0px 0px 15px rgba(138, 43, 226, 0.6) !important;
    }
    
    [data-testid="column"] .stButton button { width: 100% !important; }
    
    .stTextInput input, div[data-baseweb="select"] > div { 
        background-color: rgba(15, 23, 42, 0.6) !important; border: 1px solid rgba(148, 163, 184, 0.15) !important; 
        color: white !important; border-radius: 16px !important; padding: 0.8rem 1.2rem !important; 
        font-size: 1rem !important; transition: all 0.2s ease; box-shadow: inset 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    .stTextInput input:focus, div[data-baseweb="select"]:focus-within > div { 
        border-color: #8b5cf6 !important; box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2), inset 0 2px 4px rgba(0,0,0,0.2) !important; 
        background-color: rgba(30, 41, 59, 0.8) !important;
    }
    
    h1, h2, h3, h4, h5, h6 { color: #ffffff !important; font-weight: 700 !important; letter-spacing: -0.5px !important; }
    label { color: #94A3B8 !important; font-weight: 500 !important; font-size: 0.95rem !important; }
    p, li { color: #cbd5e1 !important; }

    .stRadio label { 
        display: flex; align-items: center; padding: 1.2rem 1.5rem; 
        border: 1px solid rgba(139, 92, 246, 0.15); border-radius: 16px; margin-bottom: 0.8rem; 
        transition: all 0.3s ease; background: rgba(15, 23, 42, 0.5); box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stRadio label:hover { 
        background: rgba(30, 41, 59, 0.8); border-color: rgba(167, 139, 250, 0.3);
        transform: translateX(4px) scale(1.01); box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    [data-testid="stExpander"] {
        background-color: rgba(15, 23, 42, 0.4) !important; border: 1px solid rgba(139, 92, 246, 0.15) !important;
        border-radius: 16px !important; overflow: hidden !important; transition: all 0.3s ease !important;
    }
    [data-testid="stExpander"]:hover { border-color: rgba(167, 139, 250, 0.3) !important; }
    [data-testid="stExpander"] summary { padding: 1.2rem !important; font-weight: 600 !important; color: #f8fafc !important; }
    [data-testid="stExpander"] summary:hover { background-color: rgba(30, 41, 59, 0.4) !important; }
    
    [data-testid="stDataFrame"] {
        border-radius: 12px !important; overflow: hidden !important; border: 1px solid rgba(139, 92, 246, 0.15) !important;
    }
    
    [data-testid="stAlert"] {
        background-color: rgba(15, 23, 42, 0.8) !important; border: 1px solid rgba(148, 163, 184, 0.15) !important;
        border-radius: 16px !important; padding: 1rem !important; color: #f8fafc !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.2) !important;
    }
    div.st-emotion-cache-121g3x8 { 
        border: 1px solid #10b981 !important;
        background: linear-gradient(90deg, rgba(16, 185, 129, 0.15), rgba(16, 185, 129, 0.02)) !important;
        border-left: 4px solid #10b981 !important;
    }
    div.st-emotion-cache-q251g2 { 
        border: 1px solid #ef4444 !important; background: rgba(239, 68, 68, 0.1) !important;
    }
    hr { border-color: rgba(255, 255, 255, 0.08) !important; }
</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Top Logo & Nav Setup
# ----------------------------------------------------
st.markdown("<div class='top-logo'>◱ Jigyasa Poll</div>", unsafe_allow_html=True)

st.markdown('<div class="particles-layer-1"></div><div class="particles-layer-2"></div><div class="particles-layer-3"></div>', unsafe_allow_html=True)

if 'data_loaded' not in st.session_state:
    st.session_state.polls, st.session_state.next_poll_id = load_data()
    st.session_state.data_loaded = True
    
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Cast Vote"

def nav_to(page_name):
    st.session_state.current_page = page_name

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email) is not None

st.markdown("<h1 class='hero-title'>Jigyasa Polling & Insights Platform</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; margin-bottom: 2rem;'><span class='live-pulse'>🔴 Live Poll Active</span></div>", unsafe_allow_html=True)
st.markdown("<div style='width: 100%; display: flex; justify-content: center;'><p class='hero-subtitle' style='text-align: center !important; margin: 0 auto;'>Make real-time, data-driven decisions for Jigyasa events.<br/>Collect votes, analyze preferences, and finalize outcomes with clarity.</p></div>", unsafe_allow_html=True)

# ----------------------------------------------------
# Bulletproof Pill Navbar (Fixed column width wrapping)
# ----------------------------------------------------
tabs = ["Cast Vote", "View Results", "Admin Dashboard"]
if st.session_state.is_admin:
    tabs.insert(2, "Workspace")

num_tabs = len(tabs)
if num_tabs == 3:
    cols = st.columns([0.5, 1.2, 1.2, 1.2, 0.5])
    active_cols = cols[1:4]
else:
    cols = st.columns([0.3, 1.2, 1.2, 1.2, 1.2, 0.3])
    active_cols = cols[1:5]

for i, tab in enumerate(tabs):
    with active_cols[i]:
        btn_type = "primary" if st.session_state.current_page == tab else "secondary"
        st.button(tab, key=f"nav_{tab}", on_click=nav_to, args=(tab,), use_container_width=True, type=btn_type)

st.write("")

# ----------------------------------------------------
# Helper Functions
# ----------------------------------------------------
def create_dark_metric(label, value, icon, bg_color, icon_color):
    """Generates a modern dark-theme metric card with CSS animations."""
    return f"""
    <div style='background: linear-gradient(145deg, rgba(30, 27, 75, 0.4), rgba(15, 23, 42, 0.8)); backdrop-filter: blur(12px); border: 1px solid rgba(139, 92, 246, 0.15); border-top: 1px solid rgba(139, 92, 246, 0.3); border-radius: 24px; padding: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05); display: flex; align-items: center; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);' onmouseover="this.style.transform='translateY(-6px)'; this.style.borderColor='rgba(167, 139, 250, 0.3)'; this.style.boxShadow='0 20px 40px rgba(0,0,0,0.5), 0 0 15px rgba(139, 92, 246, 0.1), inset 0 1px 0 rgba(255,255,255,0.1)';" onmouseout="this.style.transform='translateY(0)'; this.style.borderColor='rgba(139, 92, 246, 0.15)'; this.style.boxShadow='0 10px 30px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.05)';">
      <div style='background: linear-gradient(135deg, {bg_color}, #0f172a); width: 64px; height: 64px; border-radius: 20px; display: flex; justify-content: center; align-items: center; font-size: 28px; color: {icon_color}; margin-right: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1);'>{icon}</div>
      <div>
        <p style='margin: 0 0 6px 0; padding: 0; color: #94A3B8; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;'>{label}</p>
        <h2 style='margin: 0; padding: 0; color: #ffffff; font-size: 28px; font-weight: 800; line-height: 1.1; letter-spacing: -1px;'>{value}</h2>
      </div>
    </div>
    """

# ----------------------------------------------------
# Pages
# ----------------------------------------------------
def create_poll_page():
    if not st.session_state.is_admin:
        return
    with st.container(border=True):
        st.markdown("### Create New Poll")
        st.markdown("<p style='margin-bottom:20px;'>Configure a new poll for your audience.</p>", unsafe_allow_html=True)
        
        question = st.text_input("Poll Question", placeholder="e.g. Which keynote speaker should we invite?")
        
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            option1 = st.text_input("Choice A", placeholder="First option")
            option3 = st.text_input("Choice C (Optional)", placeholder="Third option")
        with col2:
            option2 = st.text_input("Choice B", placeholder="Second option")
            option4 = st.text_input("Choice D (Optional)", placeholder="Fourth option")
            
        st.write("")
        if st.button("Publish Poll", use_container_width=True, type="primary"):
            options = [opt.strip() for opt in [option1, option2, option3, option4] if opt.strip()]
            if not question.strip():
                st.error("Question is required.")
            elif len(options) < 2:
                st.error("At least 2 choices required.")
            else:
                new_poll = {
                    "id": st.session_state.next_poll_id,
                    "question": question.strip(),
                    "options": options,
                    "votes": {opt: [] for opt in options}
                }
                st.session_state.polls.append(new_poll)
                st.session_state.next_poll_id += 1
                save_data(st.session_state.polls, st.session_state.next_poll_id)
                st.success("Poll created successfully. View in 'Cast Vote' tab.")


def vote_page():
    if not st.session_state.polls:
        with st.container(border=True):
            st.markdown("<div style='text-align:center; padding: 4rem 0;'><h3 style='color:#ffffff; font-size: 2rem;'>No active polls</h3><p style='font-size: 1.1rem;'>Waiting for the administrator to create a poll.</p></div>", unsafe_allow_html=True)
        return

    poll_titles = [poll["question"] for poll in st.session_state.polls]
    selected_question = st.selectbox("Select Active Poll", poll_titles, label_visibility="collapsed")
    poll = next(p for p in st.session_state.polls if p["question"] == selected_question)
    st.write("")

    with st.container(border=True):
        st.markdown(f"<h3 style='margin-bottom: 2rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 1.5rem; font-size: 1.8rem; font-weight: 700; letter-spacing: -0.5px;'>{poll['question']}</h3>", unsafe_allow_html=True)
        
        with st.form("vote_form", border=False):
            selected_option = st.radio("Select your preference", poll["options"], label_visibility="collapsed")
            st.markdown("<div style='margin-top: 2rem; margin-bottom: 1rem; font-weight: 700; font-size: 1.2rem; color: #ffffff; letter-spacing: -0.3px;'>Your Information</div>", unsafe_allow_html=True)
            
            col_name, col_email = st.columns(2)
            with col_name:
                voter_name = st.text_input("Full Name", placeholder="John Doe")
            with col_email:
                voter_email = st.text_input("Student Email", placeholder="john@university.edu")

            st.write("")
            submitted = st.form_submit_button("Submit Vote", use_container_width=True, type="primary")
            
            if submitted:
                name = voter_name.strip().title()
                email = voter_email.strip().lower()
                
                if not name or not email:
                    st.error("Please provide both name and email.")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                else:
                    all_voted_emails = [v["email"] for v_list in poll["votes"].values() for v in v_list]
                    if email in all_voted_emails:
                        st.error(f"You have already voted! ({email})")
                    else:
                        poll["votes"][selected_option].append({"name": name, "email": email})
                        save_data(st.session_state.polls, st.session_state.next_poll_id)
                        st.success("Your vote has been submitted successfully!")

def results_page():
    if not st.session_state.polls:
        with st.container(border=True):
            st.markdown("<div style='text-align:center; padding: 4rem 0;'><h3 style='color:#ffffff; font-size: 2rem;'>No data available</h3><p>Waiting for votes to come in.</p></div>", unsafe_allow_html=True)
        return

    poll_titles = [poll["question"] for poll in st.session_state.polls]
    selected_question = st.selectbox("Select Poll to Analyze", poll_titles, label_visibility="collapsed")
    poll = next(p for p in st.session_state.polls if p["question"] == selected_question)
    st.write("")

    votes = poll["votes"]
    total_votes = sum(len(v_list) for v_list in votes.values())
    
    if total_votes == 0:
        with st.container(border=True):
            st.info("Waiting for the first vote to generate analytics.")
        return

    max_votes = max(len(v_list) for v_list in votes.values())
    winners = [opt for opt, vs in votes.items() if len(vs) == max_votes]
    winner_text = ", ".join(winners)
    winner_percentage = (max_votes / total_votes) * 100

    df = pd.DataFrame([(opt, len(vs)) for opt, vs in votes.items()], columns=['Option', 'Votes'])
    CHART_COLORS = ['#3b82f6', '#ec4899', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#f43f5e', '#84cc16']

    c1, c2, c3 = st.columns(3)
    c1.markdown(create_dark_metric("Total Votes", total_votes, "👤", "#3b82f6", "#ffffff"), unsafe_allow_html=True)
    c2.markdown(create_dark_metric("Winning Percentage", f"{winner_percentage:.1f}%", "⚡", "#10b981", "#ffffff"), unsafe_allow_html=True)
    c3.markdown(create_dark_metric("Current Leader", winner_text if len(winners) == 1 else "Tie", "🏆", "#f59e0b", "#ffffff"), unsafe_allow_html=True)
    st.write("")
    st.caption("Last updated: Just now")
    st.divider()

    col_chart, col_insights = st.columns([1, 1])
    
    with col_chart:
        with st.container(border=True):
            st.markdown("<p style='color:#a1a1aa; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom: 20px;'>Vote Distribution</p>", unsafe_allow_html=True)
            if PLOTLY_AVAILABLE:
                fig_donut = px.pie(df, values='Votes', names='Option', hole=0.65, color_discrete_sequence=CHART_COLORS)
                fig_donut.update_traces(
                    textposition='inside', 
                    textinfo='percent', 
                    hoverinfo='label+percent+value',
                    textfont_size=14,
                    marker=dict(line=dict(color='#111113', width=2))
                )
                fig_donut.update_layout(
                    height=240, 
                    margin=dict(t=10, b=10, l=10, r=10), 
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    legend=dict(font=dict(color='#a1a1aa'), orientation="v", y=0.5, x=1.0)
                )
                st.plotly_chart(fig_donut, use_container_width=True, config={'displayModeBar': False})
            else:
                st.warning("Visual engine updating.")
            
    with col_insights:
        with st.container(border=True):
            st.markdown("<p style='color:#a1a1aa; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom: 10px;'>Winning Margin</p>", unsafe_allow_html=True)
            if PLOTLY_AVAILABLE:
                fig_gauge = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=winner_percentage,
                    number={'suffix': "%", 'font': {'size': 44, 'color': '#ffffff', 'family': 'Plus Jakarta Sans', 'weight': 'bold'}},
                    title={'text': "", 'font': {'size': 14, 'color': '#a1a1aa'}},
                    gauge={
                        'axis': {'range': [0, 100], 'visible': False},
                        'bar': {'color': "#ffffff"},
                        'bgcolor': "#27272a",
                        'borderwidth': 0,
                    }
                ))
                fig_gauge.update_layout(height=240, margin=dict(t=30, b=10, l=10, r=10), paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
            else:
                st.warning("Visual engine updating.")

    st.divider()
    with st.container(border=True):
        st.markdown("<p style='color:#a1a1aa; font-weight:700; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;'>Insights</p>", unsafe_allow_html=True)
        st.info(f"💡 Insight: Most participants prefer **{winner_text}**, indicating a strong preference and consensus among the audience for this outcome.")
        st.write("")
        if PLOTLY_AVAILABLE:
            df_sorted = df.sort_values(by='Votes', ascending=False)
            num_bars = len(df_sorted)
            dynamic_colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(num_bars)]
            
            fig_bar = px.bar(df_sorted, x='Option', y='Votes', text='Votes')
            fig_bar.update_traces(
                marker_color=dynamic_colors,
                width=0.45, 
                textposition='outside', 
                textfont=dict(color='#ffffff', size=16, family='Plus Jakarta Sans', weight='bold')
            )
            fig_bar.update_layout(
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, title="", tickfont=dict(color='#a1a1aa', size=14)),
                yaxis=dict(showgrid=True, gridcolor='#27272a', title="", tickfont=dict(color='#a1a1aa', size=12)),
                margin=dict(t=20, b=10, l=10, r=10),
                height=340
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

    if st.session_state.is_admin:
        st.divider()
        with st.container(border=True):
            st.markdown("<p style='color:#a1a1aa; font-weight:700; text-transform:uppercase; letter-spacing:1px;'>Voters List</p>", unsafe_allow_html=True)
            for option, vs in votes.items():
                with st.expander(f"{option} ({len(vs)} votes)"):
                    if vs:
                        df_voters = pd.DataFrame(vs)
                        df_voters.columns = ["Name", "Student Email"]
                        st.dataframe(df_voters, use_container_width=True, hide_index=True)
                    else:
                        st.write("No votes yet.")

def admin_page():
    if not st.session_state.is_admin:
        with st.container(border=True):
            st.markdown("<h3>Admin Login</h3>", unsafe_allow_html=True)
            st.markdown("<p>Enter administrator credentials to manage polls.</p>", unsafe_allow_html=True)
            password = st.text_input("Admin Password", type="password", placeholder="Enter admin password")
            st.caption("Only organizers can create and manage polls")
            st.write("")
            if st.button("Sign In", type="primary", use_container_width=True):
                if password == "admin123":
                    st.session_state.is_admin = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
    else:
        with st.container(border=True):
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.markdown("<h3>Admin Dashboard</h3>", unsafe_allow_html=True)
            with col2:
                if st.button("Logout", use_container_width=True, type="secondary"):
                    st.session_state.is_admin = False
                    st.rerun()
                    
        st.write("")
        st.markdown("<h4>Manage Polls</h4>", unsafe_allow_html=True)
        if not st.session_state.polls:
            st.info("No active polls. Go to the Workspace tab to create one.")
            return
            
        for poll in st.session_state.polls:
            with st.container(border=True):
                col1, col2, col3 = st.columns([0.6, 0.2, 0.2])
                with col1:
                    st.markdown(f"**{poll['question']}**", unsafe_allow_html=True)
                    total_votes = sum(len(v_list) for v_list in poll['votes'].values())
                    st.markdown(f"<p style='font-size:0.95rem;'>Total Votes: {total_votes}</p>", unsafe_allow_html=True)
                with col2:
                    st.write("")
                    if st.button("Clear Votes", key=f"clear_{poll['id']}", use_container_width=True, type="secondary"):
                        for opt in poll['votes']:
                            poll['votes'][opt] = []
                        save_data(st.session_state.polls, st.session_state.next_poll_id)
                        st.rerun()
                with col3:
                    st.write("")
                    if st.button("Delete Poll", key=f"del_{poll['id']}", use_container_width=True, type="primary"):
                        st.session_state.polls = [p for p in st.session_state.polls if p['id'] != poll['id']]
                        save_data(st.session_state.polls, st.session_state.next_poll_id)
                        st.rerun()

# Execute Router Based on Session State
if st.session_state.current_page == "Cast Vote":
    vote_page()
elif st.session_state.current_page == "Workspace":
    create_poll_page()
elif st.session_state.current_page == "View Results":
    results_page()
elif st.session_state.current_page == "Admin Dashboard":
    admin_page()
