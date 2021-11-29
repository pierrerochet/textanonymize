from textanonymize.provider import (
    CallableProvider,
    RegexProvider,
)
from phonenumbers import PhoneNumberMatcher


fr_zipcode_provider = RegexProvider(
    "\\b(((?:0[1-9]|[13-8][0-9]|2[ab1-9]|9[0-5])(?:[0-9]{3})?|9[78][1-9](?:[0-9]{2})?))\\b",
    "zipcode",
)

fr_social_security_number_provider = RegexProvider(
    "\\b[12][0-9]{2}[0-1][0-9](2[AB]|[0-9]{2})[0-9]{3}[0-9]{3}[0-9]{2}\\b",
    "social_security_number",
)

fr_phone_number_provider = CallableProvider(
    lambda text: [
        {"start": m.start, "end": m.end, "match": m.raw_string}
        for m in PhoneNumberMatcher(text, "FR")
    ],
    "phone_number",
)

fr_name_provider = RegexProvider.from_word_list(
    "name",
    path=[
        "./textanonymize/lang/fr/resources/patronymes.csv",
        "./textanonymize/lang/fr/resources/prenoms.csv",
    ],
)
