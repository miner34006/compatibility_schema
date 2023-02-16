from compatibility_schema import json_schema as schema

from .representation_testcase import RepresentationTestCase


class TestRepresentation(RepresentationTestCase):

    def test_null_type_representation(self):
        self.assertRepr(schema.null, 'schema.none')

    def test_boolean_type_representation(self):
        self.assertRepr(schema.boolean,          'schema.bool')
        self.assertRepr(schema.boolean(True),    'schema.bool(True)')

    def test_integer_type_representation(self):
        self.assertRepr(schema.integer,               'schema.int')
        self.assertRepr(schema.integer(42),           'schema.int(42)')
        self.assertRepr(schema.integer.min(0),        'schema.int.min(0)')
        self.assertRepr(schema.integer.max(1),        'schema.int.max(1)')
        self.assertRepr(schema.integer.between(0, 1), 'schema.int.min(0).max(1)')
        self.assertRepr(schema.integer.positive,      'schema.int.min(1)')
        self.assertRepr(schema.integer.non_positive,  'schema.int.max(0)')
        self.assertRepr(schema.integer.negative,      'schema.int.max(-1)')
        self.assertRepr(schema.integer.non_negative,  'schema.int.min(0)')
        self.assertRepr(schema.integer.zero,          'schema.int(0)')

    def test_float_type_representation(self):
        self.assertRepr(schema.float,                   'schema.float')
        self.assertRepr(schema.float(3.14),             'schema.float(3.14)')
        self.assertRepr(schema.float.min(0.0),          'schema.float.min(0.0)')
        self.assertRepr(schema.float.max(1.0),          'schema.float.max(1.0)')
        self.assertRepr(schema.float.between(0.0, 1.0), 'schema.float.min(0.0).max(1.0)')
        self.assertRepr(schema.float.positive,          'schema.float.min(1.0)')
        self.assertRepr(schema.float.non_positive,      'schema.float.max(0.0)')
        self.assertRepr(schema.float.negative,          'schema.float.max(-1.0)')
        self.assertRepr(schema.float.non_negative,      'schema.float.min(0.0)')
        self.assertRepr(schema.float.zero,              'schema.float(0.0)')

    def test_string_type_representation(self):
        self.assertRepr(schema.string,                      'schema.string')
        self.assertRepr(schema.string('banana'),            "schema.string('banana')")
        self.assertRepr(schema.string.length(32),           'schema.string.length(32, 32)')
        self.assertRepr(schema.string.length(1, 64),        'schema.string.length(1, 64)')
        self.assertRepr(schema.string.min_length(1),        'schema.string.min_length(1)')
        self.assertRepr(schema.string.max_length(128),      'schema.string.max_length(128)')
        self.assertRepr(schema.string.empty,                'schema.string.length(0)')
        self.assertRepr(schema.string.non_empty,            'schema.string.min_length(1)')
        self.assertRepr(schema.string.pattern(r'[0-9\-_]'), "schema.string.pattern('[0-9\\\-_]')")
        self.assertRepr(schema.string.uri,                  "schema.string.uri")
        self.assertRepr(schema.string.alphabetic,           "schema.string.alphabet('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')")
        self.assertRepr(schema.string.numeric,              'schema.string.numeric')
        self.assertRepr(schema.string.numeric(1),           'schema.string.numeric(1)')
        self.assertRepr(schema.string.numeric(0, 1),        'schema.string.numeric(0, 1)')
        self.assertRepr(schema.string.alpha_num,            "schema.string.alphabet('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')")
        self.assertRepr(schema.string.lowercase,            "schema.string.alphabet('abcdefghijklmnopqrstuvwxyz')")
        self.assertRepr(schema.string.uppercase,            "schema.string.alphabet('ABCDEFGHIJKLMNOPQRSTUVWXYZ')")
        self.assertRepr(schema.string.contains('substr'),   "schema.string.contains('substr')")

    def test_timestamp_type_representation(self):
        self.assertRepr(schema.timestamp,     'schema.timestamp')
        self.assertRepr(schema.timestamp.iso, 'schema.timestamp.iso')

        self.assertRepr(schema.timestamp('21-10-2015 04:29 pm'),
                       "schema.timestamp('2015-10-21T16:29:00+00:00')")

        self.assertRepr(schema.timestamp('21-10-2015 04:29 pm').iso,
                       "schema.timestamp('2015-10-21T16:29:00+00:00').iso")

        self.assertRepr(schema.timestamp.format('%Y-%m-%d %H:%M:%S'),
                       "schema.timestamp.format('%Y-%m-%d %H:%M:%S')")


    def test_array_type_representation(self):
        self.assertRepr(schema.array,                'schema.array')
        self.assertRepr(schema.array([]),            'schema.array([])')
        self.assertRepr(schema.array.length(10),     'schema.array.length(10)')
        self.assertRepr(schema.array.length(1, 2),   'schema.array.length(1, 2)')
        self.assertRepr(schema.array.min_length(1),  'schema.array.min_length(1)')
        self.assertRepr(schema.array.max_length(10), 'schema.array.max_length(10)')
        self.assertRepr(schema.array.empty,          'schema.array.empty')
        self.assertRepr(schema.array.non_empty,      'schema.array.non_empty')

        self.assertRepr(schema.array([schema.integer(0), schema.integer(1)]),
                       'schema.array([schema.int(0), schema.int(1)])')

        self.assertRepr(schema.array.contains(schema.integer(42)),
                       'schema.array.contains(schema.int(42))')
        self.assertRepr(schema.array.contains_one(schema.boolean),
                       'schema.array.contains_one(schema.bool)')
        self.assertRepr(schema.array.contains_many(schema.string('banana')),
                       "schema.array.contains_many(schema.string('banana'))")
        self.assertRepr(schema.array.contains_all([schema.string('banana'), schema.string('')]),
                       "schema.array.contains_all([schema.string('banana'), schema.string('')])")

        self.assertRepr(
            schema.array.contains(schema.object({
                'id': schema.integer(1)
            })),
            "schema.array.contains(schema.object({" + "\n" +
            "    'id': schema.int(1)" + "\n" +
            "}))"
        )

        self.assertRepr(
            schema.array([
                schema.integer(1),
                schema.integer(2),
                schema.integer(3)
            ]),
            "schema.array([" + "\n" +
            "    schema.int(1)," + "\n" +
            "    schema.int(2)," + "\n" +
            "    schema.int(3)" + "\n" +
            "])"
        )

        self.assertRepr(
            schema.array([
                schema.integer(1),
                schema.integer(2),
                schema.object({
                    'id': schema.string.numeric
                })
            ]),
            "schema.array([" + "\n" +
            "    schema.int(1)," + "\n" +
            "    schema.int(2)," + "\n" +
            "    schema.object({" + "\n" +
            "        'id': schema.string.numeric" + "\n" +
            "    })" + "\n" +
            "])"
        )

        self.assertRepr(
            schema.object({
                'items': schema.array([schema.object({
                    'id': schema.string.numeric
                })])
            }),
            "schema.object({" + "\n" +
            "    'items': schema.array([schema.object({" + "\n" +
            "        'id': schema.string.numeric" + "\n" +
            "    })])" + "\n" +
            "})"
        )

    def test_array_of_type_representation(self):
        self.assertRepr(schema.array.of(schema.integer),
                       'schema.array_of(schema.int)')

        self.assertRepr(schema.array.of(schema.integer).empty,
                       'schema.array_of(schema.int).empty')

        self.assertRepr(schema.array.of(schema.integer).non_empty,
                       'schema.array_of(schema.int).non_empty')

        self.assertRepr(schema.array.of(schema.integer).length(2),
                       'schema.array_of(schema.int).length(2)')

        self.assertRepr(schema.array.of(schema.integer).length(1, 10),
                       'schema.array_of(schema.int).length(1, 10)')

        self.assertRepr(schema.array.of(schema.integer).min_length(1),
                       'schema.array_of(schema.int).min_length(1)')

        self.assertRepr(schema.array.of(schema.integer).max_length(10),
                       'schema.array_of(schema.int).max_length(10)')

        self.assertRepr(
            schema.array.of(schema.object({
                'id': schema.string.numeric
            })),
            "schema.array_of(schema.object({" + "\n" +
            "    'id': schema.string.numeric" + "\n" +
            "}))"
        )

    def test_object_type_representation(self):
        self.assertRepr(schema.object,               'schema.object')
        self.assertRepr(schema.object({}),           'schema.object({})')
        self.assertRepr(schema.object.length(1),     'schema.object.length(1)')
        self.assertRepr(schema.object.length(0, 1),  'schema.object.length(0, 1)')
        self.assertRepr(schema.object.min_length(1), 'schema.object.min_length(1)')
        self.assertRepr(schema.object.max_length(1), 'schema.object.max_length(1)')
        self.assertRepr(schema.object.empty,         'schema.object.empty')
        self.assertRepr(schema.object.non_empty,     'schema.object.non_empty')

        self.assertRepr(
            schema.object({
                'id': schema.integer.positive
            }),
            "schema.object({" + "\n" +
            "    'id': schema.int.min(1)" + "\n" +
            "})"
        )

        self.assertRepr(
            schema.object({
                'id': schema.integer.positive
            }).strict,
            "schema.object({" + "\n" +
            "    'id': schema.int.min(1)" + "\n" +
            "}).strict"
        )

        self.assertRepr(
            schema.object({
                'attrs': schema.object({
                    'height': schema.float,
                    'width': schema.float
                }),
                'id': schema.integer.positive
            }),
            "schema.object({" + "\n" +
            "    'attrs': schema.object({" + "\n" +
            "        'height': schema.float," + "\n" +
            "        'width': schema.float" + "\n" +
            "    })," + "\n" +
            "    'id': schema.int.min(1)" + "\n" +
            "})"
        )

    def test_object_type_with_renamed_keys_representation(self):
        self.assertRepr(schema.object @ {},                  'schema.object')
        self.assertRepr(schema.object.empty @ {},             'schema.object.empty')
        self.assertRepr(schema.object.empty @ {'key': 'val'}, 'schema.object.empty')

    def test_any_type_representation(self):
        self.assertRepr(schema.any, 'schema.any')
        self.assertRepr(schema.any(schema.integer), 'schema.any(schema.int)')
        self.assertRepr(schema.any(schema.integer, schema.string), 'schema.any(schema.int, schema.string)')

    def test_enum_type_representation(self):
        self.assertRepr(schema.enum(1, 2, 3),       'schema.any(schema.int(1), schema.int(2), schema.int(3))')
        self.assertRepr(schema.enum('a', 'b', 'c'), "schema.any(schema.str('a'), schema.str('b'), schema.str('c'))")
        self.assertRepr(schema.enum(0, 1, None),    'schema.any(schema.int(0), schema.int(1), schema.none)')

    def test_one_of_type_representation(self):
        self.assertRepr(schema.one_of(schema.integer, schema.string.numeric, schema.null),
                       'schema.any(schema.int, schema.string.numeric, schema.none)')

        self.assertRepr(schema.one_of(schema.integer(0), schema.integer(1)),
                       'schema.any(schema.int(0), schema.int(1))')

        self.assertRepr(schema.boolean(True) | schema.null,
                       'schema.any(schema.bool(True), schema.none)')
