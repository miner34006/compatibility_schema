from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestBooleanValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationPasses(True,  schema.boolean)
        self.assertValidationPasses(False, schema.boolean)

        self.assertValidationFails(None,   schema.boolean)
        self.assertValidationFails('True', schema.boolean)
        self.assertValidationFails('',     schema.boolean)
        self.assertValidationFails(0,      schema.boolean)
        self.assertValidationFails(1,      schema.boolean)
        self.assertValidationFails([],     schema.boolean)
        self.assertValidationFails({},     schema.boolean)

    def test_it_validates_value(self):
        self.assertValidationPasses(True,  schema.boolean(True))
        self.assertValidationPasses(False, schema.boolean(False))

        self.assertValidationFails(None,  schema.boolean(False))
        self.assertValidationFails(True,  schema.boolean(False))
        self.assertValidationFails(False, schema.boolean(True))
