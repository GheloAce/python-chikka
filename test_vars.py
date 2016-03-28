# Sample test_var, copy this and create your own at `chikka` directory.

CLIENT_ID = "CLIENT_ID"
SECRET_KEY = "SECRET_KEY"
SHORTCODE = "SHORTCODE"
MOBILES = [
    # Preferably a number you own.
    "091812345678",
    "+63 919 123 4567",
]

try:
    # noinspection PyUnresolvedReferences,PyPackageRequirements
    from phonenumbers import parse
except ImportError:
    pass
else:
    MOBILES += [parse(_, region="PH") for _ in MOBILES]
