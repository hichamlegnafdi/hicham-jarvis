import os
from pathlib import Path

def enable_stealth_startup():
    print("⏳ إعداد التشغيل المخفي التلقائي لـ JARVIS...")
    
    # 1. كنجبدو المسار ديال ملف main.py فين كاين دابا
    project_dir = Path(__file__).parent.resolve()
    main_file = project_dir / "main.py"
    
    if not main_file.exists():
        print("❌ خطأ: ملف main.py ماموجودش فهاد المجلد.")
        return

    # 2. كنجبدو مسار مجلد Startup ديال الويندوز لي كيخدم مع الشعلة
    startup_dir = Path(os.getenv('APPDATA')) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"
    vbs_path = startup_dir / "Jarvis_Stealth_AutoStart.vbs"

    # 3. كنصايبو كود VBScript باش يخدم بايثون بطريقة مخفية (بدون شاشة سوداء)
    # كنستعملو pythonw.exe فبلاصت python.exe حيت هو لي كيخدم فـ الخلفية
    vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe ""{main_file}""", 0, False
'''

    # 4. كنحطو الملف فمجلد الويندوز
    try:
        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs_content)
        print("✅ تم بنجاح! JARVIS دابا مبرمج باش يخدم بوحدو.")
        print(f"📁 تم إنشاء ملف الإقلاع في: {vbs_path}")
        print("🤖 المرة الجاية لي غتشعل فيها البيسي، غيطلع ليك الإيموجي ديريكت بلا Terminal.")
    except Exception as e:
        print(f"❌ وقع مشكل أثناء الإعداد: {str(e)}")

if __name__ == "__main__":
    enable_stealth_startup()