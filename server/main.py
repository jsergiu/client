from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from utils.logger import setup_logging
from websocket.event_handler import EventWebSocketHandler
from server.speech.recognition.whisper_asr import WhisperASR

logger = setup_logging()
logger.info("Application starting")

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create audio directory if it doesn't exist
os.makedirs("audio", exist_ok=True)

# Store active event handlers
active_event_handlers: dict[str, EventWebSocketHandler] = {}

# Initialize WhisperASR with event handlers
whisper_stt = WhisperASR(event_handlers=active_event_handlers)

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    audio_file = None
    is_closed = False
    filename = None
    
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"audio/recording_{timestamp}.webm"
        logger.info(f"Created new audio file: {filename}")
        
        # Open file for writing
        audio_file = open(filename, 'wb')
        
        while True:
            try:
                data = await websocket.receive_bytes()
                if data:
                    audio_file.write(data)
                    logger.info(f"Received audio chunk of size {len(data)} bytes")
            except WebSocketDisconnect:
                logger.info("Client disconnected normally")
                break
            except Exception as e:
                logger.error(f"Error receiving data: {str(e)}")
                break
                
    except Exception as e:
        logger.error(f"Error in WebSocket handler: {str(e)}")
    finally:
        logger.info("WebSocket connection closing, starting cleanup...")
        if audio_file:
            audio_file.close()
            logger.info("Audio file closed successfully")
            
            # Transcribe the audio file if it exists
            if filename and os.path.exists(filename):
                logger.info(f"Audio file exists, starting transcription: {filename}")
                await whisper_stt.transcribe(filename)
            else:
                logger.error(f"Audio file not found: {filename}")
        
        if not is_closed:
            try:
                await websocket.close()
                is_closed = True
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {str(e)}")

@app.websocket("/ws/events")
async def event_websocket_endpoint(websocket: WebSocket):
    handler = EventWebSocketHandler(websocket)
    
    # Generate a unique ID for this connection
    connection_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    active_event_handlers[connection_id] = handler
    logger.info(f"New event handler registered with ID: {connection_id}")
    
    try:
        await handler.handle_connection()
    finally:
        # Remove the handler when the connection is closed
        active_event_handlers.pop(connection_id, None)
        logger.info(f"Event handler removed: {connection_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 