from abc import ABC, abstractmethod

class BaseSTT(ABC):

    @abstractmethod
    def transcribe(self, wav_path: str) -> str:
        pass
