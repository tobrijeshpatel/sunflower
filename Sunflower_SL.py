import time
import math
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Seed Growth Visualization", layout="centered")

# ==========================================================
# TITLE + DESCRIPTION
# ==========================================================

st.title("🌻 Seed Growth Visualization")

GOLDEN_ANGLE = 137.50776

st.markdown(
    f"""
Sunflower seeds naturally grow with an angle of **{GOLDEN_ANGLE:.1f}°** between each seed.  
This special angle is called the **Golden Angle**, a pattern found throughout nature.

Press **Play** to watch the seeds grow in this beautiful spiral pattern.
"""
)

# ==========================================================
# CONSTANTS
# ==========================================================

TOTAL_DAYS = 200
SEED_GROWTH_RATE = 0.003
BASE_RADIUS = 70
SEEDS_PER_DAY = 15

# ==========================================================
# SESSION STATE INITIALIZATION
# ==========================================================

if "seeds" not in st.session_state:
    st.session_state.seeds = []
if "day" not in st.session_state:
    st.session_state.day = 0
if "autoplay" not in st.session_state:
    st.session_state.autoplay = False
if "var_angle" not in st.session_state:
    st.session_state.var_angle = GOLDEN_ANGLE

# ==========================================================
# PLAY BUTTON
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    button_emoji = "⏸️" if st.session_state.autoplay else "▶️"
    button_text = f"{button_emoji} {'Pause' if st.session_state.autoplay else 'Play'}"
    
    if st.button(button_text, use_container_width=True, type="primary"):
        st.session_state.autoplay = not st.session_state.autoplay

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================================
# SIMULATION ENGINE
# ==========================================================

def advance_day():
    if st.session_state.day >= TOTAL_DAYS:
        return

    st.session_state.day += 1

    for _ in range(SEEDS_PER_DAY):
        st.session_state.seeds.append([len(st.session_state.seeds) + 1, 0.0, 0])

    for i in range(len(st.session_state.seeds)):
        st.session_state.seeds[i][2] += 1
        st.session_state.seeds[i][1] += (
            SEED_GROWTH_RATE * st.session_state.seeds[i][2]
        )

if st.session_state.autoplay and st.session_state.day < TOTAL_DAYS:
    for _ in range(6):
        advance_day()

# ==========================================================
# RENDER PLOT (ALWAYS USES var_angle)
# ==========================================================

fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor("gold")
ax.set_facecolor("gold")

angle_rad = math.radians(st.session_state.var_angle)

ax.set_xlim(-BASE_RADIUS, BASE_RADIUS)
ax.set_ylim(-BASE_RADIUS, BASE_RADIUS)
ax.set_aspect("equal")
ax.axis("off")

ax.text(
    -BASE_RADIUS * 0.95,
    BASE_RADIUS * 0.95,
    f"Day {st.session_state.day} of {TOTAL_DAYS}",
    fontsize=14,
    fontweight="bold",
    alpha=0.6,
    verticalalignment="top",
)

ax.text(
    BASE_RADIUS * 0.95,
    BASE_RADIUS * 0.95,
    f"{st.session_state.var_angle:.1f}°",
    fontsize=14,
    fontweight="bold",
    alpha=0.6,
    horizontalalignment="right",
    verticalalignment="top",
)

x, y, colors = [], [], []

for n, r, age in st.session_state.seeds:
    theta = n * angle_rad
    xpos = r * math.cos(theta)
    ypos = r * math.sin(theta)

    x.append(xpos)
    y.append(ypos)

    fade = max(0.0, min(1.0, 1 - (r / BASE_RADIUS)))
    colors.append((fade, fade * 0.5, 0.1))

ax.scatter(x, y, c=colors, s=14)

st.pyplot(fig, clear_figure=True)

# ==========================================================
# SLIDER (PLACED BELOW OUTPUT)
# ==========================================================

st.markdown("### 🎨 Adjust Angle")

# Get slider value
new_angle = st.slider(
    "Angle (°)",
    5.0,
    145.0,
    value=st.session_state.var_angle,
    key="angle_slider_input",
)

# Update var_angle if slider changed
if new_angle != st.session_state.var_angle:
    st.session_state.var_angle = new_angle
    st.rerun()

# ==========================================================
# AUTO RERUN (ANIMATION)
# ==========================================================

if st.session_state.autoplay and st.session_state.day < TOTAL_DAYS:
    time.sleep(0.015)
    st.rerun()

# ==========================================================
# RESTART + RESET
# ==========================================================

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Restart Simulation", use_container_width=True, type="secondary"):
        st.session_state.seeds = []
        st.session_state.day = 0
        st.session_state.autoplay = True
        # Keep current angle from slider
        st.rerun()

with col2:
    if st.button("🏠 Reset All", use_container_width=True, type="secondary"):
        # Clear the slider widget state completely
        keys_to_delete = [k for k in st.session_state.keys()]
        for key in keys_to_delete:
            del st.session_state[key]
        
        # Reinitialize everything
        st.session_state.seeds = []
        st.session_state.day = 0
        st.session_state.autoplay = False
        st.session_state.var_angle = GOLDEN_ANGLE
        st.rerun()
