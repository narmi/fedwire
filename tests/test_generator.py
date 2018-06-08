from datetime import datetime
from decimal import Decimal
from unittest import TestCase

from fedwire import Entry, Tag, FedwireFile


class TestFedwireFile(TestCase):
    def setUp(self):
        self.entries = [
            Entry([
                Tag.sender_supplied_information(production=True),
                Tag.type(Tag.TYPE_FUNDS_TRANSFER, Tag.SUBTYPE_BASIC_FUNDS_TRANSFER),
                Tag.imad(datetime.now(), '4', ''),
                Tag.amount(Decimal('10.00')),
                Tag.sender_institution('211111086', ''),
                Tag.sender_reference('111113'),
                Tag.receiver_institution('011111390', 'Bank of America'),
                Tag.business_function_code(Tag.CODE_CTR),
                Tag.beneficiary(
                  Tag.ID_DEMAND_DEPOSIT_ACCOUNT_NUMBER,
                  '987654111',
                  'Test Guy 1',
                  '1 Walker Street\n\nCharlestown, MA 02129'),
                Tag.originator(
                    Tag.ID_DEMAND_DEPOSIT_ACCOUNT_NUMBER,
                    '6111111113',
                    'KEVIN DOUGH',
                    '8 FOOD RD\n\nSOMEWHERE, MA 10821'),
                Tag.originator_to_beneficiary('Test 2'),
            ])
        ]

    def test_add_batch(self):
        wire_file = FedwireFile()
        wire_file.add_batch(self.entries)
        wire_file.add_batch(self.entries)
        self.assertEqual(len(wire_file.entries), 2)

    def test_str(self):
        wire_file = FedwireFile(entries=self.entries)
        self.assertEqual(str(wire_file).count('\n'), 1)
