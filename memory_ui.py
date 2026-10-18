from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                               QPushButton, QTableWidget, QTableWidgetItem, 
                               QLineEdit, QHeaderView, QTabWidget, QWidget, QMessageBox)
from core.memory import Memory

class MemoryDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("JARVIS Memory & Preferences")
        self.setMinimumSize(600, 400)
        self.setStyleSheet("background-color: #1e1e28; color: #c9bfff; font-size: 14px;")
        
        self.memory = Memory()
        self.layout = QVBoxLayout(self)
        
        # نظام التبويبات (Tabs)
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabBar::tab { background: #2a2a35; padding: 10px; } QTabBar::tab:selected { background: #45a29e; color: #0b0c10; font-weight: bold; }")
        
        self.setup_preferences_tab()
        self.setup_history_tab()
        
        self.layout.addWidget(self.tabs)

    def setup_preferences_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # جدول التفضيلات
        self.pref_table = QTableWidget(0, 2)
        self.pref_table.setHorizontalHeaderLabels(["Key (المعلومة)", "Value (القيمة)"])
        self.pref_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.pref_table.setStyleSheet("background-color: #0b0c10; color: #66fcf1; gridline-color: #45a29e;")
        
        # إدخال تفضيل جديد
        input_layout = QHBoxLayout()
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("مثال: User_Name")
        self.value_input = QLineEdit()
        self.value_input.setPlaceholderText("مثال: Hamza")
        
        btn_add = QPushButton("➕ إضافة/تعديل")
        btn_add.setStyleSheet("background-color: #45a29e; color: #0b0c10; font-weight: bold; padding: 8px;")
        btn_add.clicked.connect(self.add_pref)
        
        btn_del = QPushButton("🗑️ مسح المحدد")
        btn_del.setStyleSheet("background-color: #ff4c4c; color: white; font-weight: bold; padding: 8px;")
        btn_del.clicked.connect(self.delete_pref)
        
        input_layout.addWidget(self.key_input)
        input_layout.addWidget(self.value_input)
        input_layout.addWidget(btn_add)
        input_layout.addWidget(btn_del)
        
        layout.addWidget(QLabel("📝 المعلومات التي يتذكرها J.A.R.V.I.S دائماً:"))
        layout.addWidget(self.pref_table)
        layout.addLayout(input_layout)
        
        self.load_preferences()
        self.tabs.addTab(tab, "🧠 Preferences")

    def setup_history_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        self.hist_table = QTableWidget(0, 2)
        self.hist_table.setHorizontalHeaderLabels(["المرسل", "الرسالة"])
        self.hist_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.hist_table.setStyleSheet("background-color: #0b0c10; color: #c5c6c7; gridline-color: #45a29e;")
        
        btn_clear = QPushButton("⚠️ مسح الذاكرة قصيرة المدى (History)")
        btn_clear.setStyleSheet("background-color: #ff4c4c; color: white; font-weight: bold; padding: 8px;")
        btn_clear.clicked.connect(self.clear_history)
        
        layout.addWidget(QLabel("🕒 المحادثات السابقة:"))
        layout.addWidget(self.hist_table)
        layout.addWidget(btn_clear)
        
        self.load_history()
        self.tabs.addTab(tab, "🕒 History")

    # --- وظائف التفضيلات ---
    def load_preferences(self):
        self.pref_table.setRowCount(0)
        prefs = self.memory.get_all_preferences()
        for row, (k, v) in enumerate(prefs.items()):
            self.pref_table.insertRow(row)
            self.pref_table.setItem(row, 0, QTableWidgetItem(k))
            self.pref_table.setItem(row, 1, QTableWidgetItem(v))

    def add_pref(self):
        k, v = self.key_input.text().strip(), self.value_input.text().strip()
        if k and v:
            self.memory.save_preference(k, v)
            self.key_input.clear()
            self.value_input.clear()
            self.load_preferences()

    def delete_pref(self):
        current_row = self.pref_table.currentRow()
        if current_row >= 0:
            key = self.pref_table.item(current_row, 0).text()
            self.memory.delete_preference(key)
            self.load_preferences()

    # --- وظائف التاريخ ---
    def load_history(self):
        self.hist_table.setRowCount(0)
        history = self.memory.get_history(limit=50) # كنجبدو 50 رسالة للواجهة
        for row, msg in enumerate(history):
            self.hist_table.insertRow(row)
            self.hist_table.setItem(row, 0, QTableWidgetItem("User" if msg['role']=='user' else "J.A.R.V.I.S"))
            self.hist_table.setItem(row, 1, QTableWidgetItem(msg['content']))

    def clear_history(self):
        reply = QMessageBox.question(self, 'تأكيد', 'واش متأكد بغيتي تمسح الذاكرة؟', QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.memory.clear_history()
            self.load_history()