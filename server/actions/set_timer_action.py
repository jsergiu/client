from dataclasses import dataclass
from typing import Optional, Dict, Any
from .base import ActionStrategy

@dataclass
class SetTimerAction(ActionStrategy):
    name: str = "set_timer"
    description: str = "For setting timers, alarms and reminders"
    message_on_timeout: str = "Your timer has expired"
    duration: Optional[int] = None
    confidence: Optional[float] = None

    def serialize_as_prompt(self) -> str:
        return f"""
        {self.name} - {self.description}
        Response format: {{ "command": "{self.name}", "confidence": 0.0-1.0, "duration": seconds }}
        """

    async def execute(self, parameters: Dict[str, Any]) -> str:
        duration = parameters.get('duration')
        if duration is None:
            raise ValueError("Duration must be set before executing the command")
        return f"Setting a timer for {duration} seconds" 