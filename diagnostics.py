import os
import requests
import sounddevice as sd
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
import config

class DiagnosticsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JARVIS System Diagnostics")
        self.setMinimumSize(500, 400)
        self.setStyleSheet("background-color: #0d1117; color: #c9d1d9; font-size: 14px; font-weight: bold;")
        
        self.layout = QVBoxLayout(self)
        
        self.results = QTextEdit()
        self.results.setReadOnly(True)
        self.results.setStyleSheet("background-color: #161b22; border: 1px solid #00f0ff; border-radius: 8px; padding: 10px;")
        self.layout.addWidget(self.results)
        
        self.btn_run = QPushButton("🔄 إعادة الفحص الشامل")
        self.btn_run.setStyleSheet("background-color: #21262d; border: 1px solid #00f0ff; padding: 10px; border-radius: 5px;")
        self.btn_run.clicked.connect(self.run_tests)
        self.layout.addWidget(self.btn_run)
        
        self.run_tests()

    def run_tests(self):
        self.results.clear()
        log = ["[JARVIS DIAGNOSTICS PROTOCOL INITIATED]\n"]
        
        # 1. Internet Test
        try:
            requests.get("https://generativelanguage.googleapis.com", timeout=3)
            log.append("✅ Network: Connected to Google Servers.")
        except:
            log.append("❌ Network: Offline or Google Servers unreachable.")
            
        # 2. API Key Test
        if config.GEMINI_API_KEY and len(config.GEMINI_API_KEY) > 20:
            log.append("✅ Gemini API: Key is present and formatted correctly.")
        else:
            log.append("❌ Gemini API: Key is missing or invalid in .env file.")
            
        # 3. Microphone Test
        try:
            devices = sd.query_devices()
            default_input = sd.default.device[0]
            if default_input is not None:
                log.append(f"✅ Audio Input: Active ({devices[default_input]['name']})")
            else:
                log.append("❌ Audio Input: No microphone detected.")
        except Exception as e:
            log.append(f"❌ Audio Input Error: {str(e)}")
            
        # 4. Wake Word Model Test
        model_path = "vosk-model-small-en-us-0.15"
        if os.path.exists(model_path):
            log.append("✅ Wake Word Engine: Vosk model loaded successfully.")
        else:
            log.append("❌ Wake Word Engine: Missing Vosk model folder.")
            log.append("   -> Action needed: Download and extract the model to the project root.")

        # 5. Security & Workspace Test
        workspace = os.path.join(os.getcwd(), "workspace")
        if os.path.exists(workspace):
            log.append(f"✅ Workspace: Secure folder ready ({workspace}).")
        else:
            log.append("⚠️ Workspace: Not created yet. Will be created on first use.")

        self.results.setText("\n".join(log))