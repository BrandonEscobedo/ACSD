from abc import ABC
from dataclasses import dataclass


@dataclass
class Entity(ABC):
    id: int | str

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
