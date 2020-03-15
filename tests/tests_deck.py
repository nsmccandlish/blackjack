from card import Card
from deck import Deck


def test_deck():
    deck = Deck(1)
    assert len(deck) == 52
    assert Card(1, 0) in deck._cards
    assert Card(13, 3) in deck._cards

    next = deck.get_next_card()
    assert len(deck) == 51
    assert next not in deck._cards
