import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json

# 1. Configuration (Bdl hadchi 3la 7sab l-projet dyalk)
MODEL_PATH = "vosk-model-small-en-us-0.15"  
WAKE_WORD = "jarvis"                   
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# 2. Chargement dyal l-modèle
print("⏳ Chargement dyal l-modèle Vosk...")
try:
    model = Model(MODEL_PATH)
except Exception as e:
    print(f"❌ Erreur: L-modèle mal9inahch f '{MODEL_PATH}'. T2ked mn smit l-dossier!")
    sys.exit(1)

# N7dedo vocabulaire ghir f l-mot clé bash yzreb f l-mou3alaja (Latence m-optimisya)
recognizer = KaldiRecognizer(model, 16000, f'["{WAKE_WORD}", "[unk]"]')

print(f"🟢 Système waajed ! Kan-tsna tsmi3 l-mot clé : '{WAKE_WORD}'...")

# 3. Boucle d'écoute b sounddevice
try:
    with sd.RawInputStream(samplerate=16000, blocksize=8000, device=None, dtype='int16',
                           channels=1, callback=callback):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "")
                
                # Vérifi wesh l-mot clé t-gal
                if WAKE_WORD in text:
                    print(f"🔥 Wake word '{WAKE_WORD}' tsme3 ! Activation dyal l-projet...")
                    # Hna ghadi n-zidou l-code li ghadi y-lanci Gemini wla l-module l-akhor
                    break
except KeyboardInterrupt:
    print("\n🛑 L-programme t7bess.")
except Exception as e:
    print(f"❌ Mochkil f l-micro: {e}")