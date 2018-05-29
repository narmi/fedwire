from decimal import Decimal, ROUND_HALF_UP


class BaseFedwireException(Exception):
    """
    Base class for all fedwire exceptions
    """
    pass


class FedwireConfigurationException(BaseFedwireException):
    """
    Class for API Configuration Exceptions
    """
    pass


TAG_SENDER_SUPPLIED_INFORMATION = 1500
TAG_TYPE = 1510
TAG_IMAD = 1520  # Input Message Accountability Data
TAG_AMOUNT = 2000
TAG_SENDER_DEPOSITORY_INSTITUTION = 3100
TAG_RECEIVER_DEPOSITORY_INSTITUTION = 3400
TAG_BUSINESS_FUNCTION_CODE = 3600

FORMAT_VERSION = '30'
ENVIRONMENT_TEST = 'T'
ENVIRONMENT_PRODUCTION = 'P'
DUPLICATION_ORIGINAL = ' '
DUPLICATION_RESEND = 'P'


class Entry:
    REQUIRED_TAGS = [
        TAG_SENDER_SUPPLIED_INFORMATION,
        TAG_TYPE,
        TAG_IMAD,
        TAG_AMOUNT,
        TAG_SENDER_DEPOSITORY_INSTITUTION,
        TAG_RECEIVER_DEPOSITORY_INSTITUTION,
        TAG_BUSINESS_FUNCTION_CODE,
    ]

    def __init__(self, tags=[]):
        self.tags = tags

    @property
    def line(self):
        sorted_tags = sorted(self.tags, key=lambda t: t.name)
        return ''.join([str(t) for t in sorted_tags])

    def is_valid(self):
        for tag in self.tags:
            if not tag.is_valid():
                return False

        tag_names = [tag.name for tag in self.tags]
        if len(set(self.REQUIRED_TAGS) - set(tag_names)) > 0:
            return False

        return True


class Tag:
    CODE_BTR = 'BTR'  # Bank Transfer (Beneficiary is a bank)
    CODE_CKS = 'CKS'  # Check Same Day Settlement
    CODE_CTP = 'CTP'  # Customer Transfer Plus
    CODE_CTR = 'CTR'  # Customer Transfer (not to a bank) Deposit to Sender’s Account
    CODE_DRC = 'DRC'  # Customer or Corporate Drawdown Request
    CODE_FFR = 'FFR'  # Fed Funds Returned
    CODE_FFS = 'FFS'  # Fed Funds Sold

    """
    A funds transfer in which the sender and/or receiver may be a bank or a
    third party (i.e., customer of a bank).
    """
    TYPE_FUNDS_TRANSFER = '10'
    """
    A funds transfer to or from a foreign central bank or government or
    international organization with an account at the Federal Reserve Bank of
    New York.
    """
    TYPE_FOREIGN_TRANSFER = '15'
    """
    A funds transfer between Fedwire Funds Service participants.
    """
    TYPE_SETTLEMENT_TRANSFER = '16'

    """
    A basic value funds transfer.
    """
    SUBTYPE_BASIC_FUNDS_TRANSFER = '00'
    """
    A non-value request for reversal of a funds transfer originated on the
    current business day.
    """
    SUBTYPE_REQUEST_FOR_REVERSAL = '01'
    """
    A value reversal of a funds transfer received on the current business day.
    May be used in response to a subtype code ‘01’ Request for Reversal.
    """
    SUBTYPE_REVERSAL_OF_TRANSFER = '02'
    """
    A non-value request for a reversal of a funds transfer originated on a
    prior business day.
    """
    SUBTYPE_REQUEST_FOR_REVERSAL_PRIOR_DAY_TRANSFER = '07'
    """
    A value reversal of a funds transfer received on a prior business day. May
    be used in response to a subtype code ‘07’ Request for Reversal of a Prior
    Day Transfer.
    """
    SUBTYPE_REVERSAL_PRIOR_DAY_TRANSFER = '08'
    """
    A non-value request for the receiver to send a funds transfer to a
    designated party.
    """
    SUBTYPE_REQUEST_CREDIT = '31'
    """
    A value funds transfer honoring a subtype 31 request for credit.
    """
    SUBTYPE_FUNDS_TRANSFER_HONOR_REQUEST_FOR_CREDIT = '32'
    """
    A non-value message indicating refusal to honor a subtype 31 request for
    credit.
    """
    SUBTYPE_REFUSAL_HONOR_REQUEST_FOR_CREDIT = '33'
    """
    A non-value message used to communicate questions and information that is
    not covered by a specific subtype.
    """
    SUBTYPE_SERVICE_MESSAGE = '90'

    @classmethod
    def sender_supplied_information(klass, production=False, resend=False):
        user_request_correlation = ' ' * 8  # all spaces is blank
        environment = ENVIRONMENT_PRODUCTION if production else ENVIRONMENT_TEST
        duplication = DUPLICATION_RESEND if resend else DUPLICATION_ORIGINAL
        return klass(
            TAG_SENDER_SUPPLIED_INFORMATION,
            FORMAT_VERSION + user_request_correlation + environment + duplication,
            12)

    @classmethod
    def type(klass, type, subtype):
        return klass(TAG_TYPE, type + subtype, 4)

    @classmethod
    def imad(klass, input_date, source, sequence):
        # YYYYMMDD
        # Input Source (8 characters)
        # Input Sequence Number (6 characters)
        value = input_date.strftime('%Y%m%d') + \
            (make_space(8 - len(source)) + source) + \
            (make_space(6 - len(sequence)) + sequence)
        return klass(TAG_IMAD, value, 22)

    @classmethod
    def amount(klass, value):
        # 12 numeric, right-justified with leading zeros, an implied decimal
        # point and no commas; e.g., $12,345.67 becomes 000001234567
        cents = Decimal('0.01')
        amount = value.quantize(cents, ROUND_HALF_UP) * 100
        formatted_amount = str(amount).replace('.', '').zfill(12)
        return klass(TAG_AMOUNT, formatted_amount, 12)

    @classmethod
    def sender_institution(klass, routing, name):
        # Sender ABA Number (9 characters)
        # Sender Short Name (18 characters)
        return klass(TAG_SENDER_DEPOSITORY_INSTITUTION, routing + name, 27)

    @classmethod
    def receiver_institution(klass, routing, name):
        return klass(TAG_RECEIVER_DEPOSITORY_INSTITUTION, routing + name, 27)

    @classmethod
    def business_function_code(klass, business, transaction=''):
        return klass(TAG_BUSINESS_FUNCTION_CODE, business + transaction, 6)

    def __init__(self, name, value, max_length):
        self.name = name
        self.value = str(value)
        self.max_length = max_length

    def is_valid(self):
        return len(self.value) <= self.max_length

    def __str__(self):
        value = ''.join(self.value)
        # Double the curly braces to escape them. :shrug:
        return '{{{}}}{}'.format(self.name, value)


def make_space(space_padding=0):
    """
    Return string with x number of spaces. Defaults to 0.
    """
    space = ''

    for i in range(space_padding):
        space += ' '

    return space
