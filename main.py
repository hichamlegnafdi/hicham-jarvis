import sys
import os
from PySide6.QtWidgets import QApplication
from gui.window import JarvisWindow

def main():
    os.makedirs("data", exist_ok=True)
    os.makedirs("workspace", exist_ok=True)
    
    app = QApplication(sys.argv)
    window = JarvisWindow()
    
    # حيدنا window.show() باش ما تطلعش الشاشة الكبيرة
    window.overlay.show() # كيبين غير الإيموجي العائم
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()