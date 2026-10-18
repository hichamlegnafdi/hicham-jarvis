STYLE = """
QMainWindow {
    background-color: #0d1117;
}
QWidget {
    font-family: 'Segoe UI', Arial, sans-serif;
}
/* الشريط الجانبي (Sidebar) */
#Sidebar {
    background-color: #161b22;
    border-right: 2px solid #00f0ff;
}
#HeaderLabel {
    color: #00f0ff;
    font-size: 28px;
    font-weight: 900;
    letter-spacing: 4px;
    padding: 15px 5px;
    text-shadow: 0px 0px 10px rgba(0, 240, 255, 0.5);
}
#StatusLabel {
    color: #00f0ff;
    font-size: 15px;
    font-weight: bold;
    letter-spacing: 2px;
    padding: 10px;
    border: 1px solid #00f0ff;
    border-radius: 5px;
    background-color: rgba(0, 240, 255, 0.05);
}
/* البوطونات */
QPushButton {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px;
    font-size: 14px;
    font-weight: bold;
    text-align: left;
}
QPushButton:hover {
    background-color: #30363d;
    border: 1px solid #8b949e;
    color: #ffffff;
}
QPushButton:checked {
    background-color: rgba(0, 240, 255, 0.1);
    color: #00f0ff;
    border: 1px solid #00f0ff;
}
/* الإحصائيات (Stats) */
.StatLabel {
    color: #58a6ff;
    background-color: #0d1117;
    padding: 12px;
    border-radius: 6px;
    border: 1px solid #1f2428;
    font-family: 'Consolas', monospace;
    font-weight: bold;
}
/* الشات */
QLineEdit {
    background-color: #161b22;
    color: #c9d1d9;
    border: 1px solid #00f0ff;
    border-radius: 20px;
    padding: 12px 20px;
    font-size: 15px;
}
QLineEdit:focus {
    border: 2px solid #00f0ff;
    background-color: #0d1117;
}
"""