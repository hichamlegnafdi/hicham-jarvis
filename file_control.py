import os

class FileController:
    def read_file(self, file_path: str) -> str:
        try:
            if not os.path.exists(file_path):
                return f"❌ الملف '{file_path}' غير موجود."
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return f"📄 محتوى الملف '{file_path}':\n{content}"
        except Exception as e:
            return f"❌ خطأ في قراءة الملف: {e}"

    def create_file(self, file_path: str, content: str) -> str:
        try:
            # كيصاوب المجلدات يلا مكانوش
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"✅ تم إنشاء الملف بنجاح: {file_path}"
        except Exception as e:
            return f"❌ خطأ في إنشاء الملف: {e}"

    def list_directory(self, dir_path: str) -> str:
        try:
            if not os.path.exists(dir_path):
                return f"❌ المجلد '{dir_path}' غير موجود."
            files = os.listdir(dir_path)
            if not files:
                return f"📂 المجلد '{dir_path}' فارغ."
            return f"📂 محتويات '{dir_path}':\n" + "، ".join(files)
        except Exception as e:
            return f"❌ خطأ في قراءة المجلد: {e}"