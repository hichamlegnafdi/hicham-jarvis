from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QFont

class FloatingOverlay(QWidget):
    def __init__(self):
        super().__init__()
        # إعدادات باش تبقى الواجهة ديما الفوق وبلا إطار وشفافة
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.emoji_label = QLabel("🤖")
        self.emoji_label.setFont(QFont("Segoe UI Emoji", 35))
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setStyleSheet("""
            color: #00f0ff; 
            background: rgba(13, 17, 23, 180); 
            border: 2px solid #00f0ff; 
            border-radius: 30px; 
            padding: 10px;
        """)
        layout.addWidget(self.emoji_label)
        
        self.resize(70, 70)
        self.oldPos = self.pos()

    # دوال باش تقدر تجر الإيموجي فاي بلاصة فـ الشاشة
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def update_status(self, status):
        """تغيير الإيموجي على حسب حالة Jarvis"""
        if status == "listening":
            self.emoji_label.setText("🟢") # كيتصنت
            self.emoji_label.setStyleSheet("background: rgba(0, 255, 0, 0.2); border: 2px solid #00ff00; border-radius: 30px; padding: 10px;")
        elif status == "processing":
            self.emoji_label.setText("⏳") # كيفكر
            self.emoji_label.setStyleSheet("background: rgba(255, 165, 0, 0.2); border: 2px solid #ffa500; border-radius: 30px; padding: 10px;")
        elif status == "speaking":
            self.emoji_label.setText("🗣️") # كيهضر
            self.emoji_label.setStyleSheet("background: rgba(0, 240, 255, 0.2); border: 2px solid #00f0ff; border-radius: 30px; padding: 10px;")
        else:
            self.emoji_label.setText("🤖") # واجد (Standby)
            self.emoji_label.setStyleSheet("background: rgba(13, 17, 23, 180); border: 2px solid #00f0ff; border-radius: 30px; padding: 10px;")