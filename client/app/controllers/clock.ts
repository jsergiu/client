import Controller from '@ember/controller';
import { tracked } from '@glimmer/tracking';
import { action } from '@ember/object';

export default class ClockController extends Controller {
  @tracked currentTime = '';
  @tracked period = '';
  timer: number | null = null;

  constructor() {
    super(...arguments);
    this.updateTime();
    this.startTimer();
  }

  @action
  updateTime() {
    const now = new Date();
    const hours = now.getHours();
    const minutes = now.getMinutes();
    
    // Format hours to 12-hour format
    const formattedHours = hours % 12 || 12;
    const formattedMinutes = minutes.toString().padStart(2, '0');
    
    this.currentTime = `${formattedHours}:${formattedMinutes}`;
    this.period = hours >= 12 ? 'pm' : 'am';
  }

  @action
  startTimer() {
    this.timer = window.setInterval(() => {
      this.updateTime();
    }, 1000);
  }

  willDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  }
} 