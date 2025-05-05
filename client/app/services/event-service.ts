import Service from '@ember/service';
import { tracked } from '@glimmer/tracking';

interface EventMessage {
  event_name: string;
  payload: any;
  timestamp: string;
}

export default class EventService extends Service {
  @tracked isConnected = false;
  private ws: WebSocket | null = null;
  private eventHandlers: Map<string, Set<(payload: any) => void>> = new Map();
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectTimeout = 1000; // Start with 1 second

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) {
      return;
    }

    this.ws = new WebSocket('ws://localhost:8000/ws/events');

    this.ws.onopen = () => {
      console.log('Event WebSocket connected');
      this.isConnected = true;
      this.reconnectAttempts = 0;
      this.reconnectTimeout = 1000;
    };

    this.ws.onclose = () => {
      console.log('Event WebSocket disconnected');
      this.isConnected = false;
      this.attemptReconnect();
    };

    this.ws.onerror = (error) => {
      console.error('Event WebSocket error:', error);
    };

    this.ws.onmessage = (event) => {
      try {
        const message: EventMessage = JSON.parse(event.data);
        this.handleEvent(message.event_name, message.payload);
      } catch (error) {
        console.error('Error parsing WebSocket message:', error);
      }
    };
  }

  private attemptReconnect() {
    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.error('Max reconnection attempts reached');
      return;
    }

    setTimeout(() => {
      this.reconnectAttempts++;
      this.reconnectTimeout *= 2; // Exponential backoff
      this.connect();
    }, this.reconnectTimeout);
  }

  on(eventName: string, callback: (payload: any) => void) {
    if (!this.eventHandlers.has(eventName)) {
      this.eventHandlers.set(eventName, new Set());
    }
    this.eventHandlers.get(eventName)?.add(callback);
  }

  off(eventName: string, callback: (payload: any) => void) {
    this.eventHandlers.get(eventName)?.delete(callback);
  }

  private handleEvent(eventName: string, payload: any) {
    const handlers = this.eventHandlers.get(eventName);
    if (handlers) {
      handlers.forEach(handler => {
        try {
          handler(payload);
        } catch (error) {
          console.error(`Error in event handler for ${eventName}:`, error);
        }
      });
    }
  }

  emit(eventName: string, payload: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      const message: EventMessage = {
        event_name: eventName,
        payload,
        timestamp: new Date().toISOString()
      };
      this.ws.send(JSON.stringify(message));
    } else {
      console.error('WebSocket is not connected');
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
      this.ws = null;
      this.isConnected = false;
    }
  }
}

// Don't forget to declare the service
declare module '@ember/service' {
  interface Registry {
    'event-service': EventService;
  }
} 