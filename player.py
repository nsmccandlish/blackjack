from dataclasses import dataclass

from hand import Hand


@dataclass
class Player:
    player_number: int
    money: int
    hands = []

    @property
    def player_name(self):
        return f"Player {self.player_number}"

    def get_money(self, amount):
        self.money -= amount
        return amount

    def __hash__(self):
        return self.player_number

    def split_hand(self, hand: Hand) -> Hand:
        second_hand = Hand(self.get_money(hand.bet))
        second_hand.add_card(hand.cards.pop())
        self.hands.append(second_hand)
        return second_hand

    def double_down(self, hand: Hand):
        self.get_money(hand.bet)
        hand.bet *= 2
