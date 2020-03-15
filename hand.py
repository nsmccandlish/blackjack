from typing import Set

import config
from card import Card


def can_split(card1: Card, card2: Card) -> bool:
    # If split matching only, face cards must match to split
    if config.split_matching_only or card1.number < 10:
        return card1.number == card2.number
    else:
        return (card1.number >= 10) and (card2.number >= 10)


class Hand:
    def __init__(self, bet=None, is_hidden=False):
        self.cards = []
        self.bet = bet
        self.is_hidden = is_hidden
        self.final_status = None

    def add_card(self, card: Card):
        self.cards.append(card)

    @property
    def point_options(self) -> set:
        # Given aces can be 1 or 11, what are all of the hand value options?
        hand_values = {0}
        for card in self.cards:
            values_with_card = set()
            for card_value in card.point_options:
                for hand_value in hand_values:
                    values_with_card.add(hand_value + card_value)
            hand_values = values_with_card

        return hand_values

    @property
    def best_points(self) -> int:
        point_options = self.point_options
        try:
            return max(value for value in point_options if value <= 21)
        except ValueError:
            return min(point_options)

    @property
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.best_points == 21

    def action_options(self) -> Set[str]:
        # potential options: {stand, hit, split, double_down}
        action_options = {"stand"}

        point_options = self.point_options
        if len(self.cards) == 2:
            if can_split(self.cards[0], self.cards[1]):
                action_options.add("split")

            if len(point_options) == 1 and any(
                option in [9, 10, 11] for option in point_options
            ):
                action_options.add("double_down")

        if any(option < 21 for option in point_options):
            # No hitting on blackjack
            action_options.add("hit")

        return action_options

    def __str__(self):
        if self.is_hidden:
            return f"{self.cards[0]}, ??"
        else:
            return ", ".join(str(card) for card in self.cards)
