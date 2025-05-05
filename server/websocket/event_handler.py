from fastapi import WebSocket
from typing import Dict, Any, Optional, Callable
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EventWebSocketHandler:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.is_closed = False
        self._event_handlers: Dict[str, list[Callable]] = {}
        
    def on(self, event_name: str, callback: Callable) -> None:
        """Register an event handler."""
        if event_name not in self._event_handlers:
            self._event_handlers[event_name] = []
        self._event_handlers[event_name].append(callback)
        
    async def emit(self, event_name: str, payload: Any) -> None:
        """Emit an event to the client."""
        try:
            message = {
                "event_name": event_name,
                "payload": payload,
                "timestamp": datetime.now().isoformat()
            }
            await self.websocket.send_json(message)
            logger.info(f"Emitted event: {event_name}")
        except Exception as e:
            logger.error(f"Error emitting event {event_name}: {str(e)}")
            
    async def handle_connection(self) -> None:
        """Main method to handle the WebSocket connection."""
        try:
            await self.websocket.accept()
            logger.info("Event WebSocket connection accepted")
            
            while True:
                try:
                    # Receive and parse the message
                    data = await self.websocket.receive_json()
                    event_name = data.get("event_name")
                    payload = data.get("payload")
                    
                    if event_name and event_name in self._event_handlers:
                        # Call all registered handlers for this event
                        for handler in self._event_handlers[event_name]:
                            try:
                                await handler(payload)
                            except Exception as e:
                                logger.error(f"Error in event handler for {event_name}: {str(e)}")
                    else:
                        logger.warning(f"No handlers registered for event: {event_name}")
                        
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")
                    break
                    
        except Exception as e:
            logger.error(f"Error in WebSocket handler: {str(e)}")
        finally:
            await self.cleanup()
            
    async def cleanup(self) -> None:
        """Clean up the WebSocket connection."""
        if not self.is_closed:
            try:
                await self.websocket.close()
                self.is_closed = True
                logger.info("Event WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {str(e)}") 