from copy import copy

import config
from lib.cli_utils import (
    get_user_input_integer,
    get_user_string_input,
    make_string_green,
)
from deck import Deck
from hand import Hand
from player import Player


class BlackJackGame:
    # Holds the state / state control on the game
    def __init__(self, player_count):
        self.players = [
            Player(i + 1, config.starting_money) for i in range(player_count)
        ]
        self._deck = Deck(config.deck_count)
        self.dealer_hand = Hand(is_hidden=True)

    @property
    def dealer_has_blackjack(self):
        return self.dealer_hand.is_blackjack

    def deal_card(self, hand):
        hand.add_card(self._deck.get_next_card())

    def deal_initial_hands(self):
        for hand in (
            [hand for player in self.players for hand in player.hands]
            + [self.dealer_hand]
        ) * 2:
            self.deal_card(hand)

    def finalize_wins(self):
        # TODO: unit test this
        dealer_points = self.dealer_hand.best_points
        if dealer_points > 21:
            dealer_points = 0
        self.dealer_hand.is_hidden = False
        for player in self.players:
            for hand in player.hands:
                # TODO: apply colors to outcomes
                hand_points = hand.best_points
                if hand_points > 21 or dealer_points > hand_points:
                    hand.final_status = "Lose"
                elif hand_points > dealer_points:
                    if hand.is_blackjack:
                        player.money += int(hand.bet * (1 + config.blackjack_payout))
                        hand.final_status = "Blackjack!"
                    else:
                        player.money += hand.bet * 2
                        hand.final_status = "Win"
                elif hand_points == dealer_points:
                    player.money += hand.bet
                    hand.final_status = "Tie"

    def check_reshuffle(self) -> bool:
        # Checks if the deck needs to be reshuffled, returns true if it was shuffled
        if len(self._deck) <= int(config.shuffle_threshold * config.deck_count * 52):
            self._deck.reshuffle()
            return True
        else:
            return False

    def reset_hands(self):
        for player in self.players:
            player.hands = []
        self.dealer_hand = Hand(is_hidden=True)


class BlackJackCLI:
    """
    Handles user messaging and interfacing with a BlackJackGame
    """

    def __init__(self):
        self.game: BlackJackGame = None

    def play_game(self):
        # Get number of players, create a game with it, loop until it's over
        player_count = get_user_input_integer(
            "How many players? [1-7]:  ", min_value=1, max_value=7
        )
        self.game = BlackJackGame(player_count)
        while True:
            self.game.reset_hands()
            if self.game.check_reshuffle():
                print("Reshuffling cards into the deck...")

            self.get_player_bets()

            print("Dealing cards...")
            self.game.deal_initial_hands()

            if self.game.dealer_has_blackjack:
                print("Dealer has blackjack!")
            else:
                for player in self.game.players:
                    self.player_turn(player)

            while self.game.dealer_hand.best_points < 17:
                self.game.deal_card(self.game.dealer_hand)

            self.game.finalize_wins()
            print("\nRound Complete.\n")
            self.print_board(finalized=True)
            if not (
                any(player.money > 0 for player in self.game.players)
                and self.ask_next_round()
            ):
                print("Thanks for playing")
                break

    def get_player_bets(self):
        # TODO: allow a single player control multiple initial hands?
        for player in self.game.players:
            if not player.money:
                continue
            message = f"{player.player_name}, you have ${player.money}. Enter your bet amount:  "
            player_bet = get_user_input_integer(
                message, min_value=0, max_value=player.money
            )
            if player_bet:
                player.hands.append(Hand(player_bet))
                player.money -= player_bet
                print(f"{player.player_name} has bet {player_bet}.\n")
            else:
                print(f"{player.player_name} is skipping this round.\n")

    def player_turn(self, player: Player):
        """
        Given a player, for each hand that player controls,
            put them in a queue and loop through until the player is done playing
        """
        hands_to_play_queue = copy(player.hands)
        while hands_to_play_queue:
            print("\n")
            playing_hand = hands_to_play_queue.pop(0)
            self.print_board(playing_hand=playing_hand)

            actions = playing_hand.action_options()
            if playing_hand.bet > player.money:
                actions.discard("double_down")
                actions.discard("split")

            if len(actions) == 1:
                action = actions.pop()
            else:
                message = make_string_green(
                    player.player_name
                ) + ": What action would you like to take on this hand?" "\nOptions: %s:  " % ", ".join(
                    actions
                )
                action = get_user_string_input(message, actions)

            # TODO: move these methods into the game class
            if action == "split":
                new_hand = player.split_hand(playing_hand)
                self.game.deal_card(playing_hand)
                self.game.deal_card(new_hand)
                hands_to_play_queue.insert(0, playing_hand)
                hands_to_play_queue.insert(0, new_hand)
            elif action == "double_down":
                player.double_down(playing_hand)
                self.game.deal_card(playing_hand)
            elif action == "hit":
                self.game.deal_card(playing_hand)
                if playing_hand.best_points > 21:
                    print("Bust :(")
                else:
                    hands_to_play_queue.insert(0, playing_hand)
            elif action == "stand":
                pass
            else:
                raise ValueError(f"Invalid action {action}")

    def print_board(self, playing_hand=None, finalized=False):
        """
        finalized: means the round is over, show who won and lost
        See test for documentation
        """

        print("Dealer:")
        print(self.game.dealer_hand)
        if finalized:
            print("total: %s" % self.game.dealer_hand.best_points)
        print()

        player_hand_outputs = []
        for player in self.game.players:
            for hand in player.hands:
                # Player, bet, cards, points, outcome?
                hand_messages = [
                    player.player_name,
                    f"bet: ${hand.bet}",
                    str(hand),
                    f"total: {hand.best_points}",
                ]
                if finalized:
                    hand_messages.append(hand.final_status)
                # FIXME: need to ignore colors and formatting in message lengths
                print_len = max(len(x) for x in hand_messages)
                hand_messages = [x.ljust(print_len) for x in hand_messages]
                if hand == playing_hand:
                    hand_messages = [make_string_green(val) for val in hand_messages]
                player_hand_outputs.append(hand_messages)
        for line in zip(*player_hand_outputs):
            print(" | ".join(line))
        print()

    def ask_next_round(self):
        print("Player Balances:")
        for player in self.game.players:
            print(f"    {player.player_name}: ${player.money}")
        new_round = get_user_string_input(
            "Play another round? [yes/no]:  ", {"yes", "no"}
        )
        return new_round == "yes"
