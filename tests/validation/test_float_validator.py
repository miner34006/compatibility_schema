from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestFloatValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationPasses(-3.14, schema.float)
        self.assertValidationPasses(0.0,   schema.float)
        self.assertValidationPasses(3.14,  schema.float)

        self.assertValidationFails(None,   schema.float)
        self.assertValidationFails(False,  schema.float)
        self.assertValidationFails(42,     schema.float)
        self.assertValidationFails('3.14', schema.float)
        self.assertValidationFails([],     schema.float)
        self.assertValidationFails({},     schema.float)

    def test_it_validates_value(self):
        self.assertValidationPasses(3.14,  schema.float(3.14))
        self.assertValidationPasses(-3.14, schema.float(-3.14))
        self.assertValidationPasses(0.0,   schema.float.zero)

        self.assertValidationFails(None,  schema.float(0.0))
        self.assertValidationFails(3.14,  schema.float(-3.14))
        self.assertValidationFails(-3.14, schema.float(3.14))
        self.assertValidationFails(3,     schema.float(3.14))
        self.assertValidationFails('0.0', schema.float.zero)

    def test_it_validates_min_value(self):
        self.assertValidationPasses(3.14, schema.float.min(3.14))
        self.assertValidationPasses(3.15, schema.float.min(3.14))

        self.assertValidationFails(-3.14, schema.float.min(-3.13))

    def test_it_validates_max_value(self):
        self.assertValidationPasses(3.13, schema.float.max(3.14))
        self.assertValidationPasses(3.14, schema.float.max(3.14))

        self.assertValidationFails(3.15, schema.float.max(3.14))
