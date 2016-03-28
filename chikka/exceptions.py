class NullMobileNumberException(Exception):
    pass


class InvalidMobileNumberException(Exception):
    pass


class NullClientIDException(Exception):
    pass


class NullSecretKeyException(Exception):
    pass


class NullShortCodeException(Exception):
    pass


class NullRequestCostException(Exception):
    pass


class MessageIdTooLong(Exception):
    pass


# Excemption According to
# https://api.chikka.com/docs/handling-messages#send-sms
class RequestError(Exception):
    pass


class BadRequest(RequestError):
    pass


class MissingRequiredFields(BadRequest):
    pass


class InvalidMessageID(BadRequest):
    pass


class MessageBodyTooLong(BadRequest):
    pass


class InsufficientTrialCredits(BadRequest):
    pass


class InsufficientCredits(BadRequest):
    pass


class InvalidUsedRequestID(BadRequest):
    pass


class InactiveInvalidAccessCode(BadRequest):
    pass


class InvalidMessageType(BadRequest):
    pass


class InvalidMobileNumberError(BadRequest, InvalidMobileNumberException):
    # From experience of passing an invalid number to the chikka API
    pass


class Unauthorized(RequestError):
    pass


class MethodNotAllowed(RequestError):
    pass


class NotFound(RequestError):
    pass


class ServerError(RequestError):
    pass


class UnknownResponseError(Exception):
    pass
