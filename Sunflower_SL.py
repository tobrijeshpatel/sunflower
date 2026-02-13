import time
import math
from typing import List, Tuple

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ---------------------------
# Streamlit app: Phyllotaxis / seed growth demo
# Converted from a Matplotlib-widgets version to Streamlit
# ---------------------------

st.set_page_config(page_title="Seed Growth Visualization", layout="centered")

st.title("🌻 Seed Growth Visualization")
st.caption("Interactive phyllotaxis-style seed growth with Streamlit sliders & controls.")

# ---- Defaults from the original script
TOTAL_DAYS_DEFAULT = 200
SEED_GROWTH_RATE_DEFAULT = 0.003
BASE_RADIUS_DEFAULT = 70

# ---- Session state init
if "seeds" not in st.session_state:
    # each seed: [n, r, age]
    st.session_state.seeds: List[List[float]] = []
if "day" not in st.session_state:
    st.session_state.day = 0
if "autoplay" not in st.session_state:
    st.session_state.autoplay = False
if "radius_log" not in st.session_state:
    st.session_state.radius_log: List[Tuple[int, float]] = []  # (day, outermost_radius)

# ---- Controls (Streamlit replaces matplotlib.widgets)
with st.sidebar:
    st.header("Controls")
    total_days = st.number_input("Total days", min_value=1, max_value=5000, value=TOTAL_DAYS_DEFAULT, step=1)
    seed_growth_rate = st.number_input("Seed growth rate", min_value=0.0, max_value=1.0, value=SEED_GROWTH_RATE_DEFAULT, step=0.001, format="%.3f")
    base_radius = st.number_input("Base radius", min_value=1, max_value=5000, value=BASE_RADIUS_DEFAULT, step=1)

    seeds_per_day = st.slider("Seeds / Day", 1, 20, 15, 1)
    zoom = st.slider("Zoom", 0.1, 1200.0, 1.0)
    angle_deg = st.slider("Angle (°)", 5.0, 145.0, 137.5)

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Zoom 1×", use_container_width=True):
            st.session_state["zoom_override"] = 1.0
    with col_b:
        if st.button("Golden ∠", use_container_width=True):
            # Original reset_angle used 137.50776
            st.session_state["angle_override"] = 137.50776

    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("Reset 🌻", use_container_width=True):
            st.session_state.seeds = []
            st.session_state.day = 0
            st.session_state.radius_log = []
            st.session_state.autoplay = False
            st.session_state.pop("zoom_override", None)
            st.session_state.pop("angle_override", None)
            st.rerun()
    with col_d:
        if st.button("Next Day ➜", use_container_width=True, disabled=(st.session_state.day >= int(total_days))):
            st.session_state["step_once"] = True

    st.divider()
    st.session_state.autoplay = st.toggle("Play ▶ / Pause ⏸", value=st.session_state.autoplay)

    st.divider()
    show_debug = st.checkbox("Show debug info", value=False)
    show_seed_table = st.checkbox("Show seed table (may be large)", value=False)

# Apply one-time overrides set by sidebar buttons
if "zoom_override" in st.session_state:
    zoom = float(st.session_state.pop("zoom_override"))
if "angle_override" in st.session_state:
    angle_deg = float(st.session_state.pop("angle_override"))

# ---- Simulation step (matches original logic)
def advance_one_day():
    """Advance the simulation by one day, matching the original script's update rules."""
    if st.session_state.day >= int(total_days):
        return

    st.session_state.day += 1

    # Add new seeds with r=0, age=0
    for _ in range(int(seeds_per_day)):
        st.session_state.seeds.append([len(st.session_state.seeds) + 1, 0.0, 0])

    # Age & grow all seeds
    for i in range(len(st.session_state.seeds)):
        st.session_state.seeds[i][2] += 1
        st.session_state.seeds[i][1] += seed_growth_rate * st.session_state.seeds[i][2]

    # Log outermost radius
    if st.session_state.seeds:
        outermost = max(s[1] for s in st.session_state.seeds)
        st.session_state.radius_log.append((st.session_state.day, float(outermost)))

# ---- Determine whether to step this run
step_now = False
if st.session_state.autoplay and st.session_state.day < int(total_days):
    step_now = True
if st.session_state.pop("step_once", False):
    step_now = True

