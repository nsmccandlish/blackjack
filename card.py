from dataclasses import dataclass
from typing import Tuple
import config
import sys

suit_strs = {0: "♥", 1: "♠", 2: "♣", 3: "♦"}


number_strs = {1: "A", 11: "J", 12: "Q", 13: "K"}


@dataclass(frozen=True)
class Card:
    number: int
    suit: int

    def __str__(self):
        number_str = number_strs.get(self.number) or str(self.number)
        suit_str = suit_strs[self.suit]
        return f"{number_str}{suit_str}"

    @property
    def point_options(self) -> Tuple[int, ...]:
        # Most numbers only have one value, but aces are special
        if self.number == 1:
            return (1, 11)
        elif self.number >= 10:
            return (10,)
        else:
            return (self.number,)
