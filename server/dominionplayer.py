# Dominion player class to create and manage player objects
from dominioncards import *
from dominiondeck import *
import types

class Player(object):

	def __init__(self, roster):
		self.player = self
		self.playerHand = []
		self.playerName = ''
		self.playerDeck = []
		self.playerPlay = []
		self.playerTurnActions = 0
		self.playerTurnBuys = 0
		self.playerTurnTreasure = 0
		self.playerRoom = ''
		self.deck = ''
		self.playerDiscard = []
		self.roster = roster
		self.playerHasDuration = False
		self.playerSetAside = []
		self.playerTreasurePlayed = False
		self.game = ''		
		self.reactionImmunity = False
		self.durationImmunity = False
		self.totalVictory = 0
		self.playerConn = ''
		self.playerTurn = False

	def send_data (self, client, data):
		message = str(data)
		return client.send(message)

	def recv_data (self, client, length):
	        data = client.recv(length)
        	if not data: return data
        	return data

	def drawToPlayer(self, hand):
		if hand == 0:
			for i in range(3):
				self.playerDeck.append(EstateCard)
			for i in range(7):
				self.playerDeck.append(CopperCard)
			random.shuffle(self.playerDeck)
		elif hand > 0:
			pass

	def drawHand(self):
		for i in range(5):
			if len(self.playerDeck) > 0:
				self.playerHand.append(self.playerDeck[0])
				del self.playerDeck[0]
			else:
				self.playerDiscardToDeck()
				self.playerHand.append(self.playerDeck[0])
				del self.playerDeck[0]

	def drawOneCard(self):
		if len(self.playerDeck) == 0:
			self.playerDiscardToDeck()
		else:
			self.playerHand.append(self.playerDeck[0])
			del self.playerDeck[0]

	def gainCard(self, cost, number, location, type):
		self.cost = cost
		self.number = number
		self.location = location
		self.type = type
		if self.location == 'discard':
			self.location = self.playerDiscard
		elif self.location == 'hand':
			self.location = self.playerHand
		elif self.location == 'deck':
			self.location = self.playerDeck
		choices = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		nonkingdom = ['o', 'p', 'd', 'e', 'u', 'l', 'g', 's', 'c']
		kingdom = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
		while True:
			for i in range(self.number):
				if self.type == 'treasure':
					choice = raw_input("    Please select a Treasure card that costs up to $" + str(self.cost) + ": ")
					if choice.lower() not in ['l', 'g', 's', 'c']:
						print "    Invalid selection, please choose a Treasure card!"
				elif self.type == 'kingdom':
					choice = raw_input("    Please select a Kingdom card that costs up to $" + str(self.cost) + ": ")
					if choice.lower() not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
						print "    Invalid selection, please choose a Kingdom card!"
				elif self.type == 'victory':
					choice = raw_input("    Please select a Victory card that costs up to $" + str(self.cost) + ": ")
					if choice.lower() not in ['o', 'p', 'd', 'e']:
						print "    Invalid Selection, please choose a Victory card!"
				elif self.type == 'any':
					choice = raw_input("    Please select a card that costs up to $" + str(self.cost) + ": ")
					if choice.lower() not in choices:
						print "    Invalid selection, please choose another card!"
				if choice.lower() in nonkingdom:
					if choice.lower() == 'o' or choice.lower == 'l':
						print "    Invalid selection, please choose another card!"
					else:
						p = self.deck.provinceCards
						d = self.deck.duchyCards
						e = self.deck.estateCards
						g = self.deck.goldCards
						s = self.deck.silverCards
						c = self.deck.copperCards
						u = self.deck.curseCards
						choice = eval(choice.lower())
						if choice[0].cost > self.cost:
							print "    Invalid selection, please choose another card!"
						else:
							self.location.append(choice[0])
							del choice[0]
							break
				elif choice.lower() in kingdom:
					x = 'card' + choice.lower()
					if self.deck.kingdomCards[x][0].cost > cost:
						print "    Invalid selection, please choose another card!"
					else:
						self.location.append(self.deck.kingdomCards[x][0])
						del self.deck.kingdomCards[x][0]
						break
			break

	def playTurn(self):
		self.checkPlayerDeck()
		self.checkDurationEffects()
		self.checkSetAside()
		if self.playerTurnActions == 1 and self.playerTurnBuys == 1 and self.playerTurnTreasure == 0:
			self.actionPhase()
		else:
			self.playerTurnActions = 1
			self.playerTurnBuys = 1
			self.playerTurnTreasure = 0
			self.playerTreasurePlayed = False
			self.actionPhase()
		return

	def actionPhase(self):
		actionPhaseCount = 1
		while True:
			if self.playerTurnActions == 0 or self.playerTreasurePlayed == True:
				self.buyPhase()
			else:
				self.printPlayerHand(self.roster)
				self.send_data(self.playerConn, "\n  What would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead? \n")
				while True:
					response = str(self.recv_data(self.playerConn, 1024))
					if response not in ['p', 'b', 'a', 'r']:
						self.send_data(self.playerConn, "Sorry, that is not an available choice.\n")
					elif response == 'p':
						self.playCard()
						actionPhaseCount += 1
						continue
					elif response == 'b':
						self.send_data(self.playerConn, "Which card would you like to buy?\n")
						while True:
							choice = str(self.recv_data(self.playerConn, 1024))
							if choice.lower() not in ['o', 'p', 'd', 'e', 'u', 'g', 's', 'c', 't', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
								self.send_data(self.playerConn,"Invalid selection!\n"
							elif choice.lower() in ['o', 'l', 't']:
									continue
							elif choice.lower() in ['p', 'd', 'e', 'u', 'l', 'g', 's', 'c', 'o']:
								p = self.deck.provinceCards
								d = self.deck.duchyCards
								e = self.deck.estateCards
								g = self.deck.goldCards
								s = self.deck.silverCards
								c = self.deck.copperCards
								u = self.deck.curseCards
								i = eval(i.lower())
								if i[0].cost > self.playerTurnTreasure:
									self.send_data(self.playerConn, " You do not have enough to buy this.\n" )
									continue
								else:
									self.playerPlay.append(i[0])
									self.playerTurnTreasure -= i[0].cost
									del i[0]
									self.playerTurnBuys -= 1
									break
							elif int(choice) in range(10):
								x = 'card' + i
								if self.deck.kingdomCards[x][0].cost > self.playerTurnTreasure:
									self.send_data(self.playerConn, " You do not have enough to buy this.\n")
									continue
							else:
								self.playerPlay.append(self.deck.kingdomCards[x][0])
								self.playerTurnTreasure -= self.deck.kingdomCards[x][0].cost
								del self.deck.kingdomCards[x][0]
								self.playerTurnBuys -= 1
								break
							break
						self.buyPhase()
						break
					elif response.lower() == 'a':
						self.cleanUpPhase()
					elif response.lower() == 'r':
						self.send_data(self.playerConn, " Which card would you like to read: (n)umber?\n")
						self.deck.readCard(str(self.recv_data(self.playerConn, 1024)))
						continue
			return

	def playCard(self):
		while True:
			self.send_data(self.playerConn, "Which card would you like to play: (n)umber?\n")
			i = str(self.recv_data(self.playerConn, 1024))
			try:
				i = int(i)
			except:
				continue
			if i > len(self.playerHand):
				continue
			elif self.playerHand[i - 1].treasure == True:
				self.playerPlay.append(self.playerHand[i - 1])
				self.playerTurnTreasure += self.playerHand[i - 1].value
				del self.playerHand[i - 1]
				self.playerTurnActions = 0
				self.playerTreasurePlayed = True
				self.buyPhase()
				break
			elif self.playerHand[i - 1].action == True:
				if self.playerTurnActions <= 0:
					self.send_data(self.playerConn, "You have no Actions left this turn, please (b)uy or p(a)ss.\n")
					self.buyPhase()
				else:
					self.playerPlay.append(self.playerHand[i - 1])
					del self.playerHand[i - 1]
					self.playerTurnActions -= 1
					self.playerPlay[-1].playCard(self.player, self.roster, self.deck)
					break
			elif self.playerHand[i - 1].victory == True and self.playerHand[i - 1].action == False:
				self.send_data(self.playerConn, "Invalid choice, you cannot play this card.\n")
		return

	def buyPhase(self):
		if self.playerTurnBuys == 0:
			self.cleanUpPhase()
		else:
			while True:
				self.printPlayerHand()
				self.send_data(self.playerConn("\nWhat would you like to do: (P)lay, (B)uy, P(a)ss, (R)ead?\n"))
				choice = str(self.recv_data(self.playerConn, 1024))
				if choice.lower() not in ['p', 'b', 'a', 'r']:
					continue
				elif choice.lower() == 'p':
					while True:
						self.send_data(self.playerConn("Which card would you like to play: (n)umber?\n")
						i = self.recv_data(self.playerConn, 2014)
						try:
							i = int(i)
						except:
							continue
						if i > len(self.playerHand):
							continue
						elif self.playerHand[i - 1].treasure != True and self.playerHand[i - 1].action != False or self.playerHand[i - 1].treasure != True:
							self.send_data(self.playerConn, " You are in the buy phase, please play a Treasure.\n"))
							continue
						else:
							self.playerPlay.append(self.playerHand[i - 1])
							self.playerTurnTreasure += self.playerHand[i - 1].value
							del self.playerHand[i - 1]
							break
				elif actionType.lower() == 'b':
					while True:
						self.send_data(self.playerConn, "Which card would you like to buy?\n")
						i = self.recv_data(self.playerConn, 2014)
						if i.lower() not in ['o', 'p', 'd', 'e', 'u', 'g', 's', 'c', 't', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
							self.send_data(self.playerConn,  " Invalid selection!\n")
						elif i.lower() in ['o', 'l', 't']:
							continue
						elif i.lower() in ['p', 'd', 'e', 'u', 'l', 'g', 's', 'c', 'o']:
							p = self.deck.provinceCards
							d = self.deck.duchyCards
							e = self.deck.estateCards
							g = self.deck.goldCards
							s = self.deck.silverCards
							c = self.deck.copperCards
							u = self.deck.curseCards	
							i = eval(i.lower())
							if i[0].cost > self.playerTurnTreasure:
								self.send_data(self.playerConn, " You do not have enough to buy this.\n")
								continue
							else:
								self.playerPlay.append(i[0])
								self.playerTurnTreasure -= i[0].cost
								del i[0]
								self.playerTurnBuys -= 1
								break
						elif int(i) in range(10):
							x = 'card' + i
							if self.deck.kingdomCards[x][0].cost > self.playerTurnTreasure:
								self.send_data(self.playerconn, " You do not have enough to buy this.\n")
								continue
							else:
								self.playerPlay.append(self.deck.kingdomCards[x][0])
								self.playerTurnTreasure -= self.deck.kingdomCards[x][0].cost
								del self.deck.kingdomCards[x][0]
								self.playerTurnBuys -= 1
								break
						break
					break
				elif actionType.lower() == 'a':
					self.cleanUpPhase()
				elif actionType.lower() == 'r':
					self.send_data(self.playerConn, "Which card would you like to read: (n)umber?\n")
					self.deck.readCard(self.recv_data(self.playerConn, 1024))
					break
			if self.playerTurnBuys < 1:
				self.cleanUpPhase()
			else:
				self.buyPhase()
		return

	def cleanUpPhase(self):
		self.playerTurnActions = 1
		self.playerTurnBuys = 1
		self.playerTurnTreasure = 0
		self.playerTreasurePlayed = False
		x = len(self.playerPlay)
		y = len(self.playerHand)
		while x == len(self.playerPlay) and x > 0:
			self.playerDiscard.append(self.playerPlay[0])
			del self.playerPlay[0]
			x -= 1
		while y == len(self.playerHand) and y > 0:
			self.playerDiscard.append(self.playerHand[0])
			del self.playerHand[0]
			y -= 1
		self.drawHand()
		self.checkWin()
		return
#		self.passTurn()
		
	def passTurn(self):
		self.game.playerTurn += 1
		self.game.playLoop()

	def checkDurationEffects(self):
		if self.playerHasDuration == True:
			pass
		else:
			return

	def checkSetAside(self):
		if len(self.playerSetAside) > 0:
			pass
		else:
			return

	def checkReactions(self, type):
		self.type = type
		if self.type == 'attack':
			for each in self.roster:
				if each != self:
					if any(i.reaction == True for i in each.playerHand):
						each.playerHand[i].reactCard('attack')
					else:
						pass
		elif self.type == 'gain':
			for each in self.roster:
				if any(i.reaction == True for i in each.playerHand):
					each.playerHand[i].reactCard('gain')


	def checkPlayerDeck(self):
		if len(self.playerDeck) == 0:
			self.playerDiscardToDeck()
		else:
			return

	def playerDiscardToDeck(self):
		x = len(self.playerDiscard)
		while x == len(self.playerDiscard) and x > 0:
			self.playerDeck.append(self.playerDiscard[0])
			del self.playerDiscard[0]
			x -= 1
		random.shuffle(self.playerDeck)

	def playerDeckToDiscard(self):
		x = len(self.playerDeck)
		while x == len(self.playerDeck) and x > 0:
			self.playerDiscard.append(self.playerDeck[0])
			del self.playerDeck[0]
			x -= 1
	
	def printPlayerHand(self, roster):
		self.deck.printDeckCards(self.roster)
		self.printPlayerCount(self.roster)
		self.printTurnCount(self.roster)
		for user in roster:
			user.playerConn.send("\n  Current Hand (" + user.playerName + "):\n ")
			for card in user.playerHand:
				user.playerConn.send(" " + card.cardColor + card.cardName + " \033[0m",)
			user.playerConn.send("\n")

	def printPlayerReveal(self, roster):
		for user in roster:
			user.playerConn.send("\n Current hand (" + user.playerName + "):\n")
			for card in user.playerHand:
				user.playerConn.send(card.cardColor + card.cardName + "\033[0m",)
			user.playerConn.send("\n")

	def printPlayerCount(self, roster):
		for user in roster:
			user.playerConn.send("\n\n  Deck [",)
			for i in range(len(user.playerDeck)):
				user.playerConn.send("|",)
			user.playerConn.send("] -- Discard [",)
			for i in range(len(user.playerDiscard)):
				user.playerConn.send("|",)
			user.playerConn.send("]\n\n")

	def printTurnCount(self, roster):
		for user in roster:
			user.playerConn.send("  Actions: " + str(user.playerTurnActions) + "    Buys ($" + str(user.playerTurnTreasure) + "): " + str(user.playerTurnBuys) + "\n")

	def checkWin(self):
		self.zeroTally = 0
		if len(self.deck.duchyCards) == 0: self.zeroTally += 1
		if len(self.deck.estateCards) == 0: self.zeroTally += 1
		if len(self.deck.curseCards) == 0: self.zeroTally += 1
		if len(self.deck.goldCards) == 0: self.zeroTally += 1
		if len(self.deck.silverCards) == 0: self.zeroTally += 1
		if len(self.deck.copperCards) == 0: self.zeroTally += 1
		for i in range(10):
			if len(self.deck.kingdomCards['card' + str(i)]) == 0:
				self.zeroTally += 1
			else:
				pass
		if len(self.deck.provinceCards) == 0:
			self.endGame()
		elif self.zeroTally == 3:
			self.endGame()
		else:
			pass

	def endGame(self):
		for each in self.roster:
			self.send_data(each.playerConn, "GAME OVER! The scores are: ")
		for each in self.roster:
			each.playerDeckToDiscard()
			for i in len(each.playerHand):
				each.playerDiscard.append(each.playerHand[0])
				del each.playerHand[0]
			for i in each.playerDiscard:
				if i.cardName == 'Gardens': each.totalVictory += (1 * (len(each.playerDiscard) // 10))
				else: each.totalVictory += i.victoryPoints
			self.send_data(each.playerConn, "  " + each.playerName + ": " + str(each.totalVictory + "\n")