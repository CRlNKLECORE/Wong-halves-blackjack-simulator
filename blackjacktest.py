import random

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
		self.running_count = 0  # Reset running count on shuffle

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

	def calculate_bet(self):
		true_count = self.shoe.calculate_true_count()
		
		if true_count < 1:
			return self.base_bet
		elif 1 <= true_count < 2:
			return self.base_bet * 2
		elif 2 <= true_count < 3:
			return self.base_bet * 3
		elif 3 <= true_count < 4:
			return self.base_bet * 4
		elif 4 <= true_count < 5:
			return self.base_bet * 5
		elif 5 <= true_count < 6:
			return self.base_bet * 6
		elif 6 <= true_count < 7:
			return self.base_bet * 7
		elif 7 <= true_count < 8:
			return self.base_bet * 8
		elif 8 <= true_count < 9:
			return self.base_bet * 9
		elif 9 <= true_count < 10:
			return self.base_bet * 10
		elif 10 <= true_count < 11:
			return self.base_bet * 11
		elif 11 <= true_count < 12:
			return self.base_bet * 12
		elif 12 <= true_count < 13:
			return self.base_bet * 13
		elif 13 <= true_count < 14:
			return self.base_bet * 14
		elif 14 <= true_count < 15:
			return self.base_bet * 15
		elif 15 <= true_count < 16:
			return self.base_bet * 16
		elif 16 <= true_count < 17:
			return self.base_bet * 17
		elif 17 <= true_count < 18:
			return self.base_bet * 18
		elif 18 <= true_count < 19:
			return self.base_bet * 19
		elif 19 <= true_count < 20:
			return self.base_bet * 20
		elif 20 <= true_count < 21:
			return self.base_bet * 21
		elif 21 <= true_count < 22:
			return self.base_bet * 22
		elif 22 <= true_count < 23:
			return self.base_bet * 23
		elif 23 <= true_count < 24:
			return self.base_bet * 24
		elif 24 <= true_count < 25:
			return self.base_bet * 25
		elif true_count >= 25:
			return self.base_bet * 26
		
		return self.base_bet

	def play_round(self):
		if len(self.shoe.cards) < 4:
			return False

		player_hand = [self.shoe.draw_card(), self.shoe.draw_card()]
		dealer_hand = [self.shoe.draw_card(), self.shoe.draw_card()]
		dealer_card = dealer_hand[0]
		bet = self.calculate_bet()

		while self.hand_value(player_hand) < 17:
			if len(self.shoe.cards) < 1:
				return False
			player_hand.append(self.shoe.draw_card())
			if self.hand_value(player_hand) > 21:
				break

		while self.hand_value(dealer_hand) < 17:
			if len(self.shoe.cards) < 1:
				return False
			dealer_hand.append(self.shoe.draw_card())

		self.determine_outcome(player_hand, dealer_hand, bet)
		return True

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
