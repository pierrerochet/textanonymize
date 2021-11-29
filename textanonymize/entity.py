from typing import List, Optional
import re


class Entity:
    def __init__(self, start: int, end: int, match: str, group: str):
        self.start = start
        self.end = end
        self.match = match
        self.group = group

    def __repr__(self):
        return str(dict(self))

    def keys(self):
        return ["start", "end", "match", "group"]

    def __len__(self):
        return len(self.match)

    def __getitem__(self, key):
        for k in self.keys():
            if key == k:
                return getattr(self, key)

    @classmethod
    def from_match(cls, match: re.Match, group: str):
        return cls(
            match.start(),
            match.end(),
            match.group(),
            group,
        )

    def __lt__(self, other: "Entity") -> bool:
        if self.start == other.start:
            return len(self.match) < len(other.match)
        else:
            return self.start < other.start

    def is_overlapped(self, other: "Entity") -> bool:
        if other.start >= self.start and other.start <= self.end:
            return True
        if other.end >= self.start and other.start <= self.end:
            return True
        return False


class EntityCollection:
    def __init__(self, ents: Optional[List[Entity]] = None):
        self.ents = [] if ents is None else ents
        self.counts = {}
        for ent in self.ents:
            self.counts[ent.group] = self.counts.get(ent.group, 0) + 1

    def __len__(self):
        return len(self.ents)

    def __repr__(self):
        return str(
            {
                "ents": self.ents,
                "counts": self.counts,
            }
        )

    def merge(self, other_ent_collec: "EntityCollection") -> None:
        for ent in other_ent_collec.ents:
            self.counts[ent.group] = self.counts.get(ent.group, 0) + 1
            self.ents.append(ent)

    def replace(self, text: str, keep_overlapped=False) -> str:
        format_ent = lambda ent_group: f"<privacy_data: {ent_group}>"
        new_text = ""

        if keep_overlapped:
            ents_kept = self.ents[:]
        else:
            ents_kept = []
            for i, ent in enumerate(self.ents):
                for j, other_ent in enumerate(self.ents):
                    if i == j:
                        continue
                    if ent.is_overlapped(other_ent):
                        if len(ent) < len(other_ent):
                            break
                        if (len(ent) == len(other_ent)) and (ent.start > ent.start):
                            break
                else:
                    ents_kept.append(ent)

        ents = sorted(ents_kept)
        sub_text_start = 0
        for ent in ents:
            new_text += text[sub_text_start : ent.start] + format_ent(ent.group)
            sub_text_start = ent.end
        new_text += text[sub_text_start:]

        return new_text
