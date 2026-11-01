#!/usr/bin/env python3
from blackjack import Blackjack

test = Blackjack()
test.player_name = str(input("please enter your name: ").strip())
decks = int(input("how many decks would you like? ").strip())
bets = int(input("if you want bets on type 1 else 2: ").strip())
print("The settings name, decks, bets reset on exit\n")
print("h or hit for hit\nstand or s for stand\nsurrender for surrender\nshow for show drawn cards\ndouble for double\nsplit for split\n")

def main():
    test.load_stats()
    if test.money_total <= 0:
        test.money_total = 100
    print(f"Monies {test.money_total}        Best Hiscore {test.score}\n{test.total_wins} Total Wins          {test.total_loses} Total Loses\n"
          f"Draws {test.total_draws}")
    if bets == 1:
        test.bet(int(input(f"how much do you want to bet? ")))
    test.make_deck(decks)
    test.shuffle()
    hidden = test.deck.pop()
    test.dealer_hit()
    test.hit()
    test.hit()
    test.nat21(hidden)

    while test.hands[0]:
        test1 = input() or "69"
        test1 = test1.strip().lower()
        if test1 in "h, hit":
            test.hit()
        elif test1 in "s, stand":
            test.stand()
        elif test1 in "split":
            test.split()
        elif test1 in "surrender":
            test.surrender()
        elif test1 in "show":
            test.show_drawn_cards()
        elif test1 in "double":
            test.double()
        else:
            print("no exist")

    test.save_stats()

    play_again = input("would you like to play again? (y/n) ")
    if play_again.lower() == "y":
        main()
    else:
        exit()

if __name__ == '__main__':
    main()