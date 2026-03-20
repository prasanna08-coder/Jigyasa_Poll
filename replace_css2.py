import re

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the whole style block safely
start = text.find('<style>')
end = text.find('</style>') + len('</style>')

if start != -1 and end != -1:
    new_css = """<style>
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
</style>"""
    text = text[:start] + new_css + text[end:]

# Inject the pulsing live label
t1 = "st.markdown(\"<h1 class='hero-title'>Jigyasa Polling & Insights Platform</h1>\", unsafe_allow_html=True)"
t2 = t1 + "\\n" + "st.markdown(\"<div style='text-align: center; margin-bottom: 2rem;'><span class='live-pulse'>🔴 Live Poll Active</span></div>\", unsafe_allow_html=True)"

text = text.replace(t1, t2)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("CSS Replace Done")
