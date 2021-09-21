# Black Jack Using OOP
from random import shuffle
from random import choice

# Function to make a deck of cards (list) and a dict that maps the list to their values
def makeDeck():
	suits = ['H','S','C','D']
	numbered_cards = list(i for i in range(2, 11))
	face_cards = ['J', 'Q', 'K', 'A']
	cards = []
	card_values = {}
	for i in suits:
		for j in numbered_cards:
			cards.append(str(j) + '-' + i)
		for k in face_cards:
			cards.append(k + '-' + i)

	for i in cards:
		try:
			if i[0] == 'A':
				card_values[i] = 11
			elif int(i[0]) == 1:
				card_values[i] = 10
			else:
				card_values[i] = int(i[0])
		except:
			card_values[i] = 10

	return cards, card_values

Deck, DeckValues = makeDeck()

# Create some dealer names
dealers = ['Patrick', 'Vanessa', 'Bjorn', 'Sara', 'Jamal', 'Alissa']

# Function to print a bold message (Bust, Black-Jack, out of funds)
def bold_message(message):
	print('')
	print('######################################################')
	print('#                                                    #')
	print('              %s' %message)
	print('#                                                    #')
	print('######################################################')
	print('')

# Class for person (player or dealer)
class Person(object):

	def initial_deal(self, initial_cards):
		for i in initial_cards:
			self.hand.append(i)

	def total(self):
		total = 0
		for i in self.hand:
			total += DeckValues[i]
		return total

	def hit(self, hit_card):
		self.hand.append(hit_card)
	
	def purge_hand(self):
		self.hand = []

# Class for the player, inherits from class Person
class Player(Person):

	def __init__(self, name, bankRoll, hand=[]):
		Person.__init__(self)
		self.name = name
		self.bankRoll = bankRoll
		self.hand = hand

	def bank_roll_update(self):
		print('')
		print('Your new bank is %s' %self.bankRoll)
		print('')

	def status(self):
		print('')
		print('Your current hand: %s' %self.hand)
		print('Your current total: %s' %self.total())
		print('')
	
	def bet(self, amount):
		self.bankRoll -= amount

	def add_bank(self, amount):
		self.bankRoll += amount

	def has_ace(self):
		aces = False
		for i in self.hand:
			if i[0] == 'A':
				aces = True
		return aces

	def count_aces(self):
		count = 0
		for i in self.hand:
			if i[0] == 'A':
				count += 1
		return count

	def total(self):
		total = 0
		for i in self.hand:
			total += DeckValues[i]
		# Check if hand has ace(s)
		if total > 21 and self.has_ace():
			ace_count = self.count_aces()
			# Loop to count 1 ace as 1 instead of 11 at a time
			while total > 21 and ace_count > 0:
				total = total - 10
				ace_count -= 1
		return total

# Class for the dealer, inherits from class Person
class Dealer(Person):

	def __init__(self, name, hand=[]):
		Person.__init__(self)
		self.name = name
		self.hand = hand

	def show_open(self):
		print('')
		print('Dealer hand: %s' %[self.hand[0],"?"])
		print('')

	def turn_over(self):
		print('')
		print('Dealer hand revealed: %s' %[self.hand[0], self.hand[1]])
		print('Dealer total is %s' %self.total())
		print('')

	def status(self):
		print('')
		print('Dealer current hand: %s' %self.hand)
		print('Dealer current total: %s' %self.total())
		print('')

# Class for the chute of cards
class Chute(object):

	def __init__(self, num_decks):
		self.num_decks = num_decks
		self.cards = num_decks * Deck

	def shuffle_cards(self):
		shuffle(self.cards)

	def initial_deal(self):
		return [self.cards.pop(), self.cards.pop()]

	def hit(self):
		return self.cards.pop()

