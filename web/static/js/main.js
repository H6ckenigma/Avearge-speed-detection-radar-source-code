// Real-time WebSocket connection and UI logic

// Initialize Socket.IO connection
const socket = io();

// DOM Elements
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const settingsBtn = document.getElementById('settings-btn');
const clearBtn = document.getElementById('clear-btn');
const refreshResultsBtn = document.getElementById('refresh-results-btn');
const logContainer = document.getElementById('log-container');
const statusBar = document.getElementById('status-bar');
const statusText = document.getElementById('status-text');
const distanceValue = document.getElementById('distance-value');
const speedLimitValue = document.getElementById('speed-limit-value');
const totalCars = document.getElementById('total-cars');
const speedingCars = document.getElementById('speeding-cars');
const settingsModal = document.getElementById('settings-modal');
const closeModal = document.getElementById('close-modal');
const saveSettingsBtn = document.getElementById('save-settings-btn');
const cancelSettingsBtn = document.getElementById('cancel-settings-btn');
const resultsContainer = document.getElementById('results-container');

// State
let carCount = 0;
let speedingCount = 0;

// Load initial configuration
function loadConfig() {
    fetch('/api/config')
        .then(res => res.json())
        .then(data => {
            distanceValue.textContent = `${data.distance} km`;
            speedLimitValue.textContent = `${data.speed_limit} km/h`;
            document.getElementById('distance-input').value = data.distance;
            document.getElementById('speed-limit-input').value = data.speed_limit;
            document.getElementById('num-cars-input').value = data.num_cars;
        })
        .catch(err => console.error('Error loading config:', err));
}

// Update status bar
function updateStatus(message, isRunning = false) {
    statusText.textContent = message;
    if (isRunning) {
        statusBar.classList.add('running');
    } else {
        statusBar.classList.remove('running');
    }
}

// Add log message
function addLog(message, type = 'info', timestamp = null) {
    const logMessage = document.createElement('div');
    logMessage.className = `log-message ${type}`;
    
    const time = timestamp || new Date().toLocaleTimeString('en-US', { hour12: false });
    
    logMessage.innerHTML = `
        <span class="log-time">[${time}]</span>
        <span class="log-text">${message}</span>
    `;
    
    logContainer.appendChild(logMessage);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// Clear log
function clearLog() {
    logContainer.innerHTML = '';
    addLog('Log cleared', 'info');
}

// Load and display results
function loadResults() {
    fetch('/api/results')
        .then(res => res.json())
        .then(data => {
            if (data.success && data.data.length > 0) {
                displayResults(data.data);
            } else {
                resultsContainer.innerHTML = '<p class="no-data">No data available yet.</p>';
            }
        })
        .catch(err => {
            console.error('Error loading results:', err);
            resultsContainer.innerHTML = '<p class="no-data">Error loading results.</p>';
        });
}

// Display results in table
function displayResults(data) {
    const table = document.createElement('table');
    table.className = 'results-table';
    
    // Table header
    table.innerHTML = `
        <thead>
            <tr>
                <th>Plate</th>
                <th>City</th>
                <th>Speed</th>
                <th>Excess</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            ${data.slice(-20).reverse().map(row => `
                <tr style="color: ${row.status === 'High Speed' ? 'var(--color-danger)' : 'var(--color-success)'}">
                    <td>${row.plate}</td>
                    <td>${row.city}</td>
                    <td>${row.speed}</td>
                    <td>${row.excess} km/h</td>
                    <td><strong>${row.status}</strong></td>
                </tr>
            `).join('')}
        </tbody>
    `;
    
    resultsContainer.innerHTML = '';
    resultsContainer.appendChild(table);
}

// Socket.IO Event Handlers

socket.on('connect', () => {
    console.log('Connected to server');
    document.getElementById('connection-status').textContent = '● Connected';
    document.getElementById('connection-status').style.color = 'var(--color-success)';
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
    document.getElementById('connection-status').textContent = '● Disconnected';
    document.getElementById('connection-status').style.color = 'var(--color-danger)';
});

socket.on('log_message', (data) => {
    addLog(data.message, data.type, data.timestamp);
});

socket.on('car_detected', (data) => {
    carCount++;
    totalCars.textContent = carCount;
    
    if (data.type === 'speeding') {
        speedingCount++;
        speedingCars.textContent = speedingCount;
        addLog(
            `🚨 Car #${data.car_number} | ${data.plate} | ${data.speed} km/h >> ${data.status}`,
            'speeding',
            data.timestamp
        );
        
        // Play beep sound (you can add audio element if needed)
        playBeep();
    } else {
        addLog(
            `✅ Car #${data.car_number} | ${data.plate} | ${data.speed} km/h >> ${data.status}`,
            'normal',
            data.timestamp
        );
    }
});

socket.on('results_updated', (data) => {
    addLog(data.message, 'info', data.timestamp);
    loadResults();
});

socket.on('simulation_started', (data) => {
    updateStatus('Simulation running...', true);
    startBtn.disabled = true;
    stopBtn.disabled = false;
    carCount = 0;
    speedingCount = 0;
    totalCars.textContent = '0';
    speedingCars.textContent = '0';
});

socket.on('simulation_stopped', (data) => {
    updateStatus('Ready to start', false);
    startBtn.disabled = false;
    stopBtn.disabled = true;
});

// Button Event Handlers

startBtn.addEventListener('click', () => {
    socket.emit('start_simulation');
    clearLog();
});

stopBtn.addEventListener('click', () => {
    socket.emit('stop_simulation');
});

clearBtn.addEventListener('click', clearLog);

refreshResultsBtn.addEventListener('click', loadResults);

settingsBtn.addEventListener('click', () => {
    settingsModal.classList.add('active');
});

closeModal.addEventListener('click', () => {
    settingsModal.classList.remove('active');
});

cancelSettingsBtn.addEventListener('click', () => {
    settingsModal.classList.remove('active');
});

saveSettingsBtn.addEventListener('click', () => {
    const newConfig = {
        distance: parseFloat(document.getElementById('distance-input').value),
        speed_limit: parseInt(document.getElementById('speed-limit-input').value),
        num_cars: parseInt(document.getElementById('num-cars-input').value)
    };
    
    fetch('/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newConfig)
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            addLog('⚙ Settings updated successfully', 'info');
            loadConfig();
            settingsModal.classList.remove('active');
        } else {
            addLog(`❌ Error: ${data.error}`, 'error');
        }
    })
    .catch(err => {
        addLog(`❌ Error saving settings: ${err}`, 'error');
    });
});

// Close modal when clicking outside
settingsModal.addEventListener('click', (e) => {
    if (e.target === settingsModal) {
        settingsModal.classList.remove('active');
    }
});

// Beep sound function (simple beep using Web Audio API)
function playBeep() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.3);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.3);
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    loadConfig();
    loadResults();
    addLog('🚦 Radar System Initialized', 'info');
});
