from textanonymize.provider import MultiProvider
from textanonymize.lang.all import (
    email_address_provider,
    credit_card_provider,
)
from textanonymize.lang.fr.collection import (
    fr_name_provider,
    fr_phone_number_provider,
    fr_zipcode_provider,
    fr_social_security_number_provider,
)

fr_provider = MultiProvider(
    [
        email_address_provider,
        credit_card_provider,
        fr_zipcode_provider,
        fr_social_security_number_provider,
        fr_phone_number_provider,
        fr_name_provider,
    ]
)
