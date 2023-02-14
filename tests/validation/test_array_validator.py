from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestArrayValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationPasses([],         schema.array)
        self.assertValidationPasses(['banana'], schema.array)
        self.assertValidationPasses([0, 1],     schema.array)

        self.assertValidationFails(None,  schema.array)
        self.assertValidationFails(False, schema.array)
        self.assertValidationFails(0,     schema.array)
        self.assertValidationFails('[]',  schema.array)
        self.assertValidationFails({},    schema.array)

    def test_it_validates_items(self):
        self.assertValidationPasses([],     schema.array([]))
        self.assertValidationPasses([42],   schema.array([schema.integer(42)]))
        self.assertValidationPasses([0, 1], schema.array(
            [schema.integer(0), schema.integer(1)]))

        self.assertValidationFails([],     schema.array([schema.integer(42)]))
        self.assertValidationFails([42],   schema.array([]))
        self.assertValidationFails(42,     schema.array([schema.integer(42)]))
        self.assertValidationFails(['42'], schema.array([schema.integer(42)]))

        self.assertValidationFails(['banana', 'cucumber', 'carrot'], schema.array([
            schema.string('banana'),
            schema.string('cucumber')
        ]))

        self.assertValidationFails(['banana', 'cucumber'], schema.array([
            schema.string('banana'),
            schema.string('cucumber'),
            schema.string('carrot')
        ]))

    def test_it_validates_length(self):
        self.assertValidationPasses([],         schema.array.empty)
        self.assertValidationPasses([None],     schema.array.non_empty)
        self.assertValidationPasses([],         schema.array.length(0))
        self.assertValidationPasses(['banana'], schema.array.length(1))
        self.assertValidationPasses([0],        schema.array.length(1, 2))
        self.assertValidationPasses([0, 1],     schema.array.length(1, 2))
        self.assertValidationPasses(['banana'], schema.array.min_length(1))
        self.assertValidationPasses(['banana'], schema.array.max_length(1))

        self.assertValidationFails(['banana'], schema.array.empty)
        self.assertValidationFails([],         schema.array.non_empty)
        self.assertValidationFails(['banana'], schema.array.length(0))
        self.assertValidationFails(['banana'], schema.array.length(2))
        self.assertValidationFails([0, 1],     schema.array.length(0, 1))
        self.assertValidationFails([0, 1],     schema.array.length(3, 5))
        self.assertValidationFails([],         schema.array.min_length(1))
        self.assertValidationFails([0, 1],     schema.array.max_length(1))

    def test_it_validates_any_occurrences(self):
        self.assertValidationPasses(
            [42],          schema.array.contains(schema.integer(42)))
        self.assertValidationPasses(
            [42, 42],      schema.array.contains(schema.integer(42)))
        self.assertValidationPasses(
            [1, 2, 42, 3], schema.array.contains(schema.integer(42)))

        self.assertValidationFails(
            [],     schema.array.contains(schema.integer(42)))
        self.assertValidationFails(
            [0, 1], schema.array.contains(schema.integer(42)))

    def test_it_validates_one_occurrence(self):
        self.assertValidationPasses(
            [42],      schema.array.contains_one(schema.integer(42)))
        self.assertValidationPasses(
            [0, 1, 2], schema.array.contains_one(schema.integer(1)))

        self.assertValidationFails(
            [],       schema.array.contains_one(schema.integer(42)))
        self.assertValidationFails(
            [42, 42], schema.array.contains_one(schema.integer(42)))
        self.assertValidationFails(
            [0, 1],   schema.array.contains_one(schema.integer(42)))

    def test_it_validates_many_occurrences(self):
        self.assertValidationPasses(
            [42, 42], schema.array.contains_many(schema.integer(42)))
        self.assertValidationPasses([1, 2, 42, 3, 42, 4, 5],
                                    schema.array.contains_many(schema.integer(42)))

        self.assertValidationFails(
            [],            schema.array.contains_many(schema.integer(42)))
        self.assertValidationFails(
            [42],          schema.array.contains_many(schema.integer(42)))
        self.assertValidationFails(
            [1, 2, 42, 3], schema.array.contains_many(schema.integer(42)))
        self.assertValidationFails(
            [0, 1],        schema.array.contains_many(schema.integer(42)))

    def test_it_validates_all_occurrences(self):
        array_schema = schema.array.contains_all(
            [schema.boolean(True), schema.boolean(False)])

        self.assertValidationPasses([False, True],              array_schema)
        self.assertValidationPasses([False, True, True, None],  array_schema)

        self.assertValidationFails([False, False],              array_schema)
        self.assertValidationFails([],                          array_schema)
