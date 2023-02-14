from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestEnumValidator(ValidatorTestCase):

    def test_it_validates_enumerators(self):
        self.assertValidationPasses(
            'banana', schema.enum('banana', 'cucumber'))
        self.assertValidationPasses(None,     schema.enum(None, False, 0, ''))
        self.assertValidationPasses(False,    schema.enum(0, 1))

        self.assertValidationFails('carrot', schema.enum('banana', 'cucumber'))
        self.assertValidationFails(0,        schema.enum(*range(1, 10)))

    def test_it_validates_null_type(self):
        self.assertValidationPasses(
            None, schema.enum('banana', 'cucumber', None))
        self.assertValidationPasses(None, schema.enum(None, False, 0, ''))

        self.assertValidationFails(False, schema.enum('true', 'false', None))
        self.assertValidationFails(0,     schema.enum('true', 'false', None))
        self.assertValidationFails('',    schema.enum('true', 'false', None))
        self.assertValidationFails([],    schema.enum('true', 'false', None))
        self.assertValidationFails({},    schema.enum('true', 'false', None))
