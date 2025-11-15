import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime, timedelta
from Data_simulator import gen_plate
from radar_conf import Distance, Speed_limit, Num_cars

# Page config
st.set_page_config(
    page_title="Radar Enigma",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0d1b2a 0%, #1b263b 100%);
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

st.markdown("# Radar Enigma")
st.markdown("### Average Speed Detection System")
st.markdown("---")

# Sidebar settings
st.sidebar.header("Configuration")
distance = st.sidebar.slider("Distance Between Radars (km)", 10, 200, int(Distance))
speed_limit = st.sidebar.slider("Speed Limit (km/h)", 60, 180, Speed_limit)
num_cars = st.sidebar.slider("Number of cars to simulate", 5, 50, min(Num_cars, 20))

# Display metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #3a86ff;"> Distance</h3>
        <h2 style="color: #e0e1dd;">{distance} km</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #3a86ff;"> Speed Limit</h3>
        <h2 style="color: #e0e1dd;">{speed_limit} km/h</h2>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown(f"""
    <div class="metric-card">
        <h3 style="color: #3a86ff;"> Cars</h3>
        <h2 style="color: #e0e1dd;">{num_cars}</h2>
    </div>              
    """, unsafe_allow_html=True)
    
st.markdown("---")

# buttons
col1, col2, col3 = st.columns([1, 1, 3])
with col1:
    start_btn = st.button("Start Simulation", use_container_width=True)
with col2:
    clear_btn = st.button("Clear Results", use_container_width=True)

st.markdown("---")

st.subheader("Live Detections")

# Clear results
if clear_btn:
    st.session_state.results = []
    st.success("Results cleared!")
    st.rerun()

if start_btn:
    if 'results' not in st.session_state:
        st.session_state.results = []
    
    st.session_state.results = []
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    log_container = st.container()
    
    # Stats columns
    stats_col1, stats_col2, stats_col3 = st.columns(3)
    total_cars_stat = stats_col1.empty()
    speeders_stat = stats_col2.empty()
    avg_speed_stat = stats_col3.empty()
    
    total_speeders = 0
    total_speed_sum = 0
    
    # Run simulation
    for i in range(num_cars):
        plate = gen_plate()
        speed = random.randint(80, 160)
        
        time_seconds = (distance / speed) * 3600
        
        if speed > speed_limit:
            status = "SPEEDING"
            status_color = "red"
            total_speeders += 1
        else:
            status = "Good"
            status_color = "green"
        
        total_speed_sum += speed
        avg_speed = total_speed_sum / (i + 1)
        
        progress_bar.progress((i + 1) / num_cars)
        status_text.text(f"Processing car {i + 1}/{num_cars}...")
        
        # Display in log
        with log_container:
            st.markdown(f"""
            <div style="background: rgba(58, 134, 255, 0.1);
                        padding: 15px;
                        border-radius: 10px;
                        margin: 5px 0;
                        border-left: 4px solid {status_color};">
                <strong>Car #{i + 1}</strong> | Plate: <code>{plate}</code> | 
                Speed: <strong>{speed} km/h</strong> | {status}
            </div>
            """, unsafe_allow_html=True)
        
        total_cars_stat.metric("Total Cars", i + 1)
        speeders_stat.metric("Speeders", total_speeders, 
                            delta=f"{(total_speeders/(i+1)*100):.1f}%")
        avg_speed_stat.metric("Avg Speed", f"{avg_speed:.0f} km/h")
        

        st.session_state.results.append({
            'plate': plate,
            'speed': speed,
            'status': status,
            'excess': max(0, speed - speed_limit)
        })
        

        time.sleep(0.3)
    
    # Complete
    status_text.success("Simulation Complete!")
    
    # Show results table
    st.markdown("---")
    st.subheader("Results Summary")
    
    if len(st.session_state.results) > 0:
        results_df = pd.DataFrame(st.session_state.results)
        
        # Tabs
        tab1, tab2 = st.tabs(["All Data", "Statistics"])
        
        with tab1:
            st.dataframe(results_df, use_container_width=True)
        
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Speed Distribution")
                st.bar_chart(results_df['speed'])
            
            with col2:
                st.markdown("#### Statistics")
                st.write(results_df[['speed', 'excess']].describe())

else:
    # Show welcome message
    st.info("Click 'Start Simulation' to begin")
    
    # Instructions
    with st.expander("How It Works"):
        st.markdown("""
        ### Average Speed Detection System
        
        This project simulates a radar speed detection system. The idea is that two radar points, A and B, detect a car’s
        license plate as it passes by. The system records the exact time 
        when the car is seen at each point, then calculates the average speed based on the distance between the two radars
        and the time difference and if the calculated speed is higher than the allowed speed limit, the system automatically flags it as overspeeding (High Speed in the code so far) case

        **This system cannot be bypassed** because it measures average speed over the entire 
        distance, not just at a single point!
        """)
    
    with st.expander("🇲🇦 About This Project"):
        st.markdown("""
        
        **Problem:** Single-point radars are easily bypassed using navigation apps
        
        **Solution:** Average speed cameras proven to reduce accidents by 40-60%
  
        🔗 GitHub: [View Source Code](https://github.com/H6ckenigma/New_radr_system/)
        """)


st.markdown("---")
