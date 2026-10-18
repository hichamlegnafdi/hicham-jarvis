import requests
import base64
import copy
from config import GEMINI_API_KEY, GEMINI_MODEL
from core.memory import Memory

# 1. حيدنا البلوجينز (Plugins) باش مايبقاش يطلع الإيرور
mem_db = Memory()

SYSTEM_PROMPT = """You are JARVIS, a highly advanced AI with 100% SYSTEM ACCESS.
CRITICAL RULE 1: Perfectly UNDERSTAND Moroccan Arabic (Darija), but ALWAYS REPLY IN ENGLISH with a British accent.
CRITICAL RULE 2: Your responses MUST BE EXTREMELY FAST AND SHORT.
CRITICAL RULE 3 (GOD MODE): You have a tool called 'RUN_POWERSHELL'. If the user asks you to do ANYTHING on their PC (change settings, create multiple folders, fetch system info, download files, connect to networks) and there is no direct command for it, GENERATE AND EXECUTE A POWERSHELL SCRIPT via RUN_POWERSHELL. Do everything autonomously.
"""

def get_dynamic_prompt():
    prefs = mem_db.get_all_preferences()
    pref_text = "\n".join([f"- {k}: {v}" for k, v in prefs.items()])
    dynamic_prompt = SYSTEM_PROMPT
    if pref_text:
        dynamic_prompt += f"\nUSER PREFERENCES:\n{pref_text}"
    return dynamic_prompt

# 2. تعريف الأدوات لي يقدر Jarvis يخدم بيهم
TOOLS = [{
    "functionDeclarations": [{
        "name": "execute_pc_commands",
        "description": "Execute PC commands like RUN_POWERSHELL, OPEN_APP, READ_FILE, etc.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "actions": {
                    "type": "ARRAY",
                    "items": {
                        "type": "OBJECT",
                        "properties": {
                            "command": {"type": "STRING"},
                            "target": {"type": "STRING"}
                        }
                    }
                }
            }
        }
    }]
}]

def ask(prompt: str, image_path: str = None, history: list = None) -> tuple[str, list]:
    if not GEMINI_API_KEY or len(GEMINI_API_KEY) < 20:
        return "Sir, the Gemini API key is missing or invalid. Please check the configuration.", []

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"
    contents = []
    
    if history:
        for msg in history[-6:]: # كياخد غير آخر 6 رسائل باش يعقل على السياق
            contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

    current_parts = [{"text": prompt}]
    if image_path:
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            current_parts.append({"inlineData": {"mimeType": "image/jpeg", "data": encoded_string}})
        except Exception as e:
            return f"I encountered an error reading the image, sir: {str(e)}", []

    contents.append({"role": "user", "parts": current_parts})

    payload = {
        "system_instruction": {"parts": [{"text": get_dynamic_prompt()}]},
        "contents": contents,
        "tools": TOOLS,
        "generationConfig": {"temperature": 0.3} # درجة حرارة منخفضة باش يكون دقيق
    }

    headers = {"Content-Type": "application/json", "x-goog-api-key": GEMINI_API_KEY}

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        
        # 1. يلا كان شي مشكل فالـ API غيقولينا بالضبط شنو هو
        if response.status_code != 200:
            print(f"API ERROR DETECTED: {response.text}")
            return f"API Error {response.status_code}: Please check your terminal, sir.", []

        # 2. قراءة الجواب بطريقة آمنة (هنا فين كان السطر 78)
        try:
            data = response.json()
        except Exception as json_err:
            return f"Error parsing response: {str(json_err)}", []
            
        candidates = data.get("candidates", [])
        
        if not candidates:
            return "I apologize sir, but I received an empty response.", []

        content = candidates[0].get("content", {})
        response_parts = content.get("parts", []) if content else []
        text_response = ""
        actions_list = []

        for part in response_parts:
            if "text" in part:
                text_response += part["text"]
            elif "functionCall" in part:
                func_call = part["functionCall"]
                if func_call.get("name") == "execute_pc_commands":
                    # حماية إضافية يلا ما صيفطش لينا Les arguments
                    args = func_call.get("args") or {}
                    actions_list.extend(args.get("actions", []))

        if not text_response.strip() and actions_list:
            text_response = "Right away, sir."

        return text_response.strip() or "Task completed.", actions_list

    except requests.exceptions.Timeout:
        return "The connection timed out, sir. Please check your internet.", []
    except requests.exceptions.RequestException as e:
        return f"Network error, sir: {str(e)}", []
    except Exception as e:
        return f"System error in brain module: {str(e)}", []