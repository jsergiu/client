import { module, test } from 'qunit';
import { setupTest } from 'client/tests/helpers';

module('Unit | Route | timer', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    const route = this.owner.lookup('route:timer');
    assert.ok(route);
  });
});
