# plugins/manager.py

class PluginManager:
    def __init__(self):
        # هنا فين غنزيدو الإضافات من بعد يلا بغينا
        self.plugins = {}

    def get_all_tools(self):
        # حاليا ماكاين حتى أداة إضافية
        return []

    def can_handle(self, action_name: str) -> bool:
        # كترجع False حيت مزال ما برمجنا حتى Plugin
        return False

    def execute(self, action_name: str, action_args: str) -> str:
        return "❌ إضافة غير موجودة."