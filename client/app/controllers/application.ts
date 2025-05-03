import Controller from '@ember/controller';
import { service } from '@ember/service';
import type RouterService from '@ember/routing/router-service';
import { computed } from '@ember/object';

export default class ApplicationController extends Controller {
  @service declare router: RouterService;

  @computed('router.currentRouteName')
  get isMenuRoute() {
    return this.router.currentRouteName === 'menu';
  }
} 