import time
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Seed Growth Visualization", layout="centered")

st.title("🌻 Seed Growth Visualization")

# ---- Constants
TOTAL_DAYS = 200
SEED_GROWTH_RATE = 0.003
BASE_RADIUS = 70
SEEDS_PER_DAY = 15
GOLDEN_ANGLE = 137.50776

# ---- Session State
if "seeds" not in st.session_state:
    st.session_state.seeds = []
if "day" not in st.session_state:
    st.session_state.day = 0
if "running" not in st.session_state:
    st.session_state.running = False
if "angle" not in st.session_state:
    st.session_state.angle = GOLDEN_ANGLE

# ---- Play Button (Top)
st.markdown("""
<style>
div.stButton > button:first-child {
    background: linear-gradient(135deg, #ffcc33, #ff9933);
    color: black;
    border-radius: 25px;
    height: 3em;
    font-weight: 600;
    border: none;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)

center_col = st.columns([1, 2, 1])[1]
with center_col:
    if st.button("▶ Play Simulation", use_container_width=True):
        st.session_state.running = True

# ---- Description
st.markdown(
    f'"Sunflower seeds grow with an angle {GOLDEN_ANGLE:.5f}° between them, '
    'this is golden angle found throughout nature." Click to see the seeds grow in the pattern.'
)

# ---- Simulation Step
def advance_day():
    if st.session_state.day >= TOTAL_DAYS:
        st.session_state.running = False
        return

    st.session_state.day += 1

    for _ in range(SEEDS_PER_DAY):
        st.session_state.seeds.append([len(st.session_state.seeds) + 1, 0.0, 0])

    for i in range(len(st.session_state.seeds)):
        st.session_state.seeds[i][2] += 1
        st.session_state.seeds[i][1] += SEED_GROWTH_RATE * st.session_state.seeds[i][2]

# ---- AUTOPLAY (FIXED ORDER)
if st.session_state.running:
    advance_day()
    time.sleep(0.02)
    st.rerun()

# ---- Render Plot
fig, ax = plt.subplots(figsize=(6, 6))
fig.patch.set_facecolor("gold")
ax.set_facecolor("gold")

angle_rad = math.radians(st.session_state.angle)
radius = BASE_RADIUS

ax.set_xlim(-radius, radius)
ax.set_ylim(-radius, radius)
ax.set_aspect("equal")
ax.axis("off")

# ---- Elegant Corner Labels (Shadow + Soft Fade)

# Day shadow
ax.text(-radius*0.95, radius*0.95,
        f"Day {st.session_state.day}",
        fontsize=14,
        fontweight="bold",
        color="black",
        alpha=0.25,
        verticalalignment="top")

# Day main
ax.text(-radius*0.95, radius*0.95,
        f"Day {st.session_state.day}",
        fontsize=14,
        fontweight="bold",
        color="white",
        alpha=0.85,
        verticalalignment="top")

# Angle shadow
ax.text(radius*0.95, radius*0.95,
        f"{st.session_state.angle:.1f}°",
        fontsize=14,
        fontweight="bold",
        color="black",
        alpha=0.25,
        horizontalalignment="right",
        verticalalignment="top")

# Angle main
ax.text(radius*0.95, radius*0.95,
        f"{st.session_state.angle:.1f}°",
        fontsize=14,
        fontweight="bold",
        color="white",
        alpha=0.85,
        horizontalalignment="right",
        verticalalignment="top")

# ---- Plot Seeds (Warm Golden Fade)
x, y, colors, sizes = [], [], [], []

for n, r, age in st.session_state.seeds:
    theta = n * angle_rad
    xpos = r * math.cos(theta)
    ypos = r * math.sin(theta)

    x.append(xpos)
    y.append(ypos)

    fade = min(1.0, age / 10)
    colors.append((fade, fade * 0.5, 0.1))  # warm tone
    sizes.append(12 + fade * 6)

ax.scatter(x, y, c=colors, s=sizes)

st.pyplot(fig, clear_figure=True)

# ---- Controls BELOW Output
st.markdown("---")
st.subheader("Controls")

col1, col2 = st.columns(2)

with col1:
    st.session_state.angle = st.slider(
        "Angle (°)",
        5.0,
        145.0,
        st.session_state.angle
    )

with col2:
    zoom_choice = st.radio("Zoom", ["1x", "10x", "1200x"], index=0)

if st.button("Reset All"):
    st.session_state.seeds = []
    st.session_state.day = 0
    st.session_state.running = False
    st.session_state.angle = GOLDEN_ANGLE
    st.rerun()
