import whisper
import os
import tempfile
from typing import Optional, Dict
from .base_asr import BaseASR
from websocket.event_handler import EventWebSocketHandler
import logging

logger = logging.getLogger(__name__)

class WhisperASR(BaseASR):
    def __init__(self, event_handlers: Dict[str, EventWebSocketHandler] = None):
        # Load the smallest English-only model
        self.model = whisper.load_model("tiny.en")
        self.temp_dir = tempfile.gettempdir()
        self.event_handlers = event_handlers or {}

    async def transcribe(self, wav_path: str) -> Optional[str]:
        try:
            logger.info(f"Starting transcription of file: {wav_path}")
            result = self.model.transcribe(
                wav_path,
                language='en',
                task='transcribe'
            )
            
            transcription = result["text"].strip()
            if transcription:
                logger.info(f"Transcription successful: {transcription[:100]}...")
                # Send transcription through event WebSocket
                for handler in self.event_handlers.values():
                    await handler.emit("prompt_response", {
                        "text": transcription
                    })
                logger.info("Transcription sent to all connected clients")
            else:
                logger.error("Transcription returned empty string")
            
            return transcription
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {str(e)}")
            return None 