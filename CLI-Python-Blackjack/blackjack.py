import random

class Blackjack:
    def __init__(self):
        self.cards = ["Ace", 2, 3, 4, 5, 6, 7, 8, 9, 10, "Jack", "Queen", "King"]
        self.suits = ["Clubs♣", "Diamonds♦", "Hearts♥", "Spades♠"]
        self.deck = []
        self.hands = [[]]
        self.player_count = sum(self.hands[0])
        self.dealer_card_values = list()
        self.dealer_count = sum(self.dealer_card_values)
        self.drawn_cards = ["D for Dealer", "P for Player"]
        self.player_name = "bob"
        self.money_total = 0
        self.bets = 0
        self.total_wins = 0
        self.total_loses = 0
        self.total_draws = 0
        self.score = 0
        self.can_surrender = True
        self.money = "bitcoins"

    def make_deck(self, decks=1):
        while decks > 0:
            decks -= 1
            for suit in self.suits:
                for card in self.cards:
                    self.deck.append(f"{card} of {suit}")

    def shuffle(self):
        random.shuffle(self.deck)

    def load_stats(self):
        with open("Stats.txt", "r") as f:
            lines = f.readlines()
            self.money_total = int(lines[0])
            self.total_wins = int(lines[1])
            self.total_loses = int(lines[2])
            self.total_draws = int(lines[3])
            self.score = int(lines[4])

    def save_stats(self):
        with open("Stats.txt", "w") as f:
            if self.money_total > self.score:
                self.score = self.money_total
            f.writelines([f"{str(self.money_total)}\n", f"{str(self.total_wins)}\n", f"{str(self.total_loses)}\n"
            ,f"{str(self.total_draws)}\n", f"{str(self.score)}\n"              ])

    def nat21(self, hidden=None):
        if ((len(self.hands[0]) == 2 and sum(self.hands[0]) == 21 and hidden[:1] == "A" and
             sum(self.dealer_card_values) == 10 and len(self.dealer_card_values) == 1) or
                (len(self.hands[0]) == 2 and sum(self.hands[0]) == 21 and hidden[:2] in ("10", "Ja", "Qu", "Ki") and
                 sum(self.dealer_card_values) == 11 and len(self.dealer_card_values) == 1)):
            if self.bets > 0:
                print(f"Bets Returned: {self.bets}")
            self.money_total += self.bets
            print(f"Nat21 Draw!")
            self.reset()

        elif ((len(self.hands[0]) == 2 and sum(self.hands[0]) == 21 and hidden[:1] != "A" and
               sum(self.dealer_card_values) != 10 and len(self.dealer_card_values) == 1) or
                (len(self.hands[0]) == 2 and sum(self.hands[0]) == 21 and hidden[:2] in ("10", "Ja", "Qu", "Ki") and
                 sum(self.dealer_card_values) != 11 and len(self.dealer_card_values) == 1)):
            if self.bets > 0:
                print(f"{self.bets * 2.5} Won!")
            self.money_total += round((self.bets * 2.5))
            print(f"Nat21 Win for {self.player_name}!!")
            self.reset()

        elif  ((len(self.hands[0]) == 2 and sum(self.hands[0]) != 21 and hidden[:1] == "A" and
                sum(self.dealer_card_values) == 10 and len(self.dealer_card_values) == 1) or
                (len(self.hands[0]) == 2 and sum(self.hands[0]) == 21 and hidden[:2] in ("10", "Ja", "Qu", "Ki") and
                 sum(self.dealer_card_values) == 11 and len(self.dealer_card_values) == 1)):
            if self.bets > 0:
                print(f"{self.bets} Lost!")
            print(f"Nat21 Loss Dealer Wins!")
            self.reset()

    def double(self, allow_negatives=False):
        if len(self.hands[0]) > 2:
            print("To many cards!")
        elif allow_negatives:
            print(f"Double Allowed!")
            self.money_total -= self.bets
            self.bets += self.bets
            self.hit()
            self.stand()
        elif self.money_total >= self.bets:
            print(f"Double Allowed!")
            self.money_total -= self.bets
            self.bets += self.bets
            self.hit()
            self.stand()
        else:
            print("Not enough money!")

    def reset(self):
        if len(self.hands) == 1:
            self.deck = []
            self.drawn_cards = []
            self.player_count = 0
            self.dealer_count = 0
            self.bets = 0
            self.hands = [[]]
            self.dealer_card_values = list()
            self.can_surrender = True
        else:
            del self.hands[0]
            self.player_count = 0
            self.dealer_count = 0
            self.dealer_card_values = list()
            print(f"Hands Remaining {len(self.hands)}")
            print(f"Hand Value {self.hands[0]}")

    def stand(self, hidden=None):
        print("Showing hidden card")
        if hidden is not None:
            self.dealer_hit(hidden)
        while self.dealer_count < self.player_count or self.dealer_count < 17 and self.player_count > 0:
            if self.dealer_count < 17:
                self.dealer_hit()
            elif self.player_count > self.dealer_count:
                self.dealer_hit()

    def split(self):
        if not len(self.hands[0]) == 2:
            print("Not two cards!")
        elif self.hands[0][0] == self.hands[0][1] and self.bets > 0 and (self.money_total - self.bets) >= 0:
            self.money_total -= self.bets
            self.can_surrender = False
            print("Splitting Cards!")
            card1, card2 = self.hands[0].pop(0), self.hands[0].pop(0)
            if not len(self.hands[0]):
                del self.hands[0]
            self.hands.append([card1])
            self.hands.append([card2])
            print(f"Hands {len(self.hands)}")
        elif self.hands[0][0] == self.hands[0][1] and self.bets == 0:
            self.can_surrender = False
            print("Splitting Cards!")
            card1, card2 = self.hands[0].pop(0), self.hands[0].pop(0)
            if not len(self.hands[0]):
                del self.hands[0]
            self.hands.append([card1])
            self.hands.append([card2])
            print(f"Hands {len(self.hands)}")
        else:
            print("No money?!")

    def surrender(self):
        if not self.can_surrender:
            print("No surrender after split!")
        elif self.bets > 0:
            back = self.bets / 2
            self.money_total += back
            print(f"{self.bets // 2} Returned")
        print(f"{self.player_name} Surrendered!")
        self.reset()

    def bet(self, bet=None):
        max_bet = self.money_total
        if self.player_count > 0:
            print("No betting in middle of game")
        elif bet > max_bet:
            print("Bet exceeded!")
        elif bet <= max_bet:
            self.bets = bet
            self.money_total -= bet
            print(f"Bet of {self.bets} {self.money} accepted!")

    def ace(self):
        if 11 in self.hands[0] and sum(self.hands[0]) > 21:
            self.hands[0][self.hands[0].index(11)] = 1

    def ace_dealer(self):
        if 11 in self.dealer_card_values and sum(self.dealer_card_values) > 21:
            self.dealer_card_values[self.dealer_card_values.index(11)] = 1

    def win(self):
        self.lose()
        if self.player_count == self.dealer_count and self.player_count != 0 and self.dealer_count >= 17:
            self.total_draws += 1
            print("Draw!")
            if self.bets > 0:
                print(f"Bets Returned: {self.bets}")
            self.money_total += self.bets
            self.reset()
        elif self.player_count > self.dealer_count >= 17:
            self.total_wins += 1
            print(f"{self.player_name} wins!")
            if self.bets > 0:
                print(f"{self.bets * 2} Won!")
            self.money_total += (self.bets * 2)
            self.reset()
        elif 21 >= self.dealer_count > self.player_count and self.dealer_count >= 17:
            self.total_loses += 1
            print("Dealer wins!")
            if self.bets > 0:
                print(f"{self.bets} Lost!")
            self.reset()

    def lose(self):
        if self.player_count > 21:
            self.total_loses += 1
            print(f"{self.player_name} Lose!")
            if self.bets > 0:
                print(f"{self.bets} Lost!")
            self.reset()
        elif self.player_count < self.dealer_count > 21:
            self.total_wins += 1
            print("Dealer loses!")
            if self.bets > 0:
                print(f"{self.bets * 2} Won!")
            self.money_total += (self.bets * 2)
            self.reset()

    def hit(self):
        self.win()
        if len(self.deck) == 0:
            print("Dealing empty deck!")
        else:
            draw = self.deck.pop()
            self.drawn_cards.append(draw + " P")
            print(f"{self.player_name} Drew: {draw}")
            if draw[:1].upper() in ["J", "Q", "K"]:
                self.hands[0].append(10)
                self.ace()
                self.player_count = sum(self.hands[0])
                print(f"{self.player_name} Count: {self.player_count}")
                self.win()
            elif draw[:1].upper() == "A":
                if (self.player_count + 11) > 21:
                    self.hands[0].append(1)
                    self.ace()
                    self.player_count = sum(self.hands[0])
                    print(f"{self.player_name} Count: {self.player_count}")
                    self.win()
                else:
                    self.hands[0].append(11)
                    self.ace()
                    self.player_count = sum(self.hands[0])
                    print(f"{self.player_name} Count: {self.player_count}")
                    self.win()
            else:
                self.hands[0].append(int(draw[:2]))
                self.ace()
                self.player_count = sum(self.hands[0])
                print(f"{self.player_name} Count: {self.player_count}")
                self.win()

    def dealer_hit(self, hidden=None):
        self.win()
        if len(self.deck) == 0:
            print("Dealing empty deck!")
        else:
            draw = (hidden if hidden is not None else self.deck.pop())
            self.drawn_cards.append(draw + " D")
            prin = (f"{draw} + hidden card" if self.dealer_count == 0 else draw)
            print(prin)
            if draw[:1].upper() in ["J", "Q", "K"]:
                self.dealer_card_values.append(10)
                self.ace_dealer()
                self.dealer_count = sum(self.dealer_card_values)
                print(f"Dealer Count: {self.dealer_count}, {self.player_name} Count: {self.player_count}")
                self.win()
            elif draw[:1].upper() in "A":
                if (self.dealer_count + 11) > 21:
                    self.dealer_card_values.append(1)
                    self.ace_dealer()
                    self.dealer_count = sum(self.dealer_card_values)
                    print(f"Dealer Count: {self.dealer_count}, {self.player_name} Count: {self.player_count}")
                    self.win()
                else:
                    self.dealer_card_values.append(11)
                    self.ace_dealer()
                    self.dealer_count = sum(self.dealer_card_values)
                    print(f"Dealer Count: {self.dealer_count}, {self.player_name} Count: {self.player_count}")
                    self.win()
            else:
                self.dealer_card_values.append(int(draw[:2]))
                self.ace_dealer()
                self.dealer_count = sum(self.dealer_card_values)
                print(f"Dealer Count: {self.dealer_count}, {self.player_name} Count: {self.player_count}")
                self.win()

    def show_drawn_cards(self):
        print(self.drawn_cards)
