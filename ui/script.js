const chatOutput = document.getElementById('chat-output');
const voiceBtn = document.getElementById('voice-btn');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const historyToggle = document.getElementById('history-toggle');
const historyPanel = document.getElementById('history-panel');
const closeHistory = document.getElementById('close-history');
const historyContent = document.getElementById('history-content');

const API_BASE_URL = `${window.location.protocol}//${window.location.hostname}:8000/api`;
let conversationHistory = []; // Stores the full session history

function addMessage(text, saveToHistory = true) {
    // Show on HUD (Temporary)
    const msgDiv = document.createElement('div');
    msgDiv.className = 'jarvis-msg';
    msgDiv.textContent = text;
    chatOutput.appendChild(msgDiv);
    vibratePhone(50);

    // Save to permanent Archive
    if (saveToHistory) {
        addToHistory('Jarvis', text);
    }

    // Auto-scroll to latest message if needed
    chatOutput.scrollTop = chatOutput.scrollHeight;

    // Fade out and remove after 10 seconds to keep HUD clean
    setTimeout(() => {
        msgDiv.style.opacity = '0';
        setTimeout(() => {
            if (msgDiv.parentNode) msgDiv.remove();
        }, 1000);
    }, 10000);
}

async function handleCommand(text) {
    if (!text) return;

    // Clear input field immediately
    userInput.value = '';

    // Save user message to history
    addToHistory('User', text);

    // Add thinking animation
    const reactor = document.querySelector('.arc-reactor');
    if (reactor) reactor.classList.add('thinking');

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: text }),
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        reactor.classList.remove('thinking');
        addMessage(data.response); // This also saves to history
        speak(data.response);

        // Handle Server-Side Actions (for AI triggers)
        if (data.action === "open_camera") openCamera();
        if (data.action === "request_location") requestLocation();

    } catch (error) {
        reactor.classList.remove('thinking');
        console.error('Error:', error);
        addMessage("Sir, connection to core is unstable.", false);
    }
}

function addToHistory(sender, text) {
    conversationHistory.push({ sender, text, timestamp: new Date().toLocaleTimeString() });
    renderHistory();
}

function renderHistory() {
    historyContent.innerHTML = '';
    conversationHistory.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.className = `hist-item ${item.sender === 'User' ? 'hist-user' : 'hist-jarvis'}`;
        itemDiv.innerHTML = `<strong>${item.sender}:</strong> ${item.text}`;
        historyContent.appendChild(itemDiv);
    });
    historyContent.scrollTop = historyContent.scrollHeight;
}

function speak(text) {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel(); // Stop any current speech
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1.0;
        utterance.pitch = 0.95;
        window.speechSynthesis.speak(utterance);
    }
}

// Event Listeners
historyToggle.addEventListener('click', () => {
    historyPanel.classList.remove('hidden');
});

closeHistory.addEventListener('click', () => {
    historyPanel.classList.add('hidden');
});

sendBtn.addEventListener('click', () => handleCommand(userInput.value.trim()));

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleCommand(userInput.value.trim());
});

voiceBtn.addEventListener('click', () => {
    if ('webkitSpeechRecognition' in window) {
        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';

        voiceBtn.innerHTML = '<span class="mic-icon">🛑</span> <span class="btn-text">Listening...</span>';
        voiceBtn.style.background = "#ff4b2b";

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            handleCommand(transcript);
        };

        recognition.onend = () => {
            voiceBtn.innerHTML = '<span class="mic-icon">🎤</span> <span class="btn-text">Click here to speak</span>';
            voiceBtn.style.background = "";
        };

        recognition.start();
    } else {
        alert("Please use Chrome for voice features.");
    }
});

// 3D Parallax Effect
document.addEventListener('mousemove', (e) => {
    const container = document.querySelector('.hologram-container');
    if (!container) return;
    const xAxis = (window.innerWidth / 2 - e.pageX) / 25;
    const yAxis = (window.innerHeight / 2 - e.pageY) / 25;

    container.style.transform = `rotateY(${xAxis}deg) rotateX(${yAxis}deg)`;
});

// Audio Management
const ambientAudio = new Audio('https://www.soundjay.com/mechanical/sounds/mechanical-hum-1.mp3'); // Example hum
ambientAudio.loop = true;
ambientAudio.volume = 0.2;

function playStartupSound() {
    const startup = new Audio('https://www.soundjay.com/communication/sounds/digital-beeps-1.mp3');
    startup.volume = 0.5;
    startup.play().catch(e => console.log("Audio play blocked by browser. Click anywhere to start."));
}

function toggleAmbient() {
    if (ambientAudio.paused) {
        ambientAudio.play();
    } else {
        ambientAudio.pause();
    }
}

// Theme Management
function changeTheme(theme) {
    document.body.classList.remove('mark1-theme', 'mark2-theme', 'mark42-theme', 'stealth-theme', 'nano-theme');
    const btns = document.querySelectorAll('.theme-btn');
    btns.forEach(b => b.classList.remove('active'));

    const selector = theme === 'alpha' ? '.theme-btn[title*="Alpha"]' : `.theme-btn.${theme}`;
    const activeBtn = document.querySelector(selector);
    if (activeBtn) activeBtn.classList.add('active');

    if (theme !== 'alpha') {
        document.body.classList.add(`${theme}-theme`);
    }
}

// Mobile Hardware Control
function vibratePhone(duration = 200) {
    if ("vibrate" in navigator) {
        navigator.vibrate(duration);
    }
}

