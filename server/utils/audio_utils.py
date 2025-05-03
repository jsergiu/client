import os
import subprocess
from typing import Optional

def convert_webm_to_wav(webm_path: str, sample_rate: int = 16000, channels: int = 1) -> Optional[str]:
    """
    Convert audio/webm to audio/wav using ffmpeg
    
    Args:
        webm_path: Path to the input WebM audio file
        sample_rate: Sample rate for output WAV file (default: 16000 for Whisper)
        channels: Number of audio channels (default: 1 for mono)
        
    Returns:
        Path to the converted WAV file or None if conversion fails
    """
    try:
        # Generate output WAV file path
        wav_path = os.path.splitext(webm_path)[0] + '.wav'
        
        # FFmpeg command to convert WebM to WAV
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', webm_path,
            '-acodec', 'pcm_s16le',
            '-ar', str(sample_rate),
            '-ac', str(channels),
            wav_path
        ]
        
        # Run FFmpeg command
        result = subprocess.run(
            ffmpeg_cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            return wav_path
        else:
            print(f"FFmpeg error: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"Error converting WebM to WAV: {str(e)}")
        return None 