from queue import LifoQueue
from random import shuffle

class deck:
    """
    A class to represent the deck of cards

    ...
    Attributes
    ---------
    count : int
        Number of cards in the deck
    cards : LifoQueue[card]
        Queue representing the order of cards in the deck
    
    Methods
    ---------
    deal(hand):
        Deals one card off the top of the deck into the player's hand
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the deck object.

        """
        self.count = 52
        self.cards = LifoQueue(maxsize=0)
        templist = []
        
        #Construct the deck from each combination of suits and values
        #We use a list at first to access the shuffle method then it is turned into a LifoQueue
        for _ in range(0,52):
            suits = ['Hearts', 'Diamonds', 'Spades', 'Clubs']
            values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
            for suit in suits:
                for value in values:
                    templist.append(card(value, suit))
        
        shuffle(templist)
        
        for item in templist:
            self.cards.put(item)
                    
    def deal(self, hand):
        """
        Deals one card off the top of the deck into the player's hand

        Parameters
        ----------
            hand : hand
                The player's hand of cards
        
        Returns:
            The hand with card added
        """
        hand.add(self.cards.get())
        self.count -= 1
        return hand
     
class hand():
    """
    A class to represent the player's hand

    ...
    Attributes
    ---------
    cards : list[card]
        The player's hand represented as a list of cards
    value : int
        Value of the cards in the player's hand
    
    Methods
    ---------
    add(card):
        Adds a card to the player's hand
    SetValue():
        Calculates the value of the player's hand
    stringHand():
        Returns a list of strings representing the cards in the player's hand
    """
    def __init__(self):
        """
        Constructs all the necessary attributes for the hand object.

        """
        self.cards = []
        self.value = 0
        
    def add(self, card):
        """
        Adds a card to the player's hand

        Parameters
        ----------
            card : card
                The card object to be added to the hand
        """
        self.cards.append(card)
        self.setValue()
    
    def setValue(self):
        """
        Calculates the value of the player's hand

        """
        self.value=0
        aceCount = 0
        for card in self.cards:
            if card.value not in ['Jack', 'Queen', 'King', 'Ace']:
                self.value += int(card.value)
            elif card.value in ['Jack', 'Queen', 'King']:
                self.value += 10
            else:
                self.value += 11
                aceCount += 1
        for _ in range (0,aceCount):
            if self.value > 21:
                self.value -= 10
    
    def stringHand(self):
        """
        Returns a list of string representations of the cards in the player's hand

        Returns:
            A list of string representations of the cards in the player's hand

        """
        toReturn = []
        for c in self.cards:
            toReturn.append(c.cardString())
        return toReturn
    
class card():
    """
    A class to represent a card

    ...
    Attributes
    ---------
    value : int
        The value of the card 2-11
    suit : string
        The suit of the card 
    
    Methods
    ---------
    cardString():
        Returns a string representation of the card, i.e. "2 of Clubs"
    """
    def __init__(self,value, suit):
        """
        Constructs all the necessary attributes for the card object.

        """
        self.value = value
        self.suit = suit
    
    def cardString(self):
        """
        Returns a string representation of the card, i.e. "2 of Clubs"

        Returns:
            String representation of the card

        """
        return self.value+" of "+ self.suit

def printDetails(hand, dealer=False):
    """
    Prints a string representation of the player's hand
    
    Parameters
    ----------
    hand : hand
        The hand object to be printed
    dealer : bool
        True if the target player is the dealer, else false
    

    """
    player = 'Dealer\'s' if dealer else 'Your'
    
    toPrint = hand.stringHand()
    
    print(player + " hand contains: ")

    for s in toPrint:
        print(s)

    print(player + " hand's value is: " + str(hand.value))

import time

playingDeck = deck()

#Set minimum number of cards in the deck before shuffling
shuffleAt = 17

cont = 'y' 

while(cont == 'y'):
    print("\n-------------\n")
    playerHand = hand()
    dealerHand = hand()
    bust = False
    
    if playingDeck.count < shuffleAt:
        print("\nThe deck is being shuffled\n")
        #Instantiate new deck object, which will shuffle cards
        playingDeck = deck()
    
    for _ in range(0,2):
        #Deal two cards
        playerHand = playingDeck.deal(playerHand)
        dealerHand = playingDeck.deal(dealerHand)
    
    print("Dealer shows " + dealerHand.cards[1].cardString() + "\n")
    
    printDetails(playerHand)
    
    stand = input("Hit? Enter 'h' to hit or 's' to stand: \n")
    
    while(stand != 's'):
        print("\n")
        playerHand = playingDeck.deal(playerHand)
        printDetails(playerHand)
        bust = playerHand.value > 21
        
        if bust:
            print('You bust')
            stand = 's'
            time.sleep(1)
        else:
            stand = input("Hit? Enter 'h' to hit or 's' to stand: \n")
    
    print("\n------ \n")
    
    while(dealerHand.value < 17):
        dealerHand = playingDeck.deal(dealerHand)

    time.sleep(1)
    
    printDetails(dealerHand, dealer=True)
    
    print("\n------ \n")
    time.sleep(1)
    
    if bust:
        print("You have busted and lose")
    
    elif dealerHand.value > 21:
        print("Dealer busted! You win!")
    
    else:
        print("Dealer has "  + str(dealerHand.value) + " and you have " + str(playerHand.value))
        if dealerHand.value < playerHand.value:
            print("You win!")
        elif dealerHand.value > playerHand.value:
            print("You lose")
        else:
            print("You push")
            
    cont = input("Continue? y/n: \n")