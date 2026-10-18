import sys
import os
import subprocess
import winsound
import psutil
import pygame  # غنخدمو بيها باش نطلقو الصوت بجودة عالية
from PySide6.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu
from PySide6.QtGui import QAction
from PySide6.QtCore import QThreadPool, QTimer

from core.brain import Brain
from gui.overlay import FloatingOverlay
from gui.worker import WakeWordWorker, VoiceWorker, AIWorker

# ---------------------------------------------------------
# نظام الصوت السينمائي الجديد (Edge-TTS)
# ---------------------------------------------------------
class TTS:
    def __init__(self):
        pygame.mixer.init()
        # عزلنا صوت بريطاني فخم ديال راجل (Ryan)
        self.voice = "en-GB-RyanNeural"
        os.makedirs("data", exist_ok=True)
        self.audio_file = "data/response.mp3"
        
    def speak(self, text):
        try:
            # كنستعملو Edge-TTS باش نحولو الهضرة لملف MP3 (بدون نافذة سوداء)
            subprocess.run(
                ["edge-tts", "--voice", self.voice, "--text", text, "--write-media", self.audio_file], 
                check=True, 
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            
            # كنشغلو الصوت بـ Pygame
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            
            # كنبقاو نتسناو حتى يسالي الصوت عاد ندوزو
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
                
            # كنسدو الملف باش نقدرو نمسحوه ولا نكتبو عليه المرة الجاية
            pygame.mixer.music.unload()
            
        except Exception as e:
            print(f"Edge-TTS Error: {e}")
            # Fall back to Windows' built-in speech engine without pyttsx3.
            try:
                import base64

                encoded_text = base64.b64encode(text.encode("utf-8")).decode("ascii")
                script = (
                    "Add-Type -AssemblyName System.Speech; "
                    f"$text = [Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('{encoded_text}')); "
                    "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
                    "$speaker.Speak($text)"
                )
                encoded_script = base64.b64encode(script.encode("utf-16le")).decode("ascii")
                subprocess.run(
                    ["powershell", "-NoProfile", "-EncodedCommand", encoded_script],
                    check=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            except Exception as fallback_error:
                print(f"Fallback TTS Error: {fallback_error}")

# ---------------------------------------------------------
# الواجهة الأساسية (JarvisWindow)
# ---------------------------------------------------------
class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JARVIS - Core")
        
        self.brain = Brain()
        self.tts = TTS()
        self.busy = False
        self.low_battery_warned = False
        
        self.overlay = FloatingOverlay()
        
        self.tray_icon = QSystemTrayIcon(self)
        tray_menu = QMenu()
        exit_action = QAction("Exit JARVIS", self)
        exit_action.triggered.connect(self.exit_app)
        tray_menu.addAction(exit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.proactive_monitor)
        self.monitor_timer.start(60000) 
        
        self.start_wake_word()


    def proactive_monitor(self):
        if self.busy: return 
        
        # 1. مراقبة الموارد (الباتري والرام)
        try:
            battery = psutil.sensors_battery()
            if battery:
                if battery.percent <= 20 and not battery.power_plugged and not self.low_battery_warned:
                    self.overlay.update_status("speaking")
                    self.tts.speak(f"Warning sir, battery is critically low at {battery.percent} percent.")
                    self.overlay.update_status("standby")
                    self.low_battery_warned = True
                elif battery.power_plugged:
                    self.low_battery_warned = False 
            
            ram = psutil.virtual_memory()
            if ram.percent > 90:
                self.overlay.update_status("speaking")
                self.tts.speak("Sir, system memory usage is critically high.")
                self.overlay.update_status("standby")
        except:
            pass

        # 2. مراقبة جدول الأعمال (Smart Scheduler)
        try:
            import json, os
            from datetime import datetime
            schedule_file = "data/schedule.json"
            if os.path.exists(schedule_file):
                with open(schedule_file, "r", encoding="utf-8") as f:
                    schedule_data = json.load(f)
                
                # كنجبدو الوقت ديال دابا (مثلا: 2026-10-18 18:00)
                now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
                updated = False
                
                for item in schedule_data:
                    # يلا كاين شي موعد فهاد الدقيقة ومازال ماتدارش
                    if not item.get("done") and item["time"].startswith(now_str):
                        self.overlay.update_status("speaking")
                        self.play_sfx("listen")
                        # كيقول الموعد ديالك
                        self.tts.speak(f"Reminder sir: It is time for {item['task']}")
                        self.overlay.update_status("standby")
                        
                        item["done"] = True
                        updated = True
                
                # يلا داز شي موعد، كنحفظو الملف باش مايعاودش يبرزطك بيه
                if updated:
                    with open(schedule_file, "w", encoding="utf-8") as f:
                        json.dump(schedule_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Schedule Monitor Error: {e}")

    def play_sfx(self, sound_type):
        try:
            if sound_type == "listen": winsound.Beep(1000, 150)
            elif sound_type == "processing": 
                winsound.Beep(600, 100)
                winsound.Beep(800, 100)
            elif sound_type == "error": winsound.Beep(300, 300)
        except:
            pass

    def exit_app(self):
        self.overlay.close()
        self.close()
        QApplication.quit()
        
    def start_wake_word(self):
        if self.busy: return
        self.overlay.update_status("standby")
        
        self.wake_worker = WakeWordWorker()
        self.wake_worker.signals.detected.connect(self.on_wake_word_detected)
        self.wake_worker.signals.error.connect(self.voice_error)
        QThreadPool.globalInstance().start(self.wake_worker)

    def on_wake_word_detected(self):
        self.busy = True
        self.overlay.update_status("speaking")
        self.play_sfx("listen")
        self.tts.speak("Yes sir?")
        self.start_voice()

    def start_voice(self):
        self.busy = True
        self.overlay.update_status("listening")
        
        worker = VoiceWorker()
        worker.signals.finished.connect(self._process_text)
        worker.signals.error.connect(self.voice_error)
        QThreadPool.globalInstance().start(worker)

    def voice_error(self, error_msg):
        self.busy = False
        self.overlay.update_status("standby")
        print(f"[{error_msg}]")
        self.play_sfx("error")
        self.start_wake_word()

    def _process_text(self, text, image_path=None):
        if not text or text.strip() == "":
            self.voice_error("No command detected.")
            return
            
        self.overlay.update_status("processing")
        self.play_sfx("processing")
        print(f"\nYou: {text}")
        
        worker = AIWorker(self.brain, text, image_path)
        worker.signals.finished.connect(self.ai_finished)
        worker.signals.error.connect(self.voice_error)
        QThreadPool.globalInstance().start(worker)

    def ai_finished(self, response):
        self.overlay.update_status("speaking")
        print(f"JARVIS: {response}")
        
        self.tts.speak(response)
        
        self.busy = False
        self.overlay.update_status("standby")
        self.start_wake_word()