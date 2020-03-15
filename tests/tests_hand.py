import pytest
from card import Card
from hand import Hand, config, can_split


def test_point_options():
    hand = Hand()
    hand.add_card(Card(3, 1))
    assert hand.point_options == {3}

    hand.add_card(Card(1, 1))
    assert hand.point_options == {4, 14}

    hand.add_card(Card(1, 1))
    assert hand.point_options == {5, 15, 25}


def test_hand_print():
    hand = Hand()
    hand.add_card(Card(3, 1))
    hand.add_card(Card(11, 2))

    assert str(hand) == "3♠, J♣"


@pytest.mark.parametrize(
    "cards, split_matching_only, expected_can_split",
    [
        [(Card(3, 1), Card(11, 2)), True, False],
        [(Card(3, 1), Card(3, 2)), True, True],
        [(Card(10, 1), Card(12, 2)), False, True],
        [(Card(10, 1), Card(12, 2)), True, False],
    ],
)
def test_can_split(monkeypatch, cards, split_matching_only, expected_can_split):
    monkeypatch.setattr(config, "split_matching_only", split_matching_only)
    assert can_split(cards[0], cards[1]) == expected_can_split
