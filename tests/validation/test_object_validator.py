from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestObjectValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationPasses({},         schema.object)
        self.assertValidationPasses({},         schema.object({}))
        self.assertValidationPasses({'id': 42}, schema.object)

        self.assertValidationFails(None,  schema.object)
        self.assertValidationFails(False, schema.object)
        self.assertValidationFails(0,     schema.object)
        self.assertValidationFails('{}',  schema.object)
        self.assertValidationFails([],    schema.object)

    def test_it_validates_keys(self):
        self.assertValidationPasses({}, schema.object({}))

        self.assertValidationPasses(
            {
                'string': 'banana',
                'number': 42,
                'array': [0, 1],
                'empty_object': {},
                'object': {
                    'boolean': True,
                    'object': {
                        'nothing': None
                    }
                }
            },
            schema.object({
                'string':       schema.string('banana'),
                'number':       schema.integer(42),
                'array':        schema.array([schema.integer(0), schema.integer(1)]),
                'empty_object': schema.object({}),
                'object':       schema.object({
                    'boolean': schema.boolean(True),
                    'object': schema.object({
                        'nothing': schema.null
                    })
                })
            })
        )

        self.assertValidationFails(None,        schema.object({}))
        self.assertValidationFails(
            {},          schema.object({'id': schema.integer}))
        self.assertValidationFails(
            {'id': '1'}, schema.object({'id': schema.integer}))

    def test_it_validates_strict_keys(self):
        self.assertValidationPasses({}, schema.object({}).strict)
        self.assertValidationPasses(
            {
                'id': 1234,
                'title': 'banana'
            },
            schema.object({
                'id':    schema.integer,
                'title': schema.string
            }).strict
        )

        self.assertValidationFails({'id': '1'}, schema.object({}).strict)
        self.assertValidationFails(
            {
                'id': 1234,
                'title': 'banana',
                'extra_key': True
            },
            schema.object({
                'id':    schema.integer,
                'title': schema.string
            }).strict
        )

    def test_it_validates_optional_keys_with_shema_addition(self):
        schema1 = schema.object({
            'id':     schema.integer
        })
        schema2 = schema.object({
            'comment?': schema.string
        })
        self.assertValidationPasses(
            {
                'id': 1
            },
            schema1 + schema2
        )

    def test_it_validates_optional_keys(self):
        self.assertValidationPasses(
            {
                'id': 1234
            },
            schema.object({
                'id':     schema.integer(1234),
                'title?': schema.string('banana')
            })
        )

        self.assertValidationFails(
            {
                'id': 1234,
                'title': 'not banana'
            },
            schema.object({
                'id':     schema.integer(1234),
                'title?': schema.string('banana')
            })
        )

    def test_it_validates_length(self):
        self.assertValidationPasses(
            {},                           schema.object.empty)
        self.assertValidationPasses(
            {'id': 42},                   schema.object.non_empty)
        self.assertValidationPasses(
            {},                           schema.object.length(0))
        self.assertValidationPasses(
            {'id': 42},                   schema.object.length(1))
        self.assertValidationPasses(
            {'id': 42},                   schema.object.length(1, 2))
        self.assertValidationPasses(
            {'id': 42, 'deleted': False}, schema.object.length(1, 2))
        self.assertValidationPasses(
            {'id': 42},                   schema.object.min_length(1))
        self.assertValidationPasses(
            {'id': 42},                   schema.object.max_length(1))
        self.assertValidationPasses(
            {
                'id': 42,
                'deleted': False
            },
            schema.object({
                'id': schema.integer
            }).length(2)
        )

        self.assertValidationFails(
            {'id': 42},                    schema.object.empty)
        self.assertValidationFails(
            {},                            schema.object.non_empty)
        self.assertValidationFails(
            {'id': 42},                    schema.object.length(0))
        self.assertValidationFails(
            {'id': 42},                    schema.object.length(2))
        self.assertValidationFails(
            {'id': 42, 'deleted': False},  schema.object.length(0, 1))
        self.assertValidationFails(
            {'id': 42, 'deleted': False},  schema.object.length(3, 5))
        self.assertValidationFails(
            {},                            schema.object.min_length(1))
        self.assertValidationFails(
            {'id': 42, 'deleted': False},  schema.object.max_length(1))
        self.assertValidationFails(
            {
                'id': 42
            },
            schema.object({
                'id': schema.integer
            }).length(2)
        )

    def test_validation_with_not_required_keys_after_sum(self):
        base_s = schema.object({
            'name': schema.string
        })
        s = base_s + schema.object({
            'id?': schema.integer,
        })
        self.assertValidationPasses(
            {'name': 'name'}, s)
