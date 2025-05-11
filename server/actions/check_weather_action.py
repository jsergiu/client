from dataclasses import dataclass
from typing import Optional, Dict, Any
from .base import ActionStrategy

@dataclass
class CheckWeatherAction(ActionStrategy):
    name: str = "get_weather"
    description: str = "For getting weather information for a specific location"
    location: Optional[str] = None
    confidence: Optional[float] = None

    def serialize_as_prompt(self) -> str:
        return f"""
        {self.name} - {self.description}
        Response format: {{ "command": "{self.name}", "confidence": 0.0-1.0, "location": "city_name" }}
        """

    async def execute(self, parameters: Dict[str, Any]) -> str:
        location = parameters.get('location')
        if location is None:
            raise ValueError("Location must be set before executing the command")
        return f"Getting weather information for {location}" 