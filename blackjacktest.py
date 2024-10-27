import random
from collections import Counter

class BlackjackShoe:
    def __init__(self, num_decks):
        self.num_decks = num_decks
        self.cards = self.create_shoe()
        self.shuffle_shoe()
        self.running_count = 0

    def create_shoe(self):
        single_deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        return single_deck * self.num_decks

    def shuffle_shoe(self):
        random.shuffle(self.cards)

    def burn_cards(self, num_burn):
        for _ in range(min(num_burn, len(self.cards))):
            self.draw_card()

    def draw_card(self):
        if not self.cards:
            raise ValueError("No cards left in the shoe to draw.")
        card = self.cards.pop(0)
        self.update_running_count(card)
        return card

    def update_running_count(self, card):
        if card == '2':
            self.running_count += 0.5
        elif card in ['3', '4', '6']:
            self.running_count += 1
        elif card == '5':
            self.running_count += 1.5
        elif card == '7':
            self.running_count += 1
        elif card == '8':
            self.running_count -= 0.5
        elif card == '9':
            self.running_count -= 1
        elif card in ['10', 'J', 'Q', 'K', 'A']:
            self.running_count -= 1

    def calculate_true_count(self):
        decks_remaining = len(self.cards) / 52
        if decks_remaining > 0:
            return self.running_count / decks_remaining
        return 0

class BlackjackGame:
    def __init__(self, num_decks, num_burn, initial_bankroll, base_bet):
        self.num_decks = num_decks
        self.num_burn = num_burn
        self.initial_bankroll = initial_bankroll
        self.base_bet = base_bet
        self.bankroll = initial_bankroll
        self.reset_game()

    def reset_game(self):
        self.shoe = BlackjackShoe(self.num_decks)
        self.shoe.burn_cards(self.num_burn)
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def hand_value(self, hand):
        total_value = 0
        aces = 0
        for card in hand:
            if card in ['10', 'J', 'Q', 'K']:
                total_value += 10
            elif card == 'A':
                aces += 1
                total_value += 11
            else:
                total_value += int(card)
        while total_value > 21 and aces:
            total_value -= 10
            aces -= 1
        return total_value

    def calculate_bet(self):
        true_count = self.shoe.calculate_true_count()
        if true_count < 1:
            return self.base_bet
        elif true_count == 1:
            return self.base_bet * 2
        elif true_count == 2:
            return self.base_bet * 3
        elif true_count >= 3:
            return self.base_bet * 4
        return self.base_bet

    def advanced_strategy(self, player_hand, dealer_card):
        player_total = self.hand_value(player_hand)
        dealer_value = 10 if dealer_card in ['10', 'J', 'Q', 'K'] else (11 if dealer_card == 'A' else int(dealer_card))
        true_count = self.shoe.calculate_true_count()

        if player_total >= 17:
            return "stand"
        elif player_total == 16 and dealer_value >= 7:
            if true_count >= 0:
                return "stand"
            return "hit"
        elif player_total == 15 and dealer_value == 10:
            if true_count >= 4:
                return "stand"
            return "hit"
        elif player_total == 13 and dealer_value == 2:
            if true_count >= 1:
                return "stand"
            return "hit"
        elif player_total == 12 and dealer_value in [4, 5, 6]:
            return "stand"
        elif player_total == 10 and dealer_value < 10 and true_count >= 4:
            return "double"
        elif player_total == 9 and dealer_value in [3, 4, 5, 6] and true_count >= 1:
            return "double"
        elif player_total <= 11:
            return "hit"
        else:
            return "hit"

    def insurance_decision(self):
        true_count = self.shoe.calculate_true_count()
        return true_count >= 3

    def late_surrender_decision(self, player_hand, dealer_card):
        player_total = self.hand_value(player_hand)
        true_count = self.shoe.calculate_true_count()

        if player_total == 16 and dealer_card in ['9', '10', 'A'] and true_count < 0:
            return True
        elif player_total == 15 and dealer_card == '10' and true_count < 0:
            return True
        return False

    def determine_outcome(self, player_hand, dealer_hand, bet):
        player_total = self.hand_value(player_hand)
        dealer_total = self.hand_value(dealer_hand)

        if player_total > 21:
            self.bankroll -= bet
            self.losses += 1
        elif dealer_total > 21 or player_total > dealer_total:
            self.bankroll += bet
            self.wins += 1
        elif dealer_total > player_total:
            self.bankroll -= bet
            self.losses += 1
        else:
            self.ties += 1

    def play_round(self):
        if len(self.shoe.cards) < 4:
            return False

        player_hand = [self.shoe.draw_card(), self.shoe.draw_card()]
        dealer_hand = [self.shoe.draw_card(), self.shoe.draw_card()]
        dealer_card = dealer_hand[0]
        bet = self.calculate_bet()

        if dealer_card == 'A' and self.insurance_decision():
            bet *= 1.5

        if self.late_surrender_decision(player_hand, dealer_card):
            self.bankroll -= bet / 2
            self.losses += 0.5
            return True

        while True:
            action = self.advanced_strategy(player_hand, dealer_card)
            if action == "hit":
                if len(self.shoe.cards) < 1:
                    return False
                player_hand.append(self.shoe.draw_card())
                if self.hand_value(player_hand) > 21:
                    break
            elif action == "double":
                if len(self.shoe.cards) < 1:
                    return False
                bet *= 2
                player_hand.append(self.shoe.draw_card())
                break
            else:
                break

        while self.hand_value(dealer_hand) < 17:
            if len(self.shoe.cards) < 1:
                return False
            dealer_hand.append(self.shoe.draw_card())

        self.determine_outcome(player_hand, dealer_hand, bet)
        return True

    def play_full_shoe(self):
        while len(self.shoe.cards) > 52 * 0.2:
            if not self.play_round():
                break

    def simulate_games(self, num_simulations):
        total_wins, total_losses, total_ties = 0, 0, 0

        for _ in range(num_simulations):
            self.reset_game()
            self.play_full_shoe()
            total_wins += self.wins
            total_losses += self.losses
            total_ties += self.ties
            print(f"Simulation results: Wins: {self.wins}, Losses: {self.losses}, Ties: {self.ties}, Current Bankroll: ${self.bankroll:.2f}")

        print("\nCumulative Results after all simulations:")
        print(f"Total Wins: {total_wins}")
        print(f"Total Losses: {total_losses}")
        print(f"Total Ties: {total_ties}")
        print(f"Final Bankroll: ${self.bankroll:.2f}")


num_decks = int(input("Enter the number of decks (1-2 for best advantage): "))
num_burn = int(input("Enter the number of cards to burn: "))
initial_bankroll = float(input("Enter the initial bankroll amount: "))
base_bet = float(input("Enter the base bet size: "))
num_simulations = int(input("Enter the number of simulations to run: "))

game = BlackjackGame(num_decks, num_burn, initial_bankroll, base_bet)
game.simulate_games(num_simulations)
