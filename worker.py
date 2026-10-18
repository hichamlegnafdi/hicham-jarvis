import sys
import queue
import json
import os
import sounddevice as sd
import speech_recognition as sr
from vosk import Model, KaldiRecognizer
from PySide6.QtCore import QRunnable, QObject, Signal

# ---------------------------------------------------------
# 1. إشارات العمال (Signals) باش يتواصلو مع الواجهة
# ---------------------------------------------------------
class WorkerSignals(QObject):
    finished = Signal(str)
    error = Signal(str)

class WakeWordSignals(QObject):
    detected = Signal()
    error = Signal(str)
    status_update = Signal(str)

# ---------------------------------------------------------
# 2. عامل الذكاء الاصطناعي (AI Worker) - كيتكلف بالتفكير
# ---------------------------------------------------------
class AIWorker(QRunnable):
    def __init__(self, brain, prompt, image_path=None):
        super().__init__()
        self.brain = brain
        self.prompt = prompt
        self.image_path = image_path
        self.signals = WorkerSignals()

    def run(self):
        try:
            # صيفط الطلب للعقل (Brain) وجيب النتيجة
            response = self.brain.process(self.prompt, self.image_path)
            self.signals.finished.emit(response)
        except Exception as e:
            self.signals.error.emit(f"AI Error: {str(e)}")

# ---------------------------------------------------------
# 3. عامل المايكروفون (Voice Worker) - كيتكلف يحول الهضرة لنص
# ---------------------------------------------------------
class VoiceWorker(QRunnable):
    def __init__(self, language="ar-MA", timeout=5):
        super().__init__()
        self.signals = WorkerSignals()
        self.language = language
        self.timeout = timeout

    def run(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=self.timeout, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language=self.language)
                self.signals.finished.emit(text)
            except sr.WaitTimeoutError:
                self.signals.error.emit("TIMEOUT")
            except sr.UnknownValueError:
                self.signals.error.emit("UNKNOWN")
            except Exception as e:
                self.signals.error.emit(f"Microphone Error: {str(e)}")

# ---------------------------------------------------------
# 4. عامل الاستماع الدائم (Wake Word Worker) - كيتسنى "Jarvis"
# ---------------------------------------------------------
class WakeWordWorker(QRunnable):
    def __init__(self, voice_engine=None):
        super().__init__()
        self.signals = WakeWordSignals()
        self.active = True
        self.paused = False
        self.q = queue.Queue()
        self.model_path = "vosk-model-small-en-us-0.15" 
        self.wake_words = ["jarvis", "travis", "service", "garbage", "charlie", "jervis"]

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        if not self.paused:
            self.q.put(bytes(indata))

    def run(self):
        if not os.path.exists(self.model_path):
            self.signals.error.emit(f"❌ Vosk Model missing! Please extract '{self.model_path}' in the project root.")
            return

        try:
            self.signals.status_update.emit("⏳ Loading Wake Word Model...")
            model = Model(self.model_path)
            recognizer = KaldiRecognizer(model, 16000)
            
            self.signals.status_update.emit("🟢 Auto-Listen: WAITING FOR 'JARVIS'...")
            
            with sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, dtype='int16',
                                   channels=1, callback=self.audio_callback):
                while self.active:
                    if self.paused:
                        while not self.q.empty():
                            self.q.get()
                        sd.sleep(100)
                        continue

                    data = self.q.get()
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        text = result.get("text", "").lower()
                        
                        if any(w in text for w in self.wake_words):
                            print(f"🔥 WAKE WORD DETECTED: {text}")
                            self.paused = True
                            self.signals.detected.emit()
                            
        except Exception as e:
            self.signals.error.emit(f"Wake Word Error: {str(e)}")