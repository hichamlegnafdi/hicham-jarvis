import os
from PIL import ImageGrab

class ScreenVision:
    def __init__(self, save_path="data/current_screen.png"):
        """التهيئة ديال العينين وتحديد فين غتخزن السكرين شوت"""
        self.save_path = save_path
        # كنتأكدو بلي مجلد data موجود
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

    def capture_screen(self):
        """هاد الدالة كتاخد سكرين شوت للشاشة كاملة وكتخبيها باش يشوفها Gemini"""
        try:
            print("📸 Taking screenshot...")
            # أخذ لقطة للشاشة
            screenshot = ImageGrab.grab()
            
            # حفظ الصورة
            screenshot.save(self.save_path, "PNG")
            print(f"✅ Screenshot saved at: {self.save_path}")
            
            return self.save_path
        except Exception as e:
            print(f"❌ خطأ في التقاط الشاشة: {str(e)}")
            return None