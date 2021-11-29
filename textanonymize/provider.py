from typing import List, Union, Callable
from textanonymize.entity import Entity, EntityCollection
import re


class Provider:
    def __init__(self, group: str):
        self.group = group

    def replace(self, text: str) -> str:
        ent_collec = self.find(text)
        text_anonymized = ent_collec.replace(text)
        return text_anonymized


class MultiProvider(Provider):
    def __init__(self, providers: List[Provider]):
        self.providers = providers

    def find(self, text: str) -> EntityCollection:
        ent_collec = EntityCollection()
        for p in self.providers:
            ent_collec.merge(p.find(text))
        return ent_collec


class RegexProvider(Provider):
    def __init__(self, pattern: str, group: str):
        super().__init__(group)
        self.pattern = re.compile(pattern)

    @classmethod
    def from_word_list(
        cls,
        group: str,
        path: Union[str, List[str], None] = None,
        words: Union[str, List[str], None] = None,
        ignore_case: bool = True,
    ):

        words = words if words else []

        if type(path) == str:
            with open(path, "r", encoding="utf8") as stream:
                words += [w.strip() for w in stream]

        if type(path) == list:
            for p in path:
                with open(p, "r", encoding="utf8") as stream:
                    words += [w.strip() for w in stream]

        words_given = words[:]
        words += [w.replace(" ", "-") for w in words_given if " " in w]

        if ignore_case:
            pattern = f"(?i)\\b({'|'.join(words)})\\b"
        else:
            pattern = f"\\b({'|'.join(words)})\\b"
        return cls(pattern, group)

    def find(self, text: str) -> EntityCollection:
        return EntityCollection(
            [Entity.from_match(m, self.group) for m in self.pattern.finditer(text)]
        )


class CallableProvider(Provider):
    def __init__(self, callable: Callable[[str], dict], group: str):
        super().__init__(group)
        self.callable = callable

    def find(self, text: str) -> EntityCollection:
        return EntityCollection(
            [
                Entity(m["start"], m["end"], m["match"], self.group)
                for m in self.callable(text)
            ]
        )
