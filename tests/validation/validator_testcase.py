import unittest

from valera import validate


class ValidatorTestCase(unittest.TestCase):

  def assertValidationPasses(self, expected, actual):
    result = validate(actual, expected)
    return self.assertEqual(result.get_errors(), [])

  def assertValidationFails(self, expected, actual):
    result = validate(actual, expected)
    return self.assertNotEqual(result.get_errors(), [])
