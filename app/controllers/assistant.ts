import Controller from '@ember/controller';
import { action } from '@ember/object';
import { tracked } from '@glimmer/tracking';

export default class AssistantController extends Controller {
  @tracked isRecording = false;
  private mediaRecorder: MediaRecorder | null = null;
  private audioChunks: Blob[] = [];
  private websocket: WebSocket | null = null;

  @action
  async toggleRecording() {
    if (this.isRecording) {
      this.stopRecording();
    } else {
      await this.startRecording();
    }
  }

  private async startRecording() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.mediaRecorder = new MediaRecorder(stream);
      this.audioChunks = [];

      // Connect to WebSocket
      this.websocket = new WebSocket('ws://localhost:8000/ws/audio');
      
      this.mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          this.audioChunks.push(event.data);
          // Send audio data to WebSocket
          if (this.websocket?.readyState === WebSocket.OPEN) {
            this.websocket.send(event.data);
          }
        }
      };

      this.mediaRecorder.start(100); // Collect data every 100ms
      this.isRecording = true;
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  }

  private stopRecording() {
    if (this.mediaRecorder) {
      this.mediaRecorder.stop();
      this.mediaRecorder.stream.getTracks().forEach(track => track.stop());
      this.mediaRecorder = null;
    }

    if (this.websocket) {
      this.websocket.close();
      this.websocket = null;
    }

    this.isRecording = false;
  }
} 