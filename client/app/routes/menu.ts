import Route from '@ember/routing/route';
import { service } from '@ember/service';
import type RouterService from '@ember/routing/router-service';

export default class MenuRoute extends Route {
  @service declare router: RouterService;

  setupController(controller: any) {
    super.setupController(controller, {});
    controller.router = this.router;
    controller.menuItems = [
      {
        name: 'Timer',
        icon: '⏱️',
        route: 'timer'
      },
      {
        name: 'Calendar',
        icon: '📅',
        route: 'calendar'
      },
      {
        name: 'Clock',
        icon: '🕒',
        route: 'clock'
      }
    ];
  }
}
