from textanonymize import __version__
from textanonymize.entity import Entity, EntityCollection
from textanonymize.provider import MultiProvider, RegexProvider, CallableProvider
from textanonymize.lang.fr import fr_provider
import re


def test_version():
    assert __version__ == "0.1.0"


def test_entity():
    ent1 = Entity(31, 36, "06000", "phone_number")
    assert ent1["start"] == 31
    assert ent1["end"] == 36
    assert ent1["match"] == "06000"
    assert ent1["group"] == "phone_number"

    text = "Mon numéro de téléphone est le 0600000000."
    match = re.search(r"\d{10}", text)
    ent2 = Entity.from_match(match, "phone_number")
    assert ent2["start"] == 31
    assert ent2["end"] == 41
    assert ent2["match"] == "0600000000"
    assert ent2["group"] == "phone_number"

    assert (ent2 > ent1) == True


def test_overlapped_entities():
    text = "Voici mon téléphone: 06-00-00-00-00"
    ent_collec = fr_provider.find(text)
    assert len(ent_collec) == 2

    text_an = ent_collec.replace(text)
    assert text_an == "Voici mon téléphone: <privacy_data: phone_number>"


def test_entity_collection():

    text = (
        "Mon numéro de téléphone est le 0600000000. Mon adresse email est my@email.com"
    )
    match = re.search(
        "\\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\\b",
        text,
    )
    ent = Entity.from_match(match, "email_address")
    ent_collect = EntityCollection([ent])
    ent_collect.merge(EntityCollection([Entity(31, 41, "0676367609", "phone_number")]))

    assert len(ent_collect) == 2
    assert ent_collect.counts == {"phone_number": 1, "email_address": 1}
    text_an = ent_collect.replace(text)
    assert (
        text_an
        == "Mon numéro de téléphone est le <privacy_data: phone_number>. Mon adresse email est <privacy_data: email_address>"
    )


def test_regex_provider():
    text = "Mon adresse email est my@email.com"

    email_address_provider = RegexProvider(
        "\\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\\b",
        "email_address",
    )
    ents_collec = email_address_provider.find(text)
    assert ents_collec.counts["email_address"] == 1

    ent = ents_collec.ents[0]
    assert ent["start"] == 22
    assert ent["end"] == 34
    assert ent["match"] == "my@email.com"
    assert ent["group"] == "email_address"


def test_callable_provider():
    text = "Mon adresse email est my@email.com"

    def find_with_regex(text):
        return [
            {"start": m.start(), "end": m.end(), "match": m.group()}
            for m in re.finditer(
                "\\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\\b",
                text,
            )
        ]

    callable_provider = CallableProvider(find_with_regex, "email_address")
    ent_collec = callable_provider.find(text)

    assert ent_collec.counts["email_address"] == 1

    ent = ent_collec.ents[0]
    assert ent["start"] == 22
    assert ent["end"] == 34
    assert ent["match"] == "my@email.com"
    assert ent["group"] == "email_address"


def test_multi_provider():
    text = (
        "Mon numéro de téléphone est le 0600000000. Mon adresse email est my@email.com"
    )

    provider = MultiProvider(
        [
            RegexProvider("\\b\\d{10}\\b", "phone_number"),
            RegexProvider(
                "\\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\\b",
                "email_address",
            ),
        ]
    )

    ent_collec = provider.find(text)

    assert ent_collec.counts["email_address"] == 1
    assert ent_collec.counts["phone_number"] == 1

    ent1 = ent_collec.ents[0]
    assert ent1["start"] == 31
    assert ent1["end"] == 41
    assert ent1["match"] == "0600000000"
    assert ent1["group"] == "phone_number"

    ent2 = ent_collec.ents[1]
    assert ent2["start"] == 65
    assert ent2["end"] == 77
    assert ent2["match"] == "my@email.com"
    assert ent2["group"] == "email_address"


def test_fr_provider():
    text = "Je suis Michel Dupont, mon numéro est 0600000000 et mon adresse email est my@email.com"
    ent_collec = fr_provider.find(text)

    assert len(ent_collec) == 4

    assert ent_collec.counts == {"email_address": 1, "phone_number": 1, "name": 2}
    print(ent_collec.replace(text))
    assert dict(ent_collec.ents[0]) == {
        "start": 74,
        "end": 86,
        "match": "my@email.com",
        "group": "email_address",
    }

    assert dict(ent_collec.ents[1]) == {
        "start": 38,
        "end": 48,
        "match": "0600000000",
        "group": "phone_number",
    }

    assert dict(ent_collec.ents[2]) == {
        "start": 8,
        "end": 14,
        "match": "Michel",
        "group": "name",
    }

    assert dict(ent_collec.ents[3]) == {
        "start": 15,
        "end": 21,
        "match": "Dupont",
        "group": "name",
    }
