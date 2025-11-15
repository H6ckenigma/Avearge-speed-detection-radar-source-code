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

# control buttons
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    if st.button("Start Simulation", use_container_width=True):
        st.session_state.running = True
        st.session_state.results = []
        st.rerun()
        
with col2:
    if st.button("Stop Simulation", use_container_width=True):
        st.session_state.running = False
        st.rerun()

st.markdown("---")
st.subheader("Live Detections")

# initialize session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'results' not in st.session_state:
    st.session_state.results = []

if st.session_state.running:
    # stats display
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    total_cars_stat = stats_col1.empty()
    speeders_stat = stats_col2.empty()
    avg_speed_stat = stats_col3.empty()
    
    # log display
    log_area = st.empty()
    
    total_speeders = 0
    total_speed = 0
    car_count = 0
    log_text = ""
    
    # continuous simulation loop
    while st.session_state.running:
        car_count += 1
        plate = gen_plate()
        speed = random.randint(80, 160)
        
        # check if speeding
        if speed > speed_limit:
            status = "SPEEDING"
            total_speeders += 1
            color = "red"
        else:
            status = "Good"
            color = "green"
        
        total_speed += speed
        
        # add to log
        log_text = f"Car #{car_count} | {plate} | {speed} km/h | {status}\n" + log_text
        log_area.text_area("", log_text, height=300)
        
        # update stats
        total_cars_stat.metric("Total Cars", car_count)
        speeders_stat.metric("Speeders", total_speeders)
        avg_speed_stat.metric("Average Speed", f"{total_speed/car_count:.0f} km/h")
        
        # store results
        st.session_state.results.append({
            'plate': plate,
            'speed': speed,
            'status': status,
            'excess': max(0, speed - speed_limit)
        })
        
        time.sleep(0.5)
    
    st.success("Simulation stopped")
    
    # show results when stopped
    if len(st.session_state.results) > 0:
        st.markdown("---")
        st.subheader("Results Summary")
        st.dataframe(pd.DataFrame(st.session_state.results), use_container_width=True)

else:
    st.info("Click Start Simulation to begin")
    
    # show previous results if any
    if len(st.session_state.results) > 0:
        st.markdown("---")
        st.subheader("Previous Results")
        st.dataframe(pd.DataFrame(st.session_state.results), use_container_width=True)
    
    # instructions
    with st.expander("How it works"):
        st.write("""
        This system uses two radar points to calculate average speed over a distance.
        Unlike single point radars that can be bypassed using waze, this measures speed
        over the entire section and cannot be circumvented.
        
        The system records timestamps at both radars and calculates the average speed
        based on the distance traveled and time taken.
        """)
    
    # about section
    with st.expander("About this project"):
        st.write("""
        Built to address road safety issues in Morocco where drivers often bypass 
        single-point speed cameras using navigation apps.
        
        Average speed cameras have been proven to reduce accidents by 40-60 percent
        in countries where they are deployed.
        
        GitHub: https://github.com/H6ckenigma/New_radr_system/
        """)

st.markdown("---")