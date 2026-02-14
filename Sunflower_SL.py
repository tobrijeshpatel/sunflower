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
    /* Reduce overall padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
    }
    
    /* Make ALL buttons yellow - including primary */
    .stButton > button {
        background-color: #FFD700 !important;
        color: #000000 !important;
        border: none !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background-color: #FFC700 !important;
        color: #000000 !important;
    }
    
    /* Consistent button sizing */
    div[data-testid="column"] > div > div > div > button {
        font-size: 14px !important;
        padding: 8px 16px !important;
    }
    
    /* Style preset buttons with a lighter color and smaller size */
    button[kind="secondary"] {
        background-color: #FFFACD !important;
        color: #000000 !important;
        border: 1px solid #FFD700 !important;
        font-size: 11px !important;
        padding: 6px 8px !important;
        min-height: 34px !important;
    }
    button[kind="secondary"]:hover {
        background-color: #FFD700 !important;
    }
    
    /* Compact spacing for mobile */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 1rem;
            padding-left: 1rem;
            padding-right: 1rem;
        }
        
        /* Make buttons smaller but not full width on mobile */
        button[kind="secondary"] {
            font-size: 10px !important;
            padding: 4px 4px !important;
            min-height: 30px !important;
            white-space: nowrap !important;
        }
        
        div[data-testid="column"] > div > div > div > button {
            font-size: 13px !important;
            padding: 7px 12px !important;
        }
        
        /* Reduce column gaps */
        div[data-testid="column"] {
            padding: 0 2px !important;
        }
    }
    
    /* Reduce spacing between elements */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* Consistent typography */
    h1 {
        font-size: 32px !important;
        margin-bottom: 0.5rem !important;
        font-weight: 700 !important;
    }
    h4 {
        font-size: 16px !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Consistent text sizing */
    p, div, span {
        font-size: 14px !important;
    }
    
    /* Success/Info boxes consistent sizing */
    .stAlert {
        font-size: 13px !important;
        padding: 8px 12px !important;
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
    <div style='background-color: #FFF8DC; padding: 12px 16px; border-radius: 8px; border-left: 4px solid #FFD700; margin-bottom: 10px;'>
    <p style='margin: 0 0 8px 0; font-size: 14px; color: #333333;'><strong>Discover Nature's Hidden Math!</strong> 🔍 Sunflower seeds grow with an angle of <strong>{GOLDEN_ANGLE:.1f}°</strong> between each seed — the <strong>Golden Angle</strong> that allows perfect packing with no gaps!</p>
    <p style='margin: 0; font-size: 12px; color: #555555;'><em>Press <strong>Play</strong> and watch the magic unfold...</em></p>
    </div>
    """, unsafe_allow_html=True
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
        # If simulation is complete and user clicks Play Again, restart it
        if st.session_state.day >= TOTAL_DAYS and not st.session_state.autoplay:
            st.session_state.seeds = []
            st.session_state.day = 0
            st.session_state.autoplay = True
        else:
            # Normal play/pause toggle
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

fig, ax = plt.subplots(figsize=(5, 5))
fig.patch.set_facecolor("gold")
ax.set_facecolor("gold")

angle_rad = math.radians(st.session_state.var_angle)

ax.set_xlim(-BASE_RADIUS, BASE_RADIUS)
ax.set_ylim(-BASE_RADIUS, BASE_RADIUS)
ax.set_aspect("equal")
ax.axis("off")

# Display angle in top right corner (smaller font)
ax.text(
    BASE_RADIUS * 0.95,
    BASE_RADIUS * 0.95,
    f"{st.session_state.var_angle:.1f}°",
    fontsize=11,
    fontweight="bold",
    alpha=0.6,
    horizontalalignment="right",
    verticalalignment="top",
)

# Add seed count
ax.text(
    0,
    -BASE_RADIUS * 0.95,
    f"Seeds: {len(st.session_state.seeds)}",
    fontsize=12,
    alpha=0.6,
    horizontalalignment="center",
    verticalalignment="bottom",
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

# Show progress bar during simulation
if st.session_state.day < TOTAL_DAYS:
    progress = st.session_state.day / TOTAL_DAYS
    st.progress(progress, text=f"Growing... {int(progress * 100)}% complete")

# ==========================================================
# SLIDER (PLACED BELOW OUTPUT)
# ==========================================================

# Show message after first run completes
if st.session_state.first_run_complete and not st.session_state.angle_changed:
    st.success("✨ **Now try changing the angle below!**")
    st.info("💡 A small degree change can result in a large pattern shift.", icon="💡")
    st.markdown("#### 🎨 Adjust Angle")

# Show slider only after first run is complete
if st.session_state.first_run_complete:
    # Add quick preset buttons
    st.markdown("<p style='font-size: 13px; margin-bottom: 4px; color: #333333;'><strong>🎯 Quick Presets:</strong></p>", unsafe_allow_html=True)
    preset_cols = st.columns(5)
    
    presets = [
        ("Golden", GOLDEN_ANGLE),
        ("45°", 45.0),
        ("90°", 90.0),
        ("90.25°", 90.25),
        ("145°", 145.0)
    ]
    
    for idx, (label, angle) in enumerate(presets):
        with preset_cols[idx]:
            if st.button(label, use_container_width=True, key=f"preset_{idx}"):
                st.session_state.var_angle = angle
                st.session_state.angle_changed = True
                st.rerun()
    
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
