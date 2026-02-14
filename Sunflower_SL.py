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

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("▶ Play / Pause", use_container_width=True):
        st.session_state.autoplay = not st.session_state.autoplay

# ==========================================================
# SLIDER (PLACED BEFORE SIMULATION)
# ==========================================================

st.markdown("### Adjust Angle")

# Slider directly controls var_angle - placed BEFORE rendering
st.session_state.var_angle = st.slider(
    "Angle (°)",
    5.0,
    145.0,
    value=st.session_state.var_angle,
    key="angle_slider_input",
)

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
    if st.button("Restart Simulation", use_container_width=True):
        st.session_state.seeds = []
        st.session_state.day = 0
        st.session_state.autoplay = True
        # Keep current angle from slider
        st.rerun()

with col2:
    if st.button("Reset All", use_container_width=True):
        # Delete the slider key specifically to force it to reset
        if "angle_slider_input" in st.session_state:
            del st.session_state["angle_slider_input"]
        
        # Reset all other values
        st.session_state.seeds = []
        st.session_state.day = 0
        st.session_state.autoplay = False
        st.session_state.var_angle = GOLDEN_ANGLE
        st.rerun()
