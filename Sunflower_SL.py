import time
import math
import matplotlib.pyplot as plt
import streamlit as st

st.set_page_config(page_title="Seed Growth Visualization", layout="centered")

# ==========================================================
# CUSTOM STYLING - YELLOW BUTTONS
# ==========================================================

st.markdown("""
    <style>
    /* Make all buttons yellow */
    .stButton > button {
        background-color: #FFD700;
        color: #000000;
        border: none;
        font-weight: 600;
    }
    .stButton > button:hover {
        background-color: #FFC700;
        color: #000000;
        border: none;
    }
    .stButton > button:active {
        background-color: #FFB700;
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

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
if "first_run_complete" not in st.session_state:
    st.session_state.first_run_complete = False
if "angle_changed" not in st.session_state:
    st.session_state.angle_changed = False
if "restarted_once" not in st.session_state:
    st.session_state.restarted_once = False

# ==========================================================
# PLAY BUTTON
# ==========================================================

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Determine button text based on state
    if st.session_state.autoplay:
        button_text = "Pause"
    elif st.session_state.day >= TOTAL_DAYS:
        button_text = "Play Again"
    else:
        button_text = "Play"
    
    if st.button(button_text, use_container_width=True, type="primary"):
        st.session_state.autoplay = not st.session_state.autoplay
        st.rerun()

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

# Mark first run as complete when simulation finishes
if st.session_state.day >= TOTAL_DAYS and not st.session_state.first_run_complete:
    st.session_state.first_run_complete = True

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

# Show message after first run completes
if st.session_state.first_run_complete and not st.session_state.angle_changed:
    st.success("✨ Now change the angle and see what happens!")
    st.markdown("### Adjust Angle")

# Show slider only after first run is complete
if st.session_state.first_run_complete:
    # Slider without a key - directly bound to var_angle
    # This allows it to reset properly when var_angle changes
    new_angle = st.slider(
        "Angle (°)",
        5.0,
        145.0,
        value=st.session_state.var_angle,
    )

    # Update var_angle if slider changed
    if new_angle != st.session_state.var_angle:
        st.session_state.var_angle = new_angle
        st.session_state.angle_changed = True
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

# Show Restart button only after angle has been changed
if st.session_state.angle_changed:
    with col1:
        if st.button("Restart Simulation", use_container_width=True, type="secondary"):
            st.session_state.seeds = []
            st.session_state.day = 0
            st.session_state.autoplay = True
            st.session_state.restarted_once = True
            # Keep current angle from slider
            st.rerun()

# Show Reset button only after simulation has been restarted
if st.session_state.restarted_once:
    with col2:
        if st.button("Reset All", use_container_width=True, type="secondary"):
            # Reset all values to defaults
            st.session_state.seeds = []
            st.session_state.day = 0
            st.session_state.autoplay = False
            st.session_state.var_angle = GOLDEN_ANGLE
            st.session_state.first_run_complete = False
            st.session_state.angle_changed = False
            st.session_state.restarted_once = False
            st.rerun()
