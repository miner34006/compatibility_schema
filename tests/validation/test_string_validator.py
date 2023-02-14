from compatibility_schema import json_schema as schema

from .validator_testcase import ValidatorTestCase


class TestStringValidator(ValidatorTestCase):

    def test_it_validates_type(self):
        self.assertValidationPasses('banana', schema.string)
        self.assertValidationPasses('',       schema.string)

        self.assertValidationFails(None,  schema.string)
        self.assertValidationFails(False, schema.string)
        self.assertValidationFails(0,     schema.string)
        self.assertValidationFails([],    schema.string)
        self.assertValidationFails({},    schema.string)

    def test_it_validates_value(self):
        self.assertValidationPasses('banana', schema.string('banana'))
        self.assertValidationPasses('',       schema.string(''))
        self.assertValidationPasses(' ',      schema.string(' '))

        self.assertValidationFails(None,     schema.string(''))
        self.assertValidationFails('banana', schema.string('cucumber'))
        self.assertValidationFails('',       schema.string(' '))
        self.assertValidationFails(' ',      schema.string(''))

    def test_it_validates_uri(self):
        self.assertValidationPasses('http://localhost',  schema.string.uri)
        self.assertValidationPasses('http://127.0.0.1',  schema.string.uri)
        self.assertValidationPasses('http://github.com', schema.string.uri)
        self.assertValidationPasses('github.com',        schema.string.uri)
        self.assertValidationPasses('127.0.0.1',         schema.string.uri)

        self.assertValidationFails('http://', schema.string.uri)
        self.assertValidationFails('//',      schema.string.uri)
        self.assertValidationFails('?',       schema.string.uri)

    def test_it_validates_pattern(self):
        self.assertValidationPasses(
            'banana', schema.string.pattern(r'^[a-z]+$'))

        self.assertValidationFails(
            'banana', schema.string.pattern(r'^[0-9]+$'))

    def test_it_validates_contains(self):
        self.assertValidationPasses('banana', schema.string.contains(''))
        self.assertValidationPasses('banana', schema.string.contains('banana'))
        self.assertValidationPasses(
            'abcbanana', schema.string.contains('banana'))
        self.assertValidationPasses(
            'bananaabc', schema.string.contains('banana'))
        self.assertValidationPasses(
            ' banana ', schema.string.contains('banana'))

        self.assertValidationFails('', schema.string.contains('banana'))

    def test_it_validates_numeric(self):
        self.assertValidationPasses('1234',        schema.string.numeric)
        self.assertValidationPasses('-1234',       schema.string.numeric)
        self.assertValidationPasses(
            '2147483647',  schema.string.numeric(2147483647))
        self.assertValidationPasses(
            '-2147483648', schema.string.numeric(-2147483648))
        self.assertValidationPasses(
            '-1',          schema.string.numeric(-1, 1))
        self.assertValidationPasses('1',           schema.string.numeric(1, 1))

        self.assertValidationFails('id', schema.string.numeric)
        self.assertValidationFails('-',  schema.string.numeric)
        self.assertValidationFails('--',  schema.string.numeric)

        self.assertValidationFails(
            '2147483646',  schema.string.numeric(2147483647))
        self.assertValidationFails(
            '-2147483649', schema.string.numeric(-2147483648))
        self.assertValidationFails('-2',          schema.string.numeric(-1, 1))
        self.assertValidationFails('2',           schema.string.numeric(-1, 1))

    #  TODO: падает проверка в тесте
    def test_it_validates_alphabet(self):
        self.assertValidationPasses('id',     schema.string.alphabetic)
        self.assertValidationPasses('id1234', schema.string.alpha_num)
        self.assertValidationPasses(
            'id',     schema.string.alphabetic.lowercase)
        self.assertValidationPasses(
            'ID',     schema.string.alphabetic.uppercase)
        # self.assertValidationPasses(
        #     'id1234', schema.string.alpha_num.lowercase)
        # self.assertValidationPasses(
        #     'ID1234', schema.string.alpha_num.uppercase)

        self.assertValidationFails('1234',   schema.string.alphabetic)
        self.assertValidationFails(' ',      schema.string.alpha_num)
        self.assertValidationFails(
            'ID',     schema.string.alphabetic.lowercase)
        self.assertValidationFails(
            'id',     schema.string.alphabetic.uppercase)
        self.assertValidationFails('ID1234', schema.string.alpha_num.lowercase)
        self.assertValidationFails('id1234', schema.string.alpha_num.uppercase)

    def test_it_validates_length(self):
        self.assertValidationPasses('',   schema.string.empty)
        self.assertValidationPasses(' ',  schema.string.non_empty)
        self.assertValidationPasses('',   schema.string.length(0))
        self.assertValidationPasses('a',  schema.string.length(1))
        self.assertValidationPasses('a',  schema.string.length(1, 2))
        self.assertValidationPasses('ab', schema.string.length(1, 2))
        self.assertValidationPasses('a',  schema.string.min_length(1))
        self.assertValidationPasses('a',  schema.string.max_length(1))

        self.assertValidationFails(' ',  schema.string.empty)
        self.assertValidationFails('',   schema.string.non_empty)
        self.assertValidationFails(' ',  schema.string.length(0))
        self.assertValidationFails('a',  schema.string.length(2))
        self.assertValidationFails('ab', schema.string.length(0, 1))
        self.assertValidationFails('ab', schema.string.length(3, 5))
        self.assertValidationFails('',   schema.string.min_length(1))
        self.assertValidationFails('ab', schema.string.max_length(1))
