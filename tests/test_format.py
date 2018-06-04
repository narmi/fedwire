from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from fedwire import Entry, Tag


class TestEntry(TestCase):
    def setUp(self):
        self.amount = '10.00'
        self.sender = '211111086'
        self.receiver = '011111390'
        self.entry = Entry([
            Tag.sender_supplied_information(production=True),
            Tag.type(Tag.TYPE_FUNDS_TRANSFER, Tag.SUBTYPE_BASIC_FUNDS_TRANSFER),
            Tag.imad(datetime.now(), '4', ''),
            Tag.amount(Decimal(self.amount)),
            Tag.sender_institution(self.sender, ''),
            Tag.receiver_institution(self.receiver, 'Bank of America*'),
            Tag.business_function_code(Tag.CODE_CTR),
        ])

    def test_line(self):
        line = self.entry.line
        self.assertIn(self.amount.replace('.', ''), line)
        self.assertIn(self.sender, line)
        self.assertIn(self.receiver, line)

    def test_invalid(self):
        empty = Entry([])
        self.assertFalse(empty.is_valid())

    def test_invalid_tag(self):
        self.entry.tags.pop()
        self.entry.tags.append(Tag.business_function_code('asdffoobarbaz'))
        self.assertFalse(self.entry.is_valid())

    def test_valid(self):
        self.assertTrue(self.entry.is_valid())


class TestTag(TestCase):
    def test_str(self):
        result = Tag('0000', 'value', 10)
        self.assertEqual('{0000}value', str(result))

    def test_sender_supplied_information(self):
        tag = Tag.sender_supplied_information(production=True)
        self.assertIn('30        P ', str(tag))

    def test_type(self):
        tag = Tag.type(Tag.TYPE_FUNDS_TRANSFER, Tag.SUBTYPE_BASIC_FUNDS_TRANSFER)
        self.assertIn('1000', str(tag))

    def test_imad(self):
        tag = Tag.imad(datetime.now(), '4', '')
        self.assertIn('       4      ', str(tag))

    def test_amount(self):
        tag = Tag.amount(Decimal('10.00'))
        self.assertIn('1000', str(tag))

    def test_sender_institution(self):
        tag = Tag.sender_institution('211111086', '')
        self.assertIn('211111086', str(tag))

    def test_receiver_institution(self):
        tag = Tag.receiver_institution('011111390', 'Bank of America*')
        self.assertIn('011111390', str(tag))

    def test_business_function_code(self):
        tag = Tag.business_function_code(Tag.CODE_CTR)
        self.assertIn(Tag.CODE_CTR, str(tag))

    def test_sender_reference(self):
        tag = Tag.sender_reference('111113*')
        self.assertIn('111113', str(tag))

    def test_beneficiary(self):
        tag = Tag.beneficiary(
            Tag.ID_DEMAND_DEPOSIT_ACCOUNT_NUMBER,
            '987654111*',
            'Test Guy 1*',
            '1 GONE Street**Charlestown, MA 02129*')
        self.assertIn('987654111', str(tag))

    def test_originator(self):
        tag = Tag.originator(
            Tag.ID_DEMAND_DEPOSIT_ACCOUNT_NUMBER,
            '6111111113*',
            'KEVIN DOUGH*',
            '8 FOOD RD**SOMEWHERE, MA 10821*')
        self.assertIn('6111111113', str(tag))

    def test_originator_to_beneficiary(self):
        tag = Tag.originator_to_beneficiary('Test 2*')
        self.assertIn('Test 2', str(tag))
