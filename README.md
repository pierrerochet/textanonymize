_textanonymize_ is a python package to anonymize text data.  
⚠ Currently, only __french__ is supported. More languagues can be added later. 


## Installation

```bash
pip install git+https://github.com/pierrerochet/textanonymize.git
```

## How use it


### Detect entities


```python
from textanonymize.lang.fr import fr_provider

text = "Je suis Michel Dupont, mon numéro est 0600000000 et mon adresse email est my@email.com"

ent_collec = fr_provider.find(text)
# {
#     'ents': [
#         {
#             'start': 74, 
#             'end': 86, 
#             'match': 'my@email.com', 
#             'group': 'email_address'
#         }, 
#         {
#             'start': 38, 
#             'end': 48, 
#             'match': '0600000000', 
#             'group': 'phone_number',
#         }, 
#         {
#             'start': 8, 
#             'end': 14, 
#             'match': 'Michel', 
#             'group': 'name',
#         }, 
#         {
#             'start': 15, 
#             'end': 21, 
#             'match': 'Dupont', 
#             'group': 'name'
#         }
#     ], 
#     'counts': {
#         'email_address': 1, 
#         'phone_number': 1, 
#         'name': 2,
#     }
# }

```

### Anonymize text

```python
from textanonymize.lang.fr import fr_provider

text = "Je suis Michel Dupont, mon numéro est 0600000000 et mon adresse email est my@email.com"

text_an = fr_provider.replace(text)
# or alternatively
ent_collec = fr_provider.find(text)
text_an = ent.collec.replace(text)

# Je suis <privacy_data: name> <privacy_data: name>, mon numéro est <privacy_data: phone_number> et mon adresse email est <privacy_data: email_address>
```



## Use specific provider

```python
from textanonymize.lang.fr import fr_name_provider

text = "Je suis Michel Dupont, mon numéro est 0600000000 et mon adresse email est my@email.com"
ent_collec = fr_phone_number_provider.find(text)
```

Here is specific providers available :


| Standard |
| ------------- |
| email_address_provider |
| credit_card_provider |



| French |
| ------------- |
| fr_name_provider |
| fr_phone_number_provider |
| fr_zipcode_provider | 
| fr_social_security_number_provider |


## Combine saveral provider with a MultiProvider

```python

from textanonymize.provider import MultiProvider
from textanonymize.lang.fr import (
    fr_name_provider,
    fr_phone_number_provider,
)


provider = MultiProvider([
        fr_name_provider,
        fr_phone_number_provider,
    ])

text = "Je suis Michel Dupont, mon numéro est 0600000000 et mon adresse email est my@email.com"
ent_collec = fr_provider.find(text)
```



## Build a custom provider

textanonymize provides class to help you to build your custom providers.

```python
from textanonymize.provider import CallableProvider
import re

def find_with_regex(text):
    return [
        {"start": m.start(), "end": m.end(), "match": m.group()}
        for m in re.finditer(
            "\\b[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*\\b",
            text,
        )
    ]

callable_provider = CallableProvider(find_with_regex, "email_address")
callable_provider.replace("Mon adresse email est my@email.com")
# Mon adresse email est <privacy_data: email_address>
```

Please note that the callable must always return a dict with keys : _start_, _end_ and _match_


