import streamlit
import pandas
import time
import random
from datetime import datetime, timedelta
from Data_simulator import gen_plate
from radar_conf import Distance, Speed_limit, Num_cars

streamlit.set_page_config(
    page_title="Radar Enigma",
    layout="wide"
)

streamlit.markdown("""
<syle>
    .main {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%)
    }
    .stButton>button {
        background: linear-gradient(180deg, #3a86ff 0%, #1d5fcf 100%);
        color: white;         
        border-radius: 10px;
        padding: 15px 30px;
        font-weight: bold;
        border: 2px solid #3a86ff;           
    }
    .stButton>button:hover {
        background: linear-gradient(180deg, #ffb703 0%, #e09a03 100%);
        border: 2px solid #ffb703;
        color: black;
    }
    .metric-card {
        background: rgba(255, 183, 3, 0.1);
        border-left: 4px solid #3a86ff;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

#Title
streamlit.markdown("Radar Enigma")
streamlit.markdown("### Average Speed Detection System")
streamlit.markdown("---")

#Sidebar settings
streamlit.sidebar.header("Configuration")
distance = streamlit.sidebar.slider("Distance Between Radars (km)", 10, 200, int(Distance))
Speed_limit = streamlit.sidebar.slider("Speed Limit (Km/h)", 60, 180, Speed_limit)
num_cars = streamlit.sidebar.slider("Number of cars to simulate", 5, 50, min(Num_cars, 20))

col1, col2, col3 = streamlit.columns(3)
with col1:
    streamlit.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #3a86ff;"> Distance </h3>
        <h2 style="color: #e0e1dd;"> {Distance} km </h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    streamlit.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #3a86ff;"> Speed Limit </h3>
        <h2 style="color: #e0e1dd;"> {Speed_limit} Km/h </h2>
""", unsafe_allow_html=True)
    
with col3:
    streamlit.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #3a86ff;"> Number Of Cars </h3>
        <h2 style="color: #e0e1dd;">{Num_cars}</h2>
    </div>              
""", unsafe_allow_html=True)
    
streamlit.markdown("---")

col1, col2, col3 = streamlit.columns([1, 1, 3])
with col1:
    start_btn = streamlit.button("Start Simulation", use_container_width=True)
with col2:
    stop_btn = streamlit.button("Stop Simulation", use_container_width=True)

streamlit.markdown("---")

streamlit("Live Detections")

if start_btn:
    if 'results' not in streamlit.session_state:
        streamlit.session_state.results = []

    #Progrss bar
    progress_bar = streamlit.progress(0)
    status_text = streamlit.empty()

    #Logs
    log_container = streamlit.container()

    #stats
    stats_col1, stats_col2, stats_col3 = streamlit.columns(3)
    total_cars_stat = stats_col1.empty()
    speeders_stat = stats_col2.empty()
    avg_speed_stat = stats_col3.empty()

    total_speeders = 0
    total_speed_sum = 0

    for i in range(num_cars):
        plate = gen_plate()
        speed = random.randint(80, 160)

        time_seconds = (distance / speed) * 3600

        if speed > Speed_limit:
            status = "SPEEDING"
            status_color = "red"
            total_speeders += 1
        else:
            status = "Good"
            status_color = "green"

        total_speed_sum += speed
        avg_speed = total_speed_sum / (i + 1)

        progress_bar.progress((i+1) / num_cars)
        status_text.text(f"Processing car {i+1}/{num_cars}")

        with log_container:
            streamlit.markdown(f"""
        <div style="background: rgba(58, 134, 255, 0.1);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 5px 0;
                    border-left: 4px solid {status_color};">
            <strong> Car #{i+1}</strong> | Plate: <code>{plate}</code> | Speed: <strong>{speed} Km/h</strong> | {status}
        </div>
        """, unsafe_allow_html=True)
            
    total_cars_stat.metric("Total Cars", i+1)
    speeders_stat.metric("Speeders", total_speeders,
                            delta=f"{(total_speeders/(i+1)*100):.1f}%")
    avg_speed_stat.metric("Avg Speed", f"{avg_speed: .0f} km/h")

    streamlit.session_state.results.append({
        'plate': plate,
        'speed': speed,
        'status': status,
        'excess': max(0, speed - Speed_limit)
    })

    time.sleep(0.3)

status_text.success("Simulation Complete")
    
streamlit.markdown("---")
if stop_btn:
    if 'running' in streamlit.session_state:
        streamlit.session_state.running = False
    streamlit.success("Simulation end")
streamlit.markdown("---")