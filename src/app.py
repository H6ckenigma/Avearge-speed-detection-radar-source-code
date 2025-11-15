import streamlit as st
import pandas as pd
import time
import random
from Data_simulator import gen_plate
from radar_conf import Distance, Speed_limit, Num_cars

# Page setup
st.set_page_config(page_title="Radar Enigma", layout="wide")

# Title
st.markdown("# Radar Enigma")
st.markdown("### Average Speed Detection System")
st.markdown("---")

# settings sidebar
st.sidebar.header("Configuration")
distance = st.sidebar.slider("Distance between radars (km)", 10, 200, int(Distance))
speed_limit = st.sidebar.slider("Speed Limit (km/h)", 60, 180, Speed_limit)

# display metrics
col1, col2 = st.columns(2)
col1.metric("Distance", f"{distance} km")
col2.metric("Speed Limit", f"{speed_limit} km/h")

st.markdown("---")

# initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'car_count' not in st.session_state:
    st.session_state.car_count = 0
if 'total_speeders' not in st.session_state:
    st.session_state.total_speeders = 0
if 'total_speed' not in st.session_state:
    st.session_state.total_speed = 0
if 'log_lines' not in st.session_state:
    st.session_state.log_lines = []

# control buttons
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("Start Simulation", use_container_width=True, disabled=st.session_state.running):
        st.session_state.running = True
        st.session_state.car_count = 0
        st.session_state.total_speeders = 0
        st.session_state.total_speed = 0
        st.session_state.log_lines = []
        st.rerun()
        
with col2:
    if st.button("Stop Simulation", use_container_width=True, disabled=not st.session_state.running):
        st.session_state.running = False
        st.rerun()

st.markdown("---")

# Status
if st.session_state.running:
    st.success("Simulation running...")
else:
    st.info("Ready")

st.subheader("Live Detections")

# stats display
stats_col1, stats_col2, stats_col3 = st.columns(3)
stats_col1.metric("Total Cars", st.session_state.car_count)
stats_col2.metric("Speeders", st.session_state.total_speeders)
if st.session_state.car_count > 0:
    stats_col3.metric("Average Speed", f"{st.session_state.total_speed/st.session_state.car_count:.0f} km/h")
else:
    stats_col3.metric("Average Speed", "0 km/h")

# log display
log_container = st.container()

if st.session_state.running:
    # generate new car
    st.session_state.car_count += 1
    plate = gen_plate()
    speed = random.randint(80, 160)
    
    # check if speeding
    if speed > speed_limit:
        status = "SPEEDING"
        st.session_state.total_speeders += 1
    else:
        status = "Good"
    
    st.session_state.total_speed += speed
    
    # add to log
    log_line = f"Car #{st.session_state.car_count} > {plate} going {speed} km/h >> {status}"
    st.session_state.log_lines.append(log_line)
    
    # display log (latest at top)
    with log_container:
        for line in reversed(st.session_state.log_lines[-50:]):  # show last 50 cars
            if "SPEEDING" in line:
                st.markdown(f"<span style='color: #ff5555;'>{line}</span>", unsafe_allow_html=True)
            else:
                st.markdown(f"<span style='color: #55ff55;'>{line}</span>", unsafe_allow_html=True)
    
    # wait and continue
    time.sleep(1)
    st.rerun()

else:
    # show log when stopped
    if len(st.session_state.log_lines) > 0:
        with log_container:
            for line in reversed(st.session_state.log_lines[-50:]):
                if "SPEEDING" in line:
                    st.markdown(f"<span style='color: #ff5555;'>{line}</span>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<span style='color: #55ff55;'>{line}</span>", unsafe_allow_html=True)
    else:
        with log_container:
            st.write("Waiting for simulation to start...")
    
    # instructions
    with st.expander("How it works"):
        st.write("""
        This system uses two radar points to calculate average speed over a distance.
        Unlike single point radars that can be bypassed using waze, this measures speed
        over the entire section and cannot be circumvented.
        """)

st.markdown("---")
st.markdown("Made for road safety in Morocco")