import random
from card import Card


class Deck:
    def __init__(self, deck_count):
        self._cards = None
        self.deck_count = deck_count
        self.reshuffle()

    def reshuffle(self):
        # Pick up all the cards and shuffle them back into the deck
        new_deck = []
        for suit in range(4):
            for number in range(1, 14):
                new_deck.extend([Card(suit=suit, number=number)] * self.deck_count)
        random.shuffle(new_deck)
        self._cards = new_deck

    def get_next_card(self) -> Card:
        return self._cards.pop()

    def __len__(self):
        return len(self._cards)
