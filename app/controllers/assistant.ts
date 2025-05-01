import Controller from '@ember/controller';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';

export default class AssistantController extends Controller {
  @tracked isRecording = false;
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  private websocket: WebSocket | null = null;
  private stream: MediaStream | null = null;
  private isClosing = false;

  @action
  async toggleRecording() {
    if (this.isRecording) {
      await this.stopRecording();
    } else {
      await this.startRecording();
    }
  }

  private async startRecording() {
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(this.stream, {
        mimeType: 'audio/webm;codecs=opus',
        audioBitsPerSecond: 128000
      });
      this.audioChunks = [];
      this.isClosing = false;

      // Connect to WebSocket
      this.websocket = new WebSocket('ws://localhost:8000/ws/audio');
      
      this.websocket.onopen = () => {
        console.log('WebSocket connection established');
        // Start recording after WebSocket is connected
        if (this.mediaRecorder && this.mediaRecorder.state === 'inactive') {
          this.mediaRecorder.start(1000); // Collect data every second
          this.isRecording = true;
        }
      };

      this.websocket.onerror = (error) => {
        console.error('WebSocket error:', error);
        this.stopRecording();
      };

      this.websocket.onclose = (event) => {
        console.log('WebSocket connection closed:', event.code, event.reason);
        this.websocket = null;
        if (this.isRecording && !this.isClosing) {
          this.stopRecording();
        }
      };
      
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
          // Send audio data to WebSocket
          if (this.websocket?.readyState === WebSocket.OPEN) {
            try {
              this.websocket.send(event.data);
            } catch (error) {
              console.error('Error sending audio data:', error);
              this.stopRecording();
            }
          }
        }
      };

      this.mediaRecorder.onstop = () => {
        console.log('MediaRecorder stopped, total chunks:', this.audioChunks.length);
      };

    } catch (error) {
      console.error('Error starting recording:', error);
      this.cleanup();
    }
  }

  private async stopRecording() {
    console.log('Stopping recording...');
    this.isClosing = true;
    
    if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
      try {
        this.mediaRecorder.stop();
        console.log('MediaRecorder stopped');
      } catch (error) {
        console.error('Error stopping MediaRecorder:', error);
      }
    }

    this.cleanup();
  }

  private cleanup() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop());
      this.stream = null;
    }

    if (this.websocket && !this.isClosing) {
      try {
        if (this.websocket.readyState === WebSocket.OPEN) {
          this.websocket.close(1000, "Recording stopped");
        }
      } catch (error) {
        console.error('Error closing WebSocket:', error);
      } finally {
        this.websocket = null;
      }
    }

    this.mediaRecorder = null;
    this.isRecording = false;
    this.audioChunks = [];
    this.isClosing = false;
  }
} 