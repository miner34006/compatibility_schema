from revolt.errors import SubstitutionError

from compatibility_schema import json_schema as schema

from .substitution_testcase import SubstitutionTestCase


class TestSubstitution(SubstitutionTestCase):
    def test_null_type_substitution(self):
        with self.assertRaises(SubstitutionError):
            schema.null % 'banana'

    def test_boolean_type_substitution(self):
        self.assertSchemaHasValue(schema.boolean % True, True)
        with self.assertRaises(SubstitutionError):
            schema.boolean % 'banana'

    def test_boolean_specific_value_substitution(self):
        self.assertSchemaHasValue(schema.boolean(False) % True, True)

    def test_integer_type_substitution(self):
        self.assertSchemaHasValue(schema.integer % 42, 42)
        with self.assertRaises(SubstitutionError):
            schema.integer % 'banana'

    def test_float_type_substitution(self):
        self.assertSchemaHasValue(schema.float % 3.14, 3.14)
        with self.assertRaises(SubstitutionError):
            schema.float % 'banana'

    def test_string_type_substitution(self):
        self.assertSchemaHasValue(schema.string % 'banana', 'banana')
        self.assertSchemaHasValue(schema.string('banana') % 'banana1', 'banana1')
        with self.assertRaises(SubstitutionError):
            schema.string.numeric % 1
        self.assertSchemaHasValue(schema.string.numeric(1, 2 ** 63 - 1) % 'banana', 'banana')

    def test_timestamp_type_substitution(self):
        with self.assertRaises(SubstitutionError):
            schema.timestamp % True

        schema.timestamp.format('%Y-%m-%dT%H:%M:%S+00:00') % '2010-01-03T15:15:16+00:00'

    def test_array_type_substitution(self):
        self.assertIsInstance(schema.array % [1, 2, 3], schema.array.__class__)

        array_value = [None, 0, 3.14, 'banana', [], {}]
        self.assertSchemaHasValue(schema.array % array_value, array_value)

        self.assertSchemaHasValue(schema.array([schema.integer]) % [1], [1])

        with self.assertRaises(SubstitutionError):
            schema.array % 'banana'

        with self.assertRaises(SubstitutionError):
            schema.array([schema.string.numeric]) % [1]

    def test_array_type_object_substitution(self):
        object_schema = schema.object({'id': schema.integer})

        array1_schema = schema.array([object_schema])
        array1_value = [{'id': 1}]
        self.assertSchemaHasValue(array1_schema % array1_value, array1_value)

        array2_schema = schema.array([object_schema, object_schema])
        array2_value = [{'id': 1}, {'id': 2}]
        self.assertSchemaHasValue(array2_schema % array2_value, array2_value)

        with self.assertRaises(IndexError):
            array2_schema % array1_value

        array2_value_extra = [{'id': 1}, {'id': 2}, {'id': 3}]
        array2_schema % array2_value_extra

    def test_array_of_type_substitution(self):
        self.assertSchemaHasValue(schema.array.of(
            schema.integer) % [1, 2, 3], [1, 2, 3])

        with self.assertRaises(SubstitutionError):
            schema.array.of(schema.string) % 'banana'

        self.assertSchemaHasValue(schema.array.of(
            schema.integer) % [1, 2, 3], [1, 2, 3])

    def test_array_of_object_type_substitution(self):
        object_schema = schema.object({
            'id': schema.integer,
            'is_deleted': schema.boolean,
        })
        array_value = [{'id': 1}, {'id': 2, 'is_deleted': False}]
        self.assertSchemaHasValue(schema.array.of(
            object_schema) % array_value, array_value)

    def test_object_type_substitution(self):
        object_schema = schema.object({
            'id':         schema.integer,
            'title?':     schema.string,
            'is_deleted': schema.boolean,
        })
        keys = {
            'id': 42,
            'title': 'Banana Title'
        }
        substituted = object_schema % keys
        self.assertSchemaHasValue(substituted, keys)
        self.assertIn('title', substituted)
        self.assertIn('is_deleted', substituted)

        object_value = {'id': 1, 'is_deleted': False}
        self.assertSchemaHasValue(schema.object % object_value, object_value)

        self.assertNotIn('new_key', object_schema % {'new_key': 'banana'})

        with self.assertRaises(SubstitutionError):
            schema.object % []

    def test_object_type_nested_substitution(self):
        object_schema = schema.object({
            'id': schema.integer,
            'object': schema.object({
                'id': schema.string.numeric,
                'type': schema.string.non_empty,
                'target': schema.object.strict
            }).strict,
            'is_deleted': schema.boolean
        }).strict
        keys = {
            'id': 1,
            'object': {
                'id': '1',
                'target': {}
            }
        }

        substituted = object_schema % keys
        self.assertSchemaHasValue(substituted, keys)

        self.assertIn('strict', substituted.props)
        self.assertIn('strict', substituted['object'].props)
        self.assertIn('strict', substituted['object']['target'].props)

        self.assertIn('type', substituted['object'])
        self.assertIn('is_deleted', substituted)

    def test_object_type_dotted_substitution(self):
        object_schema = schema.object({
            'id': schema.integer,
            'object': schema.object({
                'id': schema.string.numeric,
                'type': schema.string.non_empty,
                'target': schema.object.strict
            }).strict,
            'is_deleted': schema.boolean
        }).strict
        keys = {
            'id': 1,
            'object.id': '1',
            'object.target': {}
        }

        substituted = object_schema % keys
        self.assertSchemaHasValue(substituted, keys)

    def test_any_type_substitution(self):
        with self.assertRaises(SubstitutionError):
            schema.any % SubstitutionTestCase

        bool_or_null = schema.boolean(True) | schema.null
        value = False
        self.assertSchemaHasValue(bool_or_null % value, value)

        string_or_null = schema.string('a') | schema.null
        value = 'b'
        self.assertSchemaHasValue(string_or_null % value, value)

    def test_one_of_type_substitution(self):
        integer_or_numeric = schema.one_of(
            schema.integer, schema.string.numeric)
        value = '1234'
        self.assertSchemaHasValue(integer_or_numeric % value, value)

        array_of_or_none = schema.one_of(
            schema.array.of(schema.integer), schema.null)
        value = [1, 2, 3]
        self.assertSchemaHasValue(array_of_or_none % value, value)

        with self.assertRaises(SubstitutionError):
            schema.one_of(schema.boolean, schema.integer) % 'banana'

    def test_enum_type_substitution(self):
        true_or_false = schema.enum('true', 'false')
        value = 'true'
        self.assertSchemaHasValue(true_or_false % value, value)

        with self.assertRaises(SubstitutionError):
            schema.enum(True, False) % 1

        with self.assertRaises(SubstitutionError):
            schema.enum(1, 2) % 3

    def test_substitution_inside_any_with_missing_keys(self):
        s = schema.any(schema.object({'id': schema.integer, 'name': schema.string}))
        value = {'id': 1}
        s = s % value
        self.assertSchemaHasValue(s.props.types[0], {'id': 1, 'name': None})
        self.assertEqual(s.props.types[0].props.keys['id'][0].props.value, 1)

    # def test_substitution_with_another_pattern_in_any(self):
    #     s = schema.string.pattern(r'^[a-z0-9-]{1}\@[a-z0-9]{1}\.[a-z]{1}$')
    #     s = schema.object({'email': s | schema.null})
    #     s % {'email': 'aa@aa.aa'}

    def test_substitution_object_in_object(self):
        s = schema.object({
            'payload': schema.object({
                'object': schema.object
            })
        })
        value = {'id': 1}
        s = s % {'payload.object': value}
        self.assertEqual(s.props.keys['payload'][0].props.keys['object'][0].props.keys['id'][0].props.value, 1)
