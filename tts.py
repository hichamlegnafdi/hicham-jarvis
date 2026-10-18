import asyncio
import edge_tts
import pygame
import os

class TTS:
    def __init__(self):
        pygame.mixer.init()
        # صوت بريطاني ذكوري فخم بحال ديال فيلم Iron Man
        self.voice = "en-GB-RyanNeural" 

    def speak(self, text):
        if not text: return
        asyncio.run(self._async_speak(text))

    async def _async_speak(self, text):
        audio_file = "temp_speech.mp3"
        # سرعنا الصوت شوية باش يبان روبوتي وسريع
        communicate = edge_tts.Communicate(text, self.voice, rate="+15%")
        await communicate.save(audio_file)
        
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
            
        pygame.mixer.music.unload()
        if os.path.exists(audio_file):
            os.remove(audio_file)