import config
from blackjack_game import BlackJackCLI

setup_message = (
    """
Welcome to Blackjack!
Bets must be integer values.
Blackjack pays %s:1
To select an action, type that option or the first character of that option.
Have fun!
"""
    % config.blackjack_payout
)

if __name__ == "__main__":
    print("\n" * 100)
    print(setup_message)
    dealer = BlackJackCLI()
    try:
        dealer.play_game()
    except (KeyboardInterrupt, EOFError):  # ctrl-c, ctrl-d
        print("\nGoodbye.\n")
