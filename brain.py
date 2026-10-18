import os
import glob
from ai.gemini import ask
from core.memory import Memory
from core.actions import execute
from core.vision import ScreenVision

try:
    import PyPDF2
except ImportError:
    pass

class Brain:
    def __init__(self):
        self.memory = Memory()
        self.vision = ScreenVision()
        
        # كلمات الشاشة
        self.vision_triggers = [
            "look", "see", "screen", "read this", "what is on", 
            "chouf", "ecran", "chof", "شوف", "الشاشة", "شنو كتشوف"
        ]
        
        # كلمات الـ PDF
        self.pdf_triggers = [
            "pdf", "document", "summarize", "file", 
            "لخص", "ملف", "وثيقة", "تلخيص", "اقرأ"
        ]

    def read_latest_pdf(self) -> str:
        """هاد الدالة كتمشي لمجلد inbox كتقلب على أخر PDF تحط فيه وكتقراه"""
        try:
            inbox_path = "data/inbox"
            os.makedirs(inbox_path, exist_ok=True)
            
            # كنجبدو كاع ملفات الـ PDF لي كاينين
            list_of_files = glob.glob(f'{inbox_path}/*.pdf')
            if not list_of_files:
                return None
                
            # كنعزلو أخر واحد تحط فالمجلد
            latest_file = max(list_of_files, key=os.path.getctime)
            print(f"📄 Reading PDF: {latest_file}")
            
            text_content = ""
            with open(latest_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                # كنقراو غير أول 10 صفحات باش مانفوتوش الحد ديال الذكاء الاصطناعي
                for i in range(min(10, len(reader.pages))):
                    page_text = reader.pages[i].extract_text()
                    if page_text:
                        text_content += page_text + "\n"
            return text_content
        except Exception as e:
            print(f"❌ PDF Error: {e}")
            return None

    def process(self, text: str, image_path: str = None) -> str:
        self.memory.add_message("user", text)
        text_lower = text.lower()
        
        # 1. واش طلب منا نشوفو الشاشة؟
        if not image_path and any(word in text_lower for word in self.vision_triggers):
            image_path = self.vision.capture_screen()

        # 2. واش طلب منا نقراو شي ملف PDF؟
        if any(word in text_lower for word in self.pdf_triggers):
            pdf_text = self.read_latest_pdf()
            if pdf_text:
                # كنلصقو محتوى الـ PDF مع السؤال ديالك باش Gemini يجاوب عليه
                text = f"{text}\n\n[محتوى المستند للتحليل]:\n{pdf_text}"
            else:
                response = "Sir, I couldn't find any PDF files in the data/inbox folder."
                self.memory.add_message("model", response)
                return response

        history = self.memory.get_history(limit=6)

        # 3. صيفط للذكاء الاصطناعي
        response_text, actions_list = ask(prompt=text, image_path=image_path, history=history)

        # 4. تنفيذ الأوامر
        if actions_list:
            for action in actions_list:
                action_name = action.get("command")
                action_args = action.get("target", "")
                
                if action_name:
                    print(f"⚙️ Executing: {action_name} | Target: {action_args}")
                    result = execute(action_name, action_args)
                    
                    if response_text == "Right away, sir." or not response_text:
                        response_text = result

        self.memory.add_message("model", response_text)
        return response_text