## MAIN FUNCTION ##
def main(list_Deck, dict_DeckValues):

	## Game setup ##
	print('Welcome to Black Jack!')
	dealer_name = choice(dealers)
	dealer = Dealer(dealer_name)
	print('Your dealer today is: %s' %dealer.name)
	print('')
	player_name = input('Please enter your name: ')

	## This loop to ensure buy-in amount is an integer
	while True:
		try:
			player_bank_roll = int(input('Please enter your buy-in amount: '))
		except:
			print('Try again - please enter an integer for your buy-in amount: ')
			continue
		else:
			player = Player(player_name, player_bank_roll)
			break

	# Welcome message
	print('')
	print('Welcome %s! \nYour current bankroll is: %s' %(player.name, player.bankRoll))
	print('')

	# This loop to ensure number of decks is an integer
	while True:
		try:
			decks_input = int(input('Enter number of decks you would like to play with: '))
		except:
			print('Try again - please enter an integer for the number of decks you want to play with: ')
			continue
		else:
			chute = Chute(decks_input)
			break

	# Message to confirm number of decks in play
	print('We are playing with %s decks' %decks_input)

	# Shuffle the chute
	chute.shuffle_cards()
	print('')

	## Game play ##

	# Check if there are enough cards in the chute and that player still have cash
	while len(chute.cards) >= 15 and player.bankRoll > 0:
		# Player and dealer hand purge. These can go here or at the end of the current game
		player.purge_hand()
		dealer.purge_hand()

		# Get player bet
		# This loop to make sure bet is an integer
		while True:
			try:
				bet = int(input('Place your bet: '))
				# This "if" to make sure bet is <= bankRoll
				if bet > player.bankRoll:
					print('You do not have enough cash for that bet. Try again')
					continue
			except:
				print('Try again - please enter an integer for your bet: ')
				continue
			else:
				print('%s bet placed!' %bet)
				player.bet(bet)
				print('Your updated bankroll is: %s' %player.bankRoll)
				print('')
				break

		# Deal initial cards to player and show status #
		player.initial_deal(chute.initial_deal())
		player.status()

		# Check for blackjack
		if player.total() == 21:
			bold_message('BLACKJACK')
			player.add_bank(2*bet)
			player.bank_roll_update()
			# print('Your new bankroll is: %s' %player.bankRoll)
			# print('')
		else:
			print('')
			# Deal cards to dealer and show hand #
			dealer.initial_deal(chute.initial_deal())
			dealer.show_open()
			print('')

			# This loop checks for bust
			while player.total() < 21:
				# This loop to make sure player enters a string and that it is either 'h' for hit or s for 's'
				try:
					move = str(input('Enter \'h\' for hit or \'s\' for stay: '))
					# This 'if' to make sure an 'h' or an 's' was entered
					if move.lower() != 'h' and move.lower() != 's':
						print('Invalid choice. Please Enter \'h\' for hit or \'s\' for stay')
						continue
				# Handles non string inputs
				except:
					print('Invalid choice. Please Enter \'h\' for hit or \'s\' for stay')
				else:					
					print('You chose to stay') if move.lower() == 's' else print('You chose to hit')
					print('')

				# Hit scenario
				if move == 'h':
					player.hit(chute.hit())
					player.status()
					# Check for blackjack and pop out of parent while loop if so
					if player.total() == 21:
						bold_message('BLACKJACK')
						player.add_bank(2*bet)
						player.bank_roll_update()
						break
					elif player.total() > 21:
						bold_message('BUST: ' + str(player.total()))
						player.bank_roll_update()

				# Stay scenario
				else:
					# Reveal the dealers hidden card
					dealer.turn_over()
					while True:
						# Check for dealer blackjack
						if dealer.total() == 21:
							bold_message('DEALER HAS BLACKJACK')
							player.bank_roll_update()
							break
						# Check for dealer win
						elif dealer.total() > player.total() and dealer.total() < 21:
							bold_message('DEALER WINS: %s' %dealer.total())
							player.bank_roll_update()
							break
						# Check for tie (push)
						elif dealer.total() == player.total():
							bold_message('PUSH')
							player.add_bank(bet)
							player.bank_roll_update()
							break
						# Check for dealer bust
						elif dealer.total() > 21:
							bold_message('DEALER BUSTED')
							player.add_bank(2*bet)
							player.bank_roll_update()
							break
						# Else dealer takes another hit
						else:
							dealer.hit(chute.hit())
							dealer.status()
					break

	if len(chute.cards) <= 15:
		bold_message('Out of cards in the chute! Please replay to continue...')
	elif player.bankRoll == 0:
		bold_message('Out of money. Replay to re-buy-in')

# Run the main function
main(Deck, DeckValues)