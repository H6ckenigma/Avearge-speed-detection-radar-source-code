import streamlit as st
import pandas as pd
import time
import random

# plate generator
def gen_plate():    
    num = "".join([str(random.randint(0,9)) for _ in range(6)])
    city = str(random.randint(1,58))
    letter = random.choice("ABDEFG")
    return num + "|" + letter + "|" + city

# Config
Distance = 50.0
Speed_limit = 120
Num_cars = 30

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
num_cars = st.sidebar.slider("Number of cars", 5, 30, min(Num_cars, 20))

# display metrics
col1, col2, col3 = st.columns(3)
col1.metric("Distance", f"{distance} km")
col2.metric("Speed Limit", f"{speed_limit} km/h")
col3.metric("Cars", num_cars)

st.markdown("---")

# control buttons
col1, col2 = st.columns([1, 4])
with col1:
    start_btn = st.button("Start Simulation", use_container_width=True)

st.markdown("---")
st.subheader("Live Detections")

if start_btn:
    results = []
    progress_bar = st.progress(0)
    status_text = st.empty()
    log_area = st.empty()
    
    #stats columns
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    
    total_speeders = 0
    total_speed = 0
    log_text = ""
    
    # run simulation
    for i in range(num_cars):
        plate = gen_plate()
        speed = random.randint(80, 160)
        
        # check if speeding
        if speed > speed_limit:
            status = "SPEEDING"
            total_speeders += 1
        else:
            status = "Good"
        
        total_speed += speed
        
        # update progress
        progress_bar.progress((i + 1) / num_cars)
        status_text.text(f"Processing car {i + 1}/{num_cars}...")
        
        log_text += f"Car #{i + 1} | {plate} | {speed} km/h | {status}\n"
        log_area.text_area("", log_text, height=300)
        
        # update stats
        stats_col1.metric("Total Cars", i + 1)
        stats_col2.metric("Speeders", total_speeders)
        stats_col3.metric("Average Speed", f"{total_speed/(i+1):.0f} km/h")
        
        results.append({'plate': plate, 'speed': speed, 'status': status})
        
        time.sleep(0.2)
    
    status_text.success("Simulation Complete")
    
    # show results table
    st.markdown("---")
    st.subheader("Results Summary")
    st.dataframe(pd.DataFrame(results), use_container_width=True)

else:
    st.info("Click Start Simulation to begin")
    
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