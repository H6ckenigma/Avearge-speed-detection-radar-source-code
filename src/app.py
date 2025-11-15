import streamlit as st
import time
import random
from Data_simulator import gen_plate
from radar_conf import Distance, Speed_limit

st.set_page_config(page_title="Radar Enigma", layout="wide")

st.markdown("# Radar Enigma")
st.markdown("### Average Speed Detection System")
st.markdown("---")

# sidebar
st.sidebar.header("Configuration")
distance = st.sidebar.slider("Distance (km)", 10, 200, int(Distance))
speed_limit = st.sidebar.slider("Speed Limit (km/h)", 60, 180, Speed_limit)

col1, col2 = st.columns(2)
col1.metric("Distance", f"{distance} km")
col2.metric("Speed Limit", f"{speed_limit} km/h")

st.markdown("---")

# session state
if 'running' not in st.session_state:
    st.session_state.running = False
if 'cars' not in st.session_state:
    st.session_state.cars = []

col1, col2 = st.columns([1, 4])
if col1.button("Start", disabled=st.session_state.running):
    st.session_state.running = True
    st.session_state.cars = []
    st.rerun()

if col2.button("Stop", disabled=not st.session_state.running):
    st.session_state.running = False
    st.rerun()

st.markdown("---")
st.subheader("Live Detections")

if st.session_state.running:
    # generate one car
    plate = gen_plate()
    speed = random.randint(80, 160)
    status = "SPEEDING" if speed > speed_limit else "Good"
    
    st.session_state.cars.insert(0, {
        'num': len(st.session_state.cars) + 1,
        'plate': plate,
        'speed': speed,
        'status': status
    })
    
    # show stats
    total = len(st.session_state.cars)
    speeders = sum(1 for c in st.session_state.cars if c['status'] == "SPEEDING")
    avg = sum(c['speed'] for c in st.session_state.cars) / total
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("Speeders", speeders)
    col3.metric("Avg Speed", f"{avg:.0f} km/h")
    
    # show log
    for car in st.session_state.cars[:20]:
        if car['status'] == "SPEEDING":
            st.markdown(f"<span style='color:red'>Car #{car['num']} > {car['plate']} going {car['speed']} km/h >> {car['status']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:green'>Car #{car['num']} > {car['plate']} going {car['speed']} km/h >> {car['status']}</span>", unsafe_allow_html=True)
    
    time.sleep(1)
    st.rerun()

elif len(st.session_state.cars) > 0:
    # show final results
    total = len(st.session_state.cars)
    speeders = sum(1 for c in st.session_state.cars if c['status'] == "SPEEDING")
    avg = sum(c['speed'] for c in st.session_state.cars) / total
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total", total)
    col2.metric("Speeders", speeders)
    col3.metric("Avg Speed", f"{avg:.0f} km/h")
    
    for car in st.session_state.cars[:20]:
        if car['status'] == "SPEEDING":
            st.markdown(f"<span style='color:red'>Car #{car['num']} > {car['plate']} going {car['speed']} km/h >> {car['status']}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='color:green'>Car #{car['num']} > {car['plate']} going {car['speed']} km/h >> {car['status']}</span>", unsafe_allow_html=True)

else:
    st.info("Click Start to begin")

st.markdown("---")
st.markdown("Made for road safety in Morocco")