from abc import ABC, abstractmethod

class BaseASR(ABC):

    @abstractmethod
    def transcribe(self, wav_path: str) -> str:
        pass
