from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import threading
import time
import random
import pandas
import os
import sys
from datetime import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from radar_conf import Distance, Speed_limit, Num_cars, radar_a_file, radar_b_file, results_file
from Data_simulator import gen_one_car
from Processor import process

app = Flask(__name__)
app.config['SECRET_KEY'] = 'radar_secret_key_2025'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# sim control
simulation_running = False
simulation_thread = None
cars_total = 0

@app.route('/')
def index():
    """Render the main dashboard"""
    return render_template('index.html')

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    import importlib
    import radar_conf
    importlib.reload(radar_conf)
    
    return jsonify({
        'distance': radar_conf.Distance,
        'speed_limit': radar_conf.Speed_limit,
        'num_cars': radar_conf.Num_cars
    })

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration settings"""
    try:
        data = request.json
        
        config_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'radar_conf.py')
        
        with open(config_path, 'r') as f:
            lines = f.readlines()
        
        # Update values
        new_lines = []
        for line in lines:
            if line.strip().startswith('Distance ='):
                new_lines.append(f"Distance = {float(data['distance'])}\n")
            elif line.strip().startswith('Speed_limit ='):
                new_lines.append(f"Speed_limit = {int(data['speed_limit'])}\n")
            elif line.strip().startswith('Num_cars ='):
                new_lines.append(f"Num_cars = {int(data['num_cars'])}\n")
            else:
                new_lines.append(line)
        
        # Write updated config
        with open(config_path, 'w') as f:
            f.writelines(new_lines)
        
        # Reload the module
        import importlib
        import radar_conf
        importlib.reload(radar_conf)
        
        return jsonify({'success': True, 'message': 'Configuration updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/results', methods=['GET'])
def get_results():
    """Get processed results"""
    try:
        # Path to results file
        results_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'results.csv')
        
        if os.path.exists(results_path):
            df = pandas.read_csv(results_path)
            return jsonify({
                'success': True,
                'data': df.to_dict('records'),
                'total': len(df),
                'speeders': len(df[df['status'] == 'High Speed'])
            })
        return jsonify({'success': True, 'data': [], 'total': 0, 'speeders': 0})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

def simulation_loop():
    """Main simulation loop - runs in background thread"""
    global simulation_running, cars_total
    
    cars_total = 0
    last_update = time.time()
    
    socketio.emit('log_message', {
        'message': '🚦 Radar System Started',
        'type': 'info',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })
    
    while simulation_running:
        try:

            import importlib
            import radar_conf
            importlib.reload(radar_conf)
            current_speed_limit = radar_conf.Speed_limit
            
            # Random car generation
            if random.random() < 0.3:
                plate, time_a, time_b, speed = gen_one_car()
                cars_total += 1
                
                if speed > current_speed_limit:
                    status = 'Speeding!!'
                    msg_type = 'speeding'
                else:
                    status = 'Good'
                    msg_type = 'normal'
                
                socketio.emit('car_detected', {
                    'car_number': cars_total,
                    'plate': plate,
                    'speed': speed,
                    'status': status,
                    'type': msg_type,
                    'timestamp': datetime.now().strftime('%H:%M:%S')
                })
            
            time.sleep(1 + random.random() * 2)
            
            now = time.time()
            if now - last_update > 10:
                try:
                    process()
                    socketio.emit('results_updated', {
                        'message': '📊 Results Updated',
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })
                except Exception as e:
                    socketio.emit('log_message', {
                        'message': f'⚠️ Processing error: {str(e)}',
                        'type': 'error',
                        'timestamp': datetime.now().strftime('%H:%M:%S')
                    })
                last_update = now
                
        except Exception as e:
            socketio.emit('log_message', {
                'message': f'❌ Simulation error: {str(e)}',
                'type': 'error',
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
            time.sleep(1)

@socketio.on('start_simulation')
def handle_start_simulation():
    """Start the radar simulation"""
    global simulation_running, simulation_thread
    
    if not simulation_running:
        simulation_running = True
        simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
        simulation_thread.start()
        emit('simulation_started', {'message': 'Simulation started successfully'})

@socketio.on('stop_simulation')
def handle_stop_simulation():
    """Stop the radar simulation"""
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
    """Handle client connection"""
    print('Client connected')
    emit('log_message', {
        'message': '✅ Connected to Radar System',
        'type': 'success',
        'timestamp': datetime.now().strftime('%H:%M:%S')
    })

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

if __name__ == '__main__':
    # Ensure data directory exists
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Run the app
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
