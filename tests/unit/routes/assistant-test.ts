import { module, test } from 'qunit';
import { setupTest } from 'client/tests/helpers';

module('Unit | Route | assistant', function (hooks) {
  setupTest(hooks);

  test('it exists', function (assert) {
    const route = this.owner.lookup('route:assistant');
    assert.ok(route);
  });
});
