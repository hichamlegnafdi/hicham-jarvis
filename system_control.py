import os
import subprocess
from AppOpener import open as open_app, close as close_app

class SystemController:
    def execute_command(self, command, target=""):
        try:
            if command == "OPEN_APP":
                open_app(target, match_closest=True)
                return f"Tm fet7 tatbiq {target} bnaja7."
            
            elif command == "CLOSE_APP":
                close_app(target, match_closest=True)
                return f"Tm ighlaq tatbiq {target} bnaja7."
            
            elif command == "MUTE":
                # Kikhdm b PowerShell bla may7taj nircmd.exe (Native Windows)
                ps_script = "$obj = new-object -com wscript.shell; $obj.SendKeys([char]173)"
                subprocess.run(["powershell", "-Command", ps_script], capture_output=True)
                return "Tm katm wla itla9 s-sawt (Mute/Unmute)."
            
            elif command == "SLEEP":
                os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                return "Tsb7 3la khir, ghandkhol f wed3 n-noum."
                
            elif command == "BATTERY_STATUS":
                # Miza jdida: Jarvis ki3ref ch7al f l-batterie
                ps_script = "Get-CimInstance -ClassName Win32_Battery | Select-Object -ExpandProperty EstimatedChargeRemaining"
                result = subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True)
                battery = result.stdout.strip()
                if battery:
                    return f"Nisbat l-batterie hiya {battery}%."
                return "L-batterie makaynach (PC Fixe wla fih mochkil)."
                
            else:
                return "3odran, ma3reftch had l-amr."
                
        except Exception as e:
            return f"W9e3 khata2 f tanfid l-amr: {str(e)}"