if step_now:
    advance_one_day()

# ---- Render plot (matches original draw_frame)
def render_plot() -> plt.Figure:
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.patch.set_facecolor("gold")
    ax.set_facecolor("gold")

    golden_angle = math.radians(angle_deg)
    radius = base_radius / float(zoom)

    ax.set_xlim(-radius, radius)
    ax.set_ylim(-radius, radius)
    ax.set_aspect("equal", adjustable="box")
    ax.axis("off")

    x, y, colors = [], [], []

    if st.session_state.seeds:
        outermost = max(s[1] for s in st.session_state.seeds)
    else:
        outermost = None

    for n, r, age in st.session_state.seeds:
        theta = n * golden_angle
        xpos = r * math.cos(theta)
        ypos = r * math.sin(theta)

        if float(zoom) >= 1150:
            ax.plot([0, xpos], [0, ypos], linestyle=":", color="gray", linewidth=0.3)

        x.append(xpos)
        y.append(ypos)

        fade = max(0.0, min(1.0, 1 - (r / base_radius)))
        colors.append((fade, fade * 0.5, 0.1))

    ax.scatter(x, y, c=colors, s=14)
    ax.set_title(
        f"Day {st.session_state.day} — Zoom: {float(zoom):.1f}× | Angle: {float(angle_deg):.5f}° | Seeds/Day: {int(seeds_per_day)}",
        fontsize=15,
        color="black",
    )

    return fig

fig = render_plot()
st.pyplot(fig, clear_figure=True)

# ---- Status + optional debug output
left, right = st.columns(2)
with left:
    st.metric("Day", st.session_state.day)
with right:
    if st.session_state.seeds:
        outermost = max(s[1] for s in st.session_state.seeds)
        st.metric("Outermost radius", f"{outermost:.4f}")
    else:
        st.metric("Outermost radius", "—")

if show_debug:
    st.subheader("Debug")
    st.write(
        {
            "seeds_count": len(st.session_state.seeds),
            "seeds_per_day": int(seeds_per_day),
            "zoom": float(zoom),
            "angle_deg": float(angle_deg),
            "total_days": int(total_days),
            "seed_growth_rate": float(seed_growth_rate),
            "base_radius": int(base_radius),
            "autoplay": bool(st.session_state.autoplay),
        }
    )

    # Show a short sample of seed positions (avoid huge spam)
    if st.session_state.seeds:
        golden_angle = math.radians(angle_deg)
        sample = st.session_state.seeds[: min(20, len(st.session_state.seeds))]
        rows = []
        for n, r, age in sample:
            theta = n * golden_angle
            rows.append(
                {
                    "seed": int(n),
                    "x": float(r * math.cos(theta)),
                    "y": float(r * math.sin(theta)),
                    "radius": float(r),
                    "age": int(age),
                }
            )
        st.write("First seeds sample (up to 20):")
        st.dataframe(rows, use_container_width=True)

if show_seed_table and st.session_state.seeds:
    st.subheader("Seeds (all)")
    golden_angle = math.radians(angle_deg)
    rows = []
    for n, r, age in st.session_state.seeds:
        theta = n * golden_angle
        rows.append(
            {
                "seed": int(n),
                "x": float(r * math.cos(theta)),
                "y": float(r * math.sin(theta)),
                "radius": float(r),
                "age": int(age),
            }
        )
    st.dataframe(rows, use_container_width=True, height=420)

# ---- Radius log download (replaces writing radius_log.txt on disk every frame)
if st.session_state.radius_log:
    st.subheader("Radius log")
    log_lines = ["day,outermost_radius"] + [f"{d},{r:.6f}" for d, r in st.session_state.radius_log]
    csv_bytes = ("\n".join(log_lines)).encode("utf-8")
    st.download_button(
        "Download radius_log.csv",
        data=csv_bytes,
        file_name="radius_log.csv",
        mime="text/csv",
        use_container_width=False,
    )

# ---- Autoplay loop: emulate the original timer by rerunning periodically
# IMPORTANT: We avoid an infinite while-loop; instead we sleep briefly then rerun once.
if st.session_state.autoplay and st.session_state.day < int(total_days):
    time.sleep(0.05)  # ~50ms, like original timer interval
    st.rerun()
