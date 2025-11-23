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
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

simulation_running = False
simulation_thread = None
cars_total = 0

Distance = 50.0
Speed_limit = 120
Num_cars = 30

def gen_one_car():
    numbers = ''.join(random.choices(string.digits, k=6))
    letter = random.choice("ABDEFG")
    region = random.randint(1, 58)
    plate = f"{numbers}|{letter}|{region}"
    
    speed = random.randint(80, 160)
    time_a = time.time()
    time_delay = (Distance / speed) * 3600 + random.uniform(-0.5, 0.5)
    time_b = time_a + time_delay
    
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    radar_a_path = os.path.join(data_dir, 'radar_a.csv')
    radar_b_path = os.path.join(data_dir, 'radar_b.csv')
    
    try:
        file_a_exists = os.path.exists(radar_a_path) and os.path.getsize(radar_a_path) > 0
    except:
        file_a_exists = False
    
    try:
        file_b_exists = os.path.exists(radar_b_path) and os.path.getsize(radar_b_path) > 0
    except:
        file_b_exists = False
    
    with open(radar_a_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_a_exists:
            writer.writerow(['Plate', 'Timestamp'])
        writer.writerow([plate, time_a])
    
    with open(radar_b_path, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_b_exists:
            writer.writerow(['Plate', 'Timestamp'])
        writer.writerow([plate, time_b])
    
    return plate, time_a, time_b, speed

def process():
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    radar_a_path = os.path.join(data_dir, 'radar_a.csv')
    radar_b_path = os.path.join(data_dir, 'radar_b.csv')
    results_path = os.path.join(data_dir, 'results.csv')
    
    if not os.path.exists(radar_a_path) or not os.path.exists(radar_b_path):
        return
    
    radar_a_data = {}
    radar_b_data = {}
    
    try:
        with open(radar_a_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                radar_a_data[row['Plate']] = float(row['Timestamp'])
    except Exception as e:
        print(f"Error reading radar_a: {e}")
        return
    
    try:
        with open(radar_b_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                radar_b_data[row['Plate']] = float(row['Timestamp'])
    except Exception as e:
        print(f"Error reading radar_b: {e}")
        return
    
    results = []
    for plate in radar_a_data:
        if plate in radar_b_data:
            time_a = radar_a_data[plate]
            time_b = radar_b_data[plate]
            time_diff = abs(time_b - time_a) / 3600
            
            if time_diff > 0:
                speed = int(Distance / time_diff)
                status = 'High Speed' if speed > Speed_limit else 'Good'
                results.append({
                    'plate': plate,
                    'speed': speed,
                    'status': status,
                    'time_a': time_a,
                    'time_b': time_b
                })
    
    with open(results_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['plate', 'speed', 'status', 'time_a', 'time_b'])
        writer.writeheader()
        writer.writerows(results)

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
            except Exception as csv_error:
                print(f"CSV read error: {csv_error}")
                return jsonify({'success': True, 'data': [], 'total': 0, 'speeders': 0})
            speeders = sum(1 for r in results if r.get('status') == 'High Speed')
            return jsonify({'success': True, 'data': results, 'total': len(results), 'speeders': speeders})
        return jsonify({'success': True, 'data': [], 'total': 0, 'speeders': 0})
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/process', methods=['POST'])
def trigger_process():
    try:
        process()
        return jsonify({'success': True, 'message': 'Results processed successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

def simulation_loop():
    global simulation_running, cars_total, Speed_limit
    cars_total = 0
    last_update = time.time()
    
    socketio.emit('log_message', {
        'message': '🚦 Radar System Started',
        'type': 'info',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })
    
    while simulation_running:
        try:
            if random.random() < 0.5:
                plate, time_a, time_b, speed = gen_one_car()
                cars_total += 1
                status = 'Speeding!!' if speed > Speed_limit else 'Good'
                msg_type = 'speeding' if speed > Speed_limit else 'normal'
                
                socketio.emit('car_detected', {
                    'car_number': cars_total,
                    'plate': plate,
                    'speed': speed,
                    'status': status,
                    'type': msg_type,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
            
            time.sleep(1.5)
            
            now = time.time()
            if now - last_update > 10:
                try:
                    process()
                    socketio.emit('results_updated', {
                        'message': '📊 Results Updated',
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })
                except Exception as proc_error:
                    print(f"Processing error: {proc_error}")
                last_update = now
        except Exception as e:
            socketio.emit('log_message', {
                'message': f'❌ Error: {str(e)}',
                'type': 'error',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            time.sleep(1)

@socketio.on('start_simulation')
def handle_start_simulation():
    global simulation_running, simulation_thread
    if not simulation_running:
        simulation_running = True
        simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
        simulation_thread.start()
        emit('simulation_started', {'message': 'Simulation started'})

@socketio.on('stop_simulation')
def handle_stop_simulation():
    global simulation_running
    if simulation_running:
        simulation_running = False
        emit('simulation_stopped', {'message': 'Simulation stopped'})
        emit('log_message', {
            'message': '🛑 Radar System Stopped',
            'type': 'info',
            'timestamp': datetime.now().strftime('%H:%M:%S')
        })

@socketio.on('connect')
def handle_connect():
    emit('log_message', {
        'message': '✅ Connected to Radar System',
        'type': 'success',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@socketio.on_error_default
def default_error_handler(e):
    print(f'SocketIO Error: {str(e)}')

if __name__ == '__main__':
    try:
        os.makedirs(os.path.join(os.path.dirname(__file__), '..', 'data'), exist_ok=True)
    except:
        pass
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
