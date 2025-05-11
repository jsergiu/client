from typing import Dict, Any, Protocol

class ActionStrategy(Protocol):
    @property
    def name(self) -> str:
        pass

    def serialize_as_prompt(self) -> str:
        pass

    async def execute(self, parameters: Dict[str, Any]) -> str:
        pass 