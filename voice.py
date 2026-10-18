import speech_recognition as sr

class VoiceEngine:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.pause_threshold = 0.6 # زدناها شوية باش ما يقطعش ليك الهضرة بالزربة
        self.recognizer.non_speaking_duration = 0.4
        self.language = "ar-MA" # الدارجة كلغة أساسية للاستماع

    def listen(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=7, phrase_time_limit=15)
            
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text
            
        except sr.WaitTimeoutError:
            # المستعمل ما هضرش
            return "" 
        except sr.UnknownValueError:
            # جوجل ما قدراتش تفهم الصوت (ضجيج أو هضرة غير واضحة)
            return ""
        except sr.RequestError:
            raise Exception("Network error: Google Speech Recognition is unreachable.")
        except Exception as e:
            raise Exception(f"Microphone error: {str(e)}")