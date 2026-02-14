import time
import math
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ---------------------------
# Professional Streamlit Version
# ---------------------------

st.set_page_config(page_title="Seed Growth Visualization", layout="centered")

st.title("🌻 Seed Growth Visualization")

# ---- Hardcoded Natural Parameters
TOTAL_DAYS = 200
SEED_GROWTH_RATE = 0.003
BASE_RADIUS = 70
SEEDS_PER_DAY = 15
GOLDEN_ANGLE = 137.50776  # degrees

# ---- Session State Init
if "seeds" not in st.session_state:
    st.session_state.seeds = []
if "day" not in st.session_state:
    st.session_state.day = 0
if "autoplay" not in st.session_state:
    st.session_state.autoplay = False
if "angle" not in st.session_state:
    st.session_state.angle = GOLDEN_ANGLE

# ---- Sidebar Controls
with st.sidebar:
    st.header("Controls")

    angle_deg = st.slider(
        "Angle (°)",
        5.0,
        145.0,
        st.session_state.angle
    )
    st.session_state.angle = angle_deg

    zoom_option = st.radio(
        "Zoom",
        options=["1x", "10x", "1200x"],
        index=0
    )

    zoom = {"1x": 1, "10x": 10, "1200x": 1200}[zoom_option]

    st.divider()

    if st.button("Reset All", use_container_width=True):
        st.session_state.seeds = []
        st.session_state.day = 0
        st.session_state.autoplay = False
        st.session_state.angle = GOLDEN_ANGLE
        st.rerun()

# ---- Updated Description (Single Clean Line)
st.markdown(
    f'"Sunflower seeds grow with an angle {GOLDEN_ANGLE:.5f}° between them, '
    'this is golden angle found throughout nature." Click to see the seeds grow in the pattern.'
)

# ---- Play / Pause ABOVE Output
center_col = st.columns([1, 2, 1])[1]
with center_col:
    st.session_state.autoplay = st.toggle("Play / Pause", value=st.session_state.autoplay)

# ---- Simulation Logic
def advance_day():
    if st.session_state.day >= TOTAL_DAYS:
        return

    st.session_state.day += 1

    for _ in range(SEEDS_PER_DAY):
        st.session_state.seeds.append([len(st.session_state.seeds) + 1, 0.0, 0])

    for i in range(len(st.session_state.seeds)):
        st.session_state.seeds[i][2] += 1
        st.session_state.seeds[i][1] += SEED_GROWTH_RATE * st.session_state.seeds[i][2]

# ---- Determine stepping
if st.session_state.autoplay and st.session_state.day < TOTAL_DAYS:
    advance_day()

# ---- Render Plot
fig, ax = plt.subplots(figsize=(6, 6))

fig.patch.set_facecolor("gold")
ax.set_facecolor("gold")

golden_angle_rad = math.radians(st.session_state.angle)
radius = BASE_RADIUS / zoom

ax.set_xlim(-radius, radius)
ax.set_ylim(-radius, radius)
ax.set_aspect("equal")
ax.axis("off")

# ---- Elegant Corner Labels
ax.text(
    -radius * 0.95,
    radius * 0.95,
    f"Day {st.session_state.day}",
    fontsize=14,
    fontweight="bold",
    alpha=0.6,
    verticalalignment="top"
)

ax.text(
    radius * 0.95,
    radius * 0.95,
    f"{st.session_state.angle:.1f}°",
    fontsize=14,
    fontweight="bold",
    alpha=0.6,
    horizontalalignment="right",
    verticalalignment="top"
)

# ---- Plot Seeds
x, y, colors = [], [], []

for n, r, age in st.session_state.seeds:
    theta = n * golden_angle_rad
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
