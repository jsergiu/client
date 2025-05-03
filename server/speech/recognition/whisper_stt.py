import whisper
import os
import tempfile
from typing import Optional
from .base_stt import BaseSTT

class WhisperSTT(BaseSTT):
    def __init__(self):
        # Load the smallest English-only model
        self.model = whisper.load_model("tiny.en")
        self.temp_dir = tempfile.gettempdir()

    def transcribe(self, wav_path: str) -> Optional[str]:
        try:
            result = self.model.transcribe(
                wav_path,
                language='en',
                task='transcribe'
            )
            
            return result["text"].strip()
            
        except Exception as e:
            print(f"Error transcribing audio: {str(e)}")
            return None 