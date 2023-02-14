import unittest

from niltype import Nil


class SubstitutionTestCase(unittest.TestCase):

    def assertValuableHasValue(self, valuable, value):
        self.assertIsInstance(valuable.props.value, type(value))
        self.assertEqual(valuable.props.value, value)

    def assertArrayHasItems(self, array, items):
        self.assertGreaterEqual(len(array.props.items), len(items))
        for idx, item in enumerate(array.props.items):
            self.assertSchemaHasValue(item, items[idx])

    def assertObjectHasKeys(self, object, keys):
        self.assertGreaterEqual(len(object.props.keys), len(keys))
        for key, val in object.props.keys.items():
            if key in keys:
                self.assertSchemaHasValue(val[0], keys[key])

    def assertSchemaHasValue(self, substituted, value):
        if substituted.props.get('value', Nil) is not Nil:
            return self.assertValuableHasValue(substituted, value)
        elif substituted.props.get('items', Nil) is not Nil:
            return self.assertArrayHasItems(substituted, value)
        elif substituted.props.get('keys', Nil) is not Nil:
            return self.assertObjectHasKeys(substituted, value)
