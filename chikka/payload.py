import re
from requests import Response
import six
from .exceptions import *

try:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from phonenumbers import PhoneNumber, PhoneNumberFormat, format_number, is_valid_number
except ImportError:
    PhoneNumber = None

BAD_REQUEST_DESCRIPTIONS = [
    # Reference: https://api.chikka.com/docs/handling-messages#send-sms
    (re.compile(r"^Missing Required Fields"), MissingRequiredFields),
    (re.compile(r"^Invalid Message ID"), InvalidMessageID),
    (re.compile(r"^Message Body Exceeded Allowed Length"), MessageBodyTooLong),
    (re.compile(r"^Insufficient Trial Credits"), InsufficientTrialCredits),
    (re.compile(r"^Insufficient Credits"), InsufficientCredits),
    (re.compile(r"^Invalid.Used Request ID"), InvalidUsedRequestID),
    (re.compile(r"^Inactive.Invalid Access code"), InactiveInvalidAccessCode),
    (re.compile(r"^Invalid Message Type"), InvalidMessageType),
    # From testing, not found in documents.
    (re.compile(r"^Invalid Mobile Number"), InvalidMobileNumberError)
]
NON_NUMERIC = re.compile("\D+")


class ChikkaPayload(object):
    def __init__(
            self, client_id, secret_key, shortcode,
            mobile_number=None, message=None,
            request_id=None, message_id=None,
            message_type=None, request_cost=None):
        # PRELUDE
        self.__mobile_number = None
        self.__response = None
        # PROCESS
        self.client_id = client_id
        self.secret_key = secret_key
        self.shortcode = shortcode
        self.message = message
        self.request_id = request_id
        self.message_id = message_id
        self.message_type = message_type
        self.request_cost = request_cost
        if mobile_number:
            self.mobile_number = mobile_number

    @property
    def mobile_number(self):
        return self.__mobile_number

    @mobile_number.setter
    def mobile_number(self, mobile_number):
        # HANDLE
        # check and validate mobile number
        if not mobile_number:
            raise NullMobileNumberException
        if PhoneNumber and isinstance(mobile_number, PhoneNumber):
            if not is_valid_number(mobile_number):
                raise InvalidMobileNumberException(mobile_number)
            mobile_str = format_number(mobile_number, PhoneNumberFormat.E164)
        else:
            mobile_str = six.text_type(mobile_number)
        # Remove all non-numeric
        mobile_str = NON_NUMERIC.sub("", mobile_str)
        # e.g. 09991234567
        if len(mobile_str) == 11 and mobile_str.startswith('0'):
            mobile_str = "{}{}".format('63', mobile_str[1:])
        # e.g. 639991234567
        if not re.match('^63[0-9]{10}', mobile_str):
            raise InvalidMobileNumberException(mobile_str)
        # CONCLUDE
        self.__mobile_number = mobile_str

    @mobile_number.deleter
    def mobile_number(self):
        del self.__mobile_number

    @property
    def response(self):
        return self.__response

    @response.setter
    def response(self, value):
        # HANDLE
        assert isinstance(value, Response), "value needs to a subclass of requests.Response"
        # PREPARE
        chikka_json = value.json()
        status, message = chikka_json['status'], chikka_json['message']
        description = chikka_json.get('description', "")
        # PROCESS
        if status == 200:
            self.__response = value
        elif status == 400:
            for description_re, exp_cls in BAD_REQUEST_DESCRIPTIONS:
                if description_re.match(description):
                    raise exp_cls(description)
            raise UnknownResponseError(chikka_json)
        elif status == 401:
            raise Unauthorized
        elif status == 403:
            raise MethodNotAllowed
        elif status == 404:
            raise NotFound
        elif status == 500:
            raise ServerError
        else:
            raise UnknownResponseError(chikka_json)

    @response.deleter
    def response(self):
        del self.__response

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        # Note:  This is for backwards compatibility for users of the 0.5.0
        # who expects a `dict` instead of an object
        # For deprecation
        except AttributeError as exc:
            raise TypeError(exc.message)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __delitem__(self, key):
        delattr(self, key)

    def dict(self):
        return {
            k: v for k, v in
            (
                ('client_id', self.client_id),
                ('secret_key', self.secret_key),
                ('shortcode', self.shortcode),
                ('mobile_number', self.mobile_number),
                ('message', self.message),
                ('request_id', self.request_id),
                ('message_id', self.message_id),
                ('message_type', self.message_type),
                ('request_cost', self.request_cost)
            ) if v}
