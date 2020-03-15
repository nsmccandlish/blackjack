import blackjack_game
from card import Card
from hand import Hand

from player import Player
from unittest.mock import Mock


class MockGame:
    def __init__(self, dealer_hand, players):
        self.dealer_hand = dealer_hand
        self.players = players


class MockHand:
    def __init__(self, hand_str, points=None, bet=None):
        self.hand_str = hand_str
        self.bet = bet
        self.best_points = points

    def __str__(self):
        return self.hand_str


def test_print_board(capsys, monkeypatch):

    interface = blackjack_game.BlackJackCLI()
    player_1 = Player(player_number=1, money=25)
    player_1.hands = [
        MockHand("Full House yay good job", 8, 3),
        MockHand("a", 9, 1500000),
    ]
    player_8 = Player(player_number=8, money=100)
    player_8.hands = [MockHand("Tuesday", 14, 10)]
    interface.game = MockGame(MockHand("asdf1"), [player_1, player_8])
    interface.print_board()
    captured = capsys.readouterr()
    assert (
        captured.out
        == """Dealer:
asdf1

Player 1                | Player 1      | Player 8 
bet: $3                 | bet: $1500000 | bet: $10 
Full House yay good job | a             | Tuesday  
total: 8                | total: 9      | total: 14

"""
    )


def test_print_board_green_hand(capsys):
    interface = blackjack_game.BlackJackCLI()
    player_1 = Player(player_number=1, money=25)
    player_1.hands = [
        MockHand("Full House yay good job", 8, 3),
        MockHand("a", 9, 1500000),
    ]
    player_8 = Player(player_number=8, money=100)
    player_8.hands = [MockHand("Tuesday", 14, 10)]
    interface.game = MockGame(MockHand("asdf1"), [player_1, player_8])
    interface.print_board(playing_hand=player_1.hands[1])
    captured = capsys.readouterr()
    assert (
        captured.out
        == """Dealer:
asdf1

Player 1                | \x1b[92mPlayer 1     \x1b[0m | Player 8 
bet: $3                 | \x1b[92mbet: $1500000\x1b[0m | bet: $10 
Full House yay good job | \x1b[92ma            \x1b[0m | Tuesday  
total: 8                | \x1b[92mtotal: 9     \x1b[0m | total: 14

"""
    )


def test_split_hand(monkeypatch):
    interface = blackjack_game.BlackJackCLI()
    game = blackjack_game.BlackJackGame(1)
    player = game.players[0]
    player.money = 50
    splittable_hand = Hand(20)
    splittable_hand.cards = [Card(3, 3), Card(3, 1)]
    player.hands = [splittable_hand]
    interface.game = game

    monkeypatch.setattr(interface, "print_board", Mock())
    # Have the player split the hand, then stand on each split hand
    monkeypatch.setattr(
        blackjack_game,
        "get_user_string_input",
        Mock(side_effect=["split", "stand", "stand"]),
    )
    monkeypatch.setattr(
        game._deck, "get_next_card", Mock(side_effect=[Card(5, 1), Card(9, 0)])
    )
    interface.player_turn(player)

    assert player.money == 30
    assert len(player.hands) == 2
    assert str(player.hands[0]) == "3♦, 5♠"
    assert str(player.hands[1]) == "3♠, 9♥"
