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

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Reset All", use_container_width=True):
            st.session_state.seeds = []
            st.session_state.day = 0
            st.session_state.autoplay = False
            st.session_state.angle = GOLDEN_ANGLE
            st.rerun()

    with col2:
        if st.button("Next Day", use_container_width=True):
            st.session_state.step_once = True

    st.session_state.autoplay = st.toggle("Play / Pause", value=st.session_state.autoplay)

# ---- About Section
st.markdown(
    f"""
    ### About  
    Seeds grow using the **golden angle ({GOLDEN_ANGLE:.5f}°)** —  
    a pattern found throughout nature.

    Even a small change in this angle dramatically alters the structure.  
    Try adjusting it and observe how the pattern transforms.
    """
)

# ---- Simulation Logic
def advance_day():
    if st.session_state.day >= TOTAL_DAYS:
        return

    st.session_state.day += 1

    # Add new seeds
    for _ in range(SEEDS_PER_DAY):
        st.session_state.seeds.append([len(st.session_state.seeds) + 1, 0.0, 0])

    # Grow seeds
    for i in range(len(st.session_state.seeds)):
        st.session_state.seeds[i][2] += 1
        st.session_state.seeds[i][1] += SEED_GROWTH_RATE * st.session_state.seeds[i][2]


# ---- Determine stepping
step_now = False

if st.session_state.autoplay and st.session_state.day < TOTAL_DAYS:
    step_now = True

if st.session_state.pop("step_once", False):
    step_now = True

# Faster animation
if step_now:
    steps_per_frame = 5 if st.session_state.autoplay else 1
    for _ in range(steps_per_frame):
        advance_day()

# ---- Render Plot
fig, ax = plt.subplots(figsize=(6, 6))

# 🌟 Restore golden/yellow background
fig.patch.set_facecolor("gold")
ax.set_facecolor("gold")

golden_angle_rad = math.radians(st.session_state.angle)
radius = BASE_RADIUS / zoom

ax.set_xlim(-radius, radius)
ax.set_ylim(-radius, radius)
ax.set_aspect("equal")
ax.axis("off")

x, y = [], []
colors = []

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
    time.sleep(0.01)
    st.rerun()
