from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import random
import os
import csv
from datetime import datetime
import string

app = Flask(__name__)
app.config['SECRET_KEY'] = 'radar_secret_key_2025'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', logger=True, engineio_logger=True)

simulation_running = False
simulation_thread = None
cars_total = 0

Distance = 50.0
Speed_limit = 120
Num_cars = 30

def gen_one_car():
    numbers = ''.join(random.choices(string.digits, k=4))
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    region = random.randint(10, 99)
    plate = f"{numbers}|{letters}|{region}"
    speed = random.randint(80, 160)
    time_a = time.time()
    time_b = time_a + random.uniform(1.0, 3.0)
    return plate, time_a, time_b, speed

def process():
    pass

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    return jsonify({
        'distance': Distance,
        'speed_limit': Speed_limit,
        'num_cars': Num_cars
    })

@app.route('/api/config', methods=['POST'])
def update_config():
    global Distance, Speed_limit, Num_cars
    try:
        data = request.json
        Distance = float(data.get('distance', Distance))
        Speed_limit = int(data.get('speed_limit', Speed_limit))
        Num_cars = int(data.get('num_cars', Num_cars))
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/results', methods=['GET'])
def get_results():
    try:
        results_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'results.csv')
        if os.path.exists(results_path):
            results = []
            try:
                with open(results_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        results.append(row)
            except:
                return jsonify({'success': True, 'data': [], 'total': 0, 'speeders': 0})
            speeders = sum(1 for r in results if r.get('status') == 'High Speed')
            return jsonify({'success': True, 'data': results, 'total': len(results), 'speeders': speeders})
        return jsonify({'success': True, 'data': [], 'total': 0, 'speeders': 0})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

def simulation_loop():
    global simulation_running, cars_total, Speed_limit
    cars_total = 0
    
    print("[DEBUG] Simulation loop started")
    
    socketio.emit('log_message', {
        'message': '🚦 Radar System Started',
        'type': 'info',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }, namespace='/', broadcast=True)
    
    while simulation_running:
        try:
            print(f"[DEBUG] Loop iteration, random check: {random.random()}")
            
            if random.random() < 0.5:
                plate, time_a, time_b, speed = gen_one_car()
                cars_total += 1
                status = 'Speeding!!' if speed > Speed_limit else 'Good'
                msg_type = 'speeding' if speed > Speed_limit else 'normal'
                
                car_data = {
                    'car_number': cars_total,
                    'plate': plate,
                    'speed': speed,
                    'status': status,
                    'type': msg_type,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                }
                
                print(f"[DEBUG] Emitting car: {car_data}")
                socketio.emit('car_detected', car_data, namespace='/', broadcast=True)
            
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Simulation error: {str(e)}")
            socketio.emit('log_message', {
                'message': f'❌ Error: {str(e)}',
                'type': 'error',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            }, namespace='/', broadcast=True)
            time.sleep(1)
    
    print("[DEBUG] Simulation loop ended")

@socketio.on('start_simulation')
def handle_start_simulation():
    global simulation_running, simulation_thread
    print("[DEBUG] Received start_simulation event")
    if not simulation_running:
        simulation_running = True
        simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
        simulation_thread.start()
        print("[DEBUG] Simulation thread started")
        emit('simulation_started', {'message': 'Simulation started'}, broadcast=True)

@socketio.on('stop_simulation')
def handle_stop_simulation():
    global simulation_running
    print("[DEBUG] Received stop_simulation event")
    if simulation_running:
        simulation_running = False
        emit('simulation_stopped', {'message': 'Simulation stopped'}, broadcast=True)
        emit('log_message', {
            'message': '🛑 Radar System Stopped',
            'type': 'info',
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }, broadcast=True)

@socketio.on('connect')
def handle_connect():
    print("[DEBUG] Client connected")
    emit('log_message', {
        'message': '✅ Connected to Radar System',
        'type': 'success',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@socketio.on_error_default
def default_error_handler(e):
    print(f'[ERROR] SocketIO Error: {str(e)}')

if __name__ == '__main__':
    try:
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
    except:
        pass
    port = int(os.environ.get('PORT', 5000))
    print(f"[DEBUG] Starting server on port {port}")
    socketio.run(app, host='0.0.0.0', port=port, debug=True, allow_unsafe_werkzeug=True)
