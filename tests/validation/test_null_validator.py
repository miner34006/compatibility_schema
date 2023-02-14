from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestNullValidator(ValidatorTestCase):

  def test_it_validates_type(self):
    self.assertValidationPasses(None, schema.null)

    self.assertValidationFails(False, schema.null)
    self.assertValidationFails(0,     schema.null)
    self.assertValidationFails('',    schema.null)
    self.assertValidationFails([],    schema.null)
    self.assertValidationFails({},    schema.null)
