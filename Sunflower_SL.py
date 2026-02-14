import time
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Seed Growth Visualization", layout="centered")

st.title("🌻 Seed Growth Visualization")

# ---- Styling
st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(135deg, #ffcc33, #ff9933);
    color: black;
    border-radius: 25px;
    font-weight: 600;
    border: none;
    padding: 0.6em 1.5em;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

# ---- Constants
TOTAL_DAYS = 200
SEED_GROWTH_RATE = 0.003
BASE_RADIUS = 70
SEEDS_PER_DAY = 15
GOLDEN_ANGLE = 137.50776

# ---- Session State Initialization
if "seeds" not in st.session_state:
    st.session_state.seeds = []
if "day" not in st.session_state:
    st.session_state.day = 0
if "autoplay" not in st.session_state:
    st.session_state.autoplay = False
if "angle" not in st.session_state:
    st.session_state.angle = GOLDEN_ANGLE
if "show_prompt" not in st.session_state:
    st.session_state.show_prompt = True

# ---- Description
st.markdown(
    f'"Sunflower seeds grow with an angle {GOLDEN_ANGLE:.5f}° between them, '
    'this is golden angle found throughout nature." Click Play to see the seeds grow.'
)

# ---- Play Button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    if st.button("▶ Play / Pause", use_container_width=True):
        st.session_state.autoplay = not st.session_state.autoplay

# ==========================================================
# Simulation Logic
# ==========================================================

def advance_day():
    if st.session_state.day >= TOTAL_DAYS:
        return

    st.session_state.day += 1

    for _ in range(SEEDS_PER_DAY):
        st.session_state.seeds.append([len(st.session_state.seeds) + 1, 0.0, 0])

    for i in range(len(st.session_state.seeds)):
        st.session_state.seeds[i][2] += 1
        st.session_state.seeds[i][1] += SEED_GROWTH_RATE * st.session_state.seeds[i][2]

# Speed: 6 days per frame
if st.session_state.autoplay and st.session_state.day < TOTAL_DAYS:
    for _ in range(6):
        advance_day()

# ==========================================================
# Render Plot
# ==========================================================

fig, ax = plt.subplots(figsize=(6,6))
fig.patch.set_facecolor("gold")
ax.set_facecolor("gold")

angle_rad = math.radians(st.session_state.angle)
radius = BASE_RADIUS

ax.set_xlim(-radius, radius)
ax.set_ylim(-radius, radius)
ax.set_aspect("equal")
ax.axis("off")

ax.text(-radius*0.95, radius*0.95,
        f"Day {st.session_state.day} of {TOTAL_DAYS}",
        fontsize=14, fontweight="bold",
        alpha=0.6, verticalalignment="top")

ax.text(radius*0.95, radius*0.95,
        f"{st.session_state.angle:.1f}°",
        fontsize=14, fontweight="bold",
        alpha=0.6, horizontalalignment="right",
        verticalalignment="top")

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

# ---- Autoplay Loop
if st.session_state.autoplay and st.session_state.day < TOTAL_DAYS:
    time.sleep(0.015)
    st.rerun()

# ==========================================================
# Controls (Always Rendered — Just Conditionally Visible)
# ==========================================================

st.markdown("---")

if st.session_state.day >= TOTAL_DAYS and st.session_state.show_prompt:
    st.success("Now change the angle ↓")

st.markdown("#### Adjust Angle")

# IMPORTANT: Always render slider
st.slider(
    "Angle (°)",
    5.0,
    145.0,
    key="angle"
)

col1, col2 = st.columns(2)

# Restart Simulation
with col1:
    if st.button("Restart Simulation", use_container_width=True):
        st.session_state.seeds = []
        st.session_state.day = 0
        st.session_state.autoplay = True
        st.session_state.show_prompt = False
        st.rerun()

# Reset All
with col2:
    if st.button("Reset All", use_container_width=True):
        st.session_state.seeds = []
        st.session_state.day = 0
        st.session_state.autoplay = False
        st.session_state.angle = GOLDEN_ANGLE
        st.session_state.show_prompt = False
        st.rerun()
