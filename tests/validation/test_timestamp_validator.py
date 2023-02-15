from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestTimestampValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationPasses('21-10-2015 04:29 pm', schema.timestamp)

        self.assertValidationFails(None,  schema.timestamp)
        self.assertValidationFails(False, schema.timestamp)
        self.assertValidationFails(0,     schema.timestamp)
        self.assertValidationFails([],    schema.timestamp)
        self.assertValidationFails({},    schema.timestamp)

    def test_it_validates_value(self):
        timestamp = schema.timestamp('21-10-2015 04:29 pm')

        self.assertValidationPasses('21-10-2015 04:29 pm',       timestamp)
        self.assertValidationPasses('21/10/2015 16:29',          timestamp)
        self.assertValidationPasses('2015-10-21T16:29:00+00:00', timestamp)

        self.assertValidationFails('21-10-2015 04:29 am', timestamp)
        self.assertValidationFails('?',                   timestamp)

    def test_it_validates_format(self):
        timestamp = schema.timestamp.format('%Y-%m-%d %H:%M:%S')

        self.assertValidationPasses('2015-10-21 16:29:00', timestamp)

        self.assertValidationFails('2015/10/21 16:29:00',       timestamp)
        self.assertValidationFails('2015-10-21T16:29:00+00:00', timestamp)

    def test_it_validates_with_substitution(self):
        timestamp = schema.timestamp.format('%Y-%m-%dT%H:%M:%S+00:00') % '2023-02-15T16:40:59+00:00'
        self.assertValidationPasses('2023-02-15T16:40:59+00:00', timestamp)

    def test_it_validates_iso(self):
        self.assertValidationPasses(
            '2015-10-21T16:29:00.000Z', schema.timestamp.iso)

        self.assertValidationFails(
            '21 October 2015, 16:29:00', schema.timestamp.iso)

    def test_it_validates_ambiguous_cases(self):
        timestamp = schema.timestamp('03 Feb 2020')
        self.assertValidationFails('2020-02-03', timestamp)

        timestamp = schema.timestamp('03 Feb 2020').format('%Y-%m-%d')
        self.assertValidationPasses('2020-02-03', timestamp)
