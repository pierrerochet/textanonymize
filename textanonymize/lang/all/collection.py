from textanonymize.provider import RegexProvider

credit_card_provider = RegexProvider(
    "\\b5[1-5][0-9]{14}\\b",
    "credit_card",
)

email_address_provider = RegexProvider(
    "\\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\\b",
    "email_address",
)
