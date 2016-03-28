import os
import binascii
import requests
from .exceptions import *
from .payload import *

# add local_settings.py to .gitignore
# variables in local_settings optional, it won't be uploaded
try:
    from local_settings import CLIENT_ID, SECRET_KEY, SHORTCODE
except ImportError:
    CLIENT_ID = None
    SECRET_KEY = None
    SHORTCODE = None

API_URL = 'https://post.chikka.com/smsapi/request'


class Chikka(object):
    def __init__(self, client_id, secret_key, shortcode):
        self.client_id = client_id
        self.secret_key = secret_key
        self.shortcode = shortcode

    def send(
            self, mobile_number, message, message_id=None,
            request_id=None, request_cost=None):
        payload = self._prepare_payload()
        payload.mobile_number = mobile_number
        payload.request_id = request_id

        # check if `request_id` was passed
        # which means a message was received
        # and determines `message_type` and `request_cost`
        if request_id:
            payload.message_type = 'REPLY'
            # since message type is REPLY user is required to supply
            # the request cost
            if request_cost:
                payload.request_cost = request_cost
            else:
                raise NullRequestCostException
        else:
            payload.message_type = 'SEND'

        # `message_id` can be passed to this method
        # this can be useful to track messages sent
        # however if `message_id` was not provided
        # we will generate a random `message_id`
        payload.message_id = message_id or binascii.hexlify(os.urandom(16))

        payload.message = message
        payload.response = requests.post(API_URL, data=payload.dict())

        return payload

    def _prepare_payload(self, *args, **kwargs):

        client_id = getattr(self, 'client_id', CLIENT_ID)
        secret_key = getattr(self, 'secret_key', SECRET_KEY)
        shortcode = getattr(self, 'shortcode', SHORTCODE)

        if not client_id:
            raise NullClientIDException("Error: Your Client ID is required.")
        if not secret_key:
            raise NullSecretKeyException("Error: Your Secret Key is required.")
        if not shortcode:
            raise NullShortCodeException("Error: Your shortcode is required.")

        return ChikkaPayload(client_id, secret_key, shortcode, *args, **kwargs)