// System Stats Polling
async function updateSystemStats() {
    try {
        // Try to get local battery if on mobile
        if ("getBattery" in navigator) {
            const battery = await navigator.getBattery();
            document.getElementById('bat-bar').style.width = `${battery.level * 100}%`;
        }

        const response = await fetch(`${API_BASE_URL}/system`);
        if (response.ok) {
            const stats = await response.json();
            document.getElementById('cpu-bar').style.width = `${stats.cpu}%`;
            document.getElementById('ram-bar').style.width = `${stats.ram}%`;

            // If we didn't get local battery, use server battery
            if (!("getBattery" in navigator)) {
                document.getElementById('bat-bar').style.width = `${stats.battery}%`;
            }
        }
    } catch (e) {
        console.error("Stat fetch failed");
    }
}

// Mock Weather/News (Can be replaced with real API keys)
function updateEnvironment() {
    document.getElementById('weather-info').textContent = `TEMP: 24°C | HUMID: 45%`;
    document.getElementById('news-info').textContent = `NEWS: STARK EXPO ANNOUNCED`;
}

// Notification Bridge Polling
async function updateNotifications() {
    try {
        const response = await fetch(`${API_BASE_URL}/notifications`);
        if (response.ok) {
            const newNotifs = await response.json();
            if (newNotifs.length > 0) {
                const list = document.getElementById('notif-list');
                const emptyMsg = list.querySelector('.notif-empty');
                if (emptyMsg) emptyMsg.remove();

                newNotifs.forEach(n => {
                    const item = document.createElement('div');
                    item.className = 'notif-item';
                    item.innerHTML = `
                        <div class="notif-title">${n.app}: ${n.title}</div>
                        <div class="notif-body">${n.body}</div>
                    `;
                    list.prepend(item);

                    // Cleanup old notifs if list is too long
                    if (list.children.length > 5) list.lastElementChild.remove();

                    // Voice announcement if not already speaking
                    if (!window.speechSynthesis.speaking) {
                        speak(`Sir, you have a new notification from ${n.app}. It says: ${n.title}`);
                    }
                });
            }
        }
    } catch (e) {
        console.error("Notif fetch failed");
    }
}

// Sensor Suite Logic
function requestLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
            const { latitude, longitude } = position.coords;
            document.getElementById('location-info').textContent = `GPS: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
            addMessage(`Sir, coordinates secured: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`, false);
            speak(`Coordinates secured, Sir. We are currently at ${latitude.toFixed(2)} degrees latitude.`);
        }, (err) => {
            addMessage("Sir, I'm unable to access the GPS satellites.", false);
        });
    }
}

function triggerFileSelect() {
    document.getElementById('file-input').click();
}

function handleFileUpload(input) {
    const file = input.files[0];
    if (file) {
        addMessage(`Sir, I've received the file: ${file.name}. Commencing analysis...`, false);
        // In a real app, you'd send this to the server
    }
}

// Camera / Visual Scan
let stream = null;
async function openCamera() {
    const overlay = document.getElementById('camera-overlay');
    const video = document.getElementById('webcam');
    overlay.classList.remove('hidden');

    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        addMessage("Visual scan mode active. Scanning for anomalies.", false);
        speak("Visual scan mode active, Sir.");
    } catch (err) {
        addMessage("Sir, the optical sensors are offline.", false);
        overlay.classList.add('hidden');
    }
}

function closeCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    document.getElementById('camera-overlay').classList.add('hidden');
    addMessage("Visual scan terminated.", false);
}

// Browser Notifications
function sendBrowserNotification(title, body) {
    if ("Notification" in window) {
        if (Notification.permission === "granted") {
            new Notification(title, { body, icon: "https://cdn4.iconfinder.com/data/icons/artificial-intelligence-6/64/Artificial_Intelligence_brain_cogs_head_mind-512.png" });
        } else if (Notification.permission !== "denied") {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    sendBrowserNotification(title, body);
                }
            });
        }
    }
}

// Command Interceptor for Sensors
const originalHandleCommand = handleCommand;
handleCommand = function (text) {
    const lowText = text.toLowerCase();

    if (lowText.includes("scan") || lowText.includes("camera") || lowText.includes("vision")) {
        openCamera();
        return;
    }

    if (lowText.includes("where am i") || lowText.includes("location") || lowText.includes("gps")) {
        requestLocation();
        return;
    }

    if (lowText.includes("upload") || lowText.includes("file")) {
        triggerFileSelect();
        return;
    }

    originalHandleCommand(text);
};

window.onload = async () => {
    // Existing window.onload logic...
    // Start Polling
    setInterval(updateSystemStats, 3000);
    setInterval(updateNotifications, 5000);
    updateEnvironment();

    // Audio Start
    playStartupSound();
    ambientAudio.play().catch(() => { }); // Usually needs interaction

    // Fetch persistent history...
    try {
        const response = await fetch(`${API_BASE_URL}/history`);
        if (response.ok) {
            const history = await response.json();
            conversationHistory = history;
            renderHistory();
        }
    } catch (e) {
        console.error("Could not load history:", e);
    }

    setTimeout(() => {
        addMessage("Systems initialized. Welcome back, Sir.", false);
        speak("Systems initialized. Welcome back, Sir.");

        // Request Permissions
        if ("Notification" in window) Notification.requestPermission();
    }, 1000);
};
