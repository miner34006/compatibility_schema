from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestArrayOfValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationFails(None,  schema.array.of(schema.integer))
        self.assertValidationFails(False, schema.array.of(schema.integer))
        self.assertValidationFails(0,     schema.array.of(schema.integer))
        self.assertValidationFails('[]',  schema.array.of(schema.integer))
        self.assertValidationFails({},    schema.array.of(schema.integer))

    def test_it_validates_items_schema(self):
        self.assertValidationPasses(
            ['banana', 'cucumber'], schema.array.of(schema.string))
        self.assertValidationPasses(
            [1, 2, 3],              schema.array.of(schema.integer))
        self.assertValidationPasses(
            [None],                 schema.array.of(schema.null))

        self.assertValidationFails(
            ['banana', 'cucumber'], schema.array.of(schema.integer))
        self.assertValidationFails(
            [1, 2, 3],              schema.array.of(schema.string))

    def test_it_validates_length(self):
        self.assertValidationPasses(
            [],         schema.array.of(schema.string).empty)
        self.assertValidationPasses(
            ['banana'], schema.array.of(schema.string).non_empty)
        self.assertValidationPasses(
            ['banana'], schema.array.of(schema.string).length(1))
        self.assertValidationPasses(
            [0],        schema.array.of(schema.integer).length(1, 2))
        self.assertValidationPasses(
            [0, 1],     schema.array.of(schema.integer).length(1, 2))
        self.assertValidationPasses(
            ['banana'], schema.array.of(schema.string).min_length(1))
        self.assertValidationPasses(
            ['banana'], schema.array.of(schema.string).max_length(1))

        self.assertValidationFails(
            ['banana'], schema.array.of(schema.string).empty)
        self.assertValidationFails(
            [],         schema.array.of(schema.string).non_empty)
        self.assertValidationFails(
            [1],        schema.array.of(schema.integer).length(2))
        self.assertValidationFails(
            [1, 2, 3],  schema.array.of(schema.integer).length(2))
        self.assertValidationFails(
            [0, 1],     schema.array.of(schema.integer).length(0, 1))
        self.assertValidationFails(
            [0, 1],     schema.array.of(schema.integer).length(3, 5))
        self.assertValidationFails(
            [],         schema.array.of(schema.integer).min_length(1))
        self.assertValidationFails(
            [0, 1],     schema.array.of(schema.integer).max_length(1))
