import sqlite3
import os

class Memory:
    def __init__(self, db_path="data/jarvis_memory.db"):
        # التأكد من أن مجلد data موجود باش ما يكراشيش
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """إنشاء قاعدة البيانات والجداول يلا ماكانوش"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # جدول المحادثات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # جدول الإعدادات والتفضيلات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preferences (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_message(self, role: str, content: str):
        """حفظ رسالة جديدة فالذاكرة"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", (role, content))
        conn.commit()
        conn.close()

    def get_history(self, limit: int = 6) -> list:
        """جلب آخر الرسائل باش يعقل على السياق (مقلوبين بالترتيب الصحيح)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        # نرجعوهم بالترتيب الزمني الصحيح (من القديم للجديد)
        return [{"role": row[0], "content": row[1]} for row in reversed(rows)]

    def get_all_preferences(self) -> dict:
        """جلب تفضيلات المستخدم (بحال واش كيبغي الصوت عالي، إلخ)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM preferences")
        rows = cursor.fetchall()
        conn.close()
        return {row[0]: row[1] for row in rows}