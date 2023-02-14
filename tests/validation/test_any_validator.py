from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestAnyValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationPasses(42,       schema.any)
        self.assertValidationPasses(True,     schema.any)
        self.assertValidationPasses('banana', schema.any)
        self.assertValidationPasses([],       schema.any)
        self.assertValidationPasses({},       schema.any)
        self.assertValidationPasses(None,     schema.any)
