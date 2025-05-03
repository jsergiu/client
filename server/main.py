from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import os
from datetime import datetime
from utils.logger import setup_logging

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

@app.websocket("/ws/audio")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connection accepted")
    audio_file = None
    is_closed = False
    
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"audio/recording_{timestamp}.webm"
        
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
        audio_file.close()
        
        if not is_closed:
            try:
                await websocket.close()
                is_closed = True
                logger.info("WebSocket connection closed")
            except Exception as e:
                logger.error(f"Error closing WebSocket: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 