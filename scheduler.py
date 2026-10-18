import time
import datetime
import os
from PySide6.QtCore import QThread, Signal

class ReminderWorker(QThread):
    reminder_triggered = Signal(str)

    def __init__(self):
        super().__init__()
        self.active = True
        self.reminders_file = "data/reminders.txt"
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(self.reminders_file):
            open(self.reminders_file, 'w', encoding="utf-8").close()

    def run(self):
        while self.active:
            now = datetime.datetime.now().strftime("%H:%M")
            try:
                with open(self.reminders_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                remaining = []
                for line in lines:
                    line = line.strip()
                    if not line: continue
                    
                    # Kayfhem l-we9t w l-message (mefro9in b | wla espace)
                    parts = line.split("|") if "|" in line else line.split(" ", 1)
                    if len(parts) >= 2:
                        r_time = parts[0].strip()
                        r_msg = parts[1].strip()
                        
                        if r_time == now:
                            # Sifat s-signal l-Jarvis bach y-hder
                            self.reminder_triggered.emit(f"تذكير مهم: {r_msg}")
                        else:
                            remaining.append(line)
                    else:
                        remaining.append(line)
                        
                with open(self.reminders_file, "w", encoding="utf-8") as f:
                    f.write("\n".join(remaining) + "\n" if remaining else "")
                    
            except Exception as e:
                pass
                
            time.sleep(30) # Kay9eleb kola 30 tanya