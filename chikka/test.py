# coding=utf-8
#
# To run, preferably:
# $ python2.7 -m unittest discover
#
from unittest import TestCase, main
from logging import getLogger
from .core import *
from .payload import *
from .exceptions import *

try:
    from .test_vars import *
except ImportError:
    raise ImportError(
        "Create a file named `test_vars.py` in the same directory, and assign: "
        "CLIENT_ID, SECRET_KEY, SHORTCODE and MOBILES.")
else:
    assert isinstance(MOBILES, list), "MOBILES needs to be as list of valid mobile numbers."
    assert len(MOBILES), "MOBILES must have at least 1 valid mobile number."

try:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from phonenumbers import PhoneNumber, PhoneNumberFormat, format_number
except ImportError:
    PhoneNumber = None

log = getLogger(__name__)


class TestChikka(TestCase):
    @classmethod
    def set_test_variables(cls):
        cls.client_id = CLIENT_ID
        assert cls.client_id
        cls.secret_key = SECRET_KEY
        assert cls.secret_key
        cls.short_code = SHORTCODE
        assert cls.short_code
        cls.valid_mobiles = MOBILES
        cls.invalid_mobiles = [
            "009279517459",
            "+551155256325"]
        cls.chikka_instance = Chikka(cls.client_id, cls.secret_key, cls.short_code)

    def test_chikka_instance(self):
        self.assertIsInstance(self.chikka_instance, Chikka)

    def test_basic_message(self):
        message = "@test_basic_message {}"
        for mobile in self.valid_mobiles:
            chikka_response = self.chikka_instance.send(mobile, message.format(mobile))
            self.assertIsInstance(chikka_response, ChikkaPayload)
            self.assertIsInstance(chikka_response.response, Response)
            self.assertTrue(chikka_response['client_id'], "Not a `dict()` like instance.")

    def test_invalid_mobile(self):
        message = "@test_invalid_mobile"
        for mobile in self.invalid_mobiles:
            try:
                chikka_response = self.chikka_instance.send(mobile, message)
            except InvalidMobileNumberException:
                pass
            except Exception as exc:
                self.fail("`{}` type of error was raised for `{}`".format(exc, mobile))
            else:
                self.fail([
                    "`{}` was seen as valid.".format(mobile),
                    {
                        'dict': chikka_response.dict(),
                        'json': chikka_response.response.json()
                    }])

    def test_unicode_message(self):
        message = "@test_unicode_message Hello βeta, Niño."
        self.chikka_instance.send(self.valid_mobiles[0], message)

    def test_too_long_message(self):
        message = "Some Test." * 60
        try:
            self.chikka_instance.send(self.valid_mobiles[0], message)
        except Exception as exc:
            self.assertIsInstance(exc, MessageBodyTooLong)


TestChikka.set_test_variables()
