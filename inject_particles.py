import re
import random

def get_shadows(num):
    shadows = []
    colors = ['#8b5cf6', '#3b82f6', '#10b981', '#ffffff']
    for _ in range(num):
        x = random.randint(1, 100)
        y = random.randint(1, 100)
        w = random.randint(1, 3)
        colors_hex = random.choice(colors)
        shadows.append(f"{x}vw {y}vh {w}px {colors_hex}")
    return ", ".join(shadows)

with open('app.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Generate particle strings
shadows1 = get_shadows(50)
shadows2 = get_shadows(30)
shadows3 = get_shadows(20)

particle_css = f"""
    /* CSS PARTICLES BACKGROUND */
    .particles-layer-1 {{ position: fixed; top: 0; left: 0; width: 2px; height: 2px; background: transparent; box-shadow: {shadows1}; animation: animParticle 50s linear infinite; opacity: 0.6; pointer-events: none; z-index: 0; }}
    .particles-layer-2 {{ position: fixed; top: 0; left: 0; width: 3px; height: 3px; background: transparent; box-shadow: {shadows2}; animation: animParticle 80s linear infinite; opacity: 0.4; pointer-events: none; z-index: 0; }}
    .particles-layer-3 {{ position: fixed; top: 0; left: 0; width: 4px; height: 4px; background: transparent; box-shadow: {shadows3}; animation: animParticle 120s linear infinite; opacity: 0.2; pointer-events: none; z-index: 0; }}
    .particles-layer-1::after, .particles-layer-2::after, .particles-layer-3::after {{ content: " "; position: absolute; top: 100vh; width: 100%; height: 100%; background: transparent; box-shadow: inherit; }}

    @keyframes animParticle {{ 0% {{ transform: translateY(0); }} 100% {{ transform: translateY(-100vh); }} }}
"""

# Inject into CSS block (inserting just before base typography)
insertion_point = text.find("/* Base typography and background */")
if insertion_point != -1:
    text = text[:insertion_point] + particle_css + text[insertion_point:]

# We also need to inject the div elements into the DOM via st.markdown right below the top logo.
div_injection = "st.markdown('<div class=\"particles-layer-1\"></div><div class=\"particles-layer-2\"></div><div class=\"particles-layer-3\"></div>', unsafe_allow_html=True)"
target_logo = 'st.markdown("<div class=\'top-logo\'>◱ Jigyasa Poll</div>", unsafe_allow_html=True)'

if target_logo in text and div_injection not in text:
    text = text.replace(target_logo, target_logo + "\\n" + div_injection)

# Make sure buttons and form components have a higher z-index so they are clickable over particles.
# Actually pointer-events: none is in the CSS, so they won't block clicks.

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Particles added successfully")
