# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# define global variabls
game_deck = []
player_hand = []
dealer_hand = []

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.card_list = []

    def __str__(self):
        ans = "Hand contains"
        for i in range(len(self.card_list)):
            ans += " "
            ans += self.card_list[i].get_suit()
            ans += self.card_list[i].get_rank()            
        return ans

    def add_card(self, card):
        self.card_list.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        hand_value = 0
        has_aces = False
        for i in range(len(self.card_list)):
            val = VALUES[self.card_list[i].get_rank()]            
            hand_value += val
            if val == 1:    # Ace found
                has_aces = True

        if has_aces:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value    # compute the value of the hand, see Blackjack video
        return hand_value

    def draw(self, canvas, pos):
        pass    # draw a hand on the canvas, use the draw method for cards
         
# define deck class 
class Deck: 
    def __init__(self):
        self.card_list = []
        for i in SUITS:
            for j in RANKS:
                self.card_list.append(Card(i, j))

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.card_list)

    def deal_card(self):
        return self.card_list.pop()    # deal a card object from the deck
    
    def __str__(self):
        ans = "Deck contains"
        for i in range(len(self.card_list)):
            ans += " "
            ans += self.card_list[i].get_suit()
            ans += self.card_list[i].get_rank()            
        return ans
        

#define event handlers for buttons
def deal():
    global outcome, in_play
    global game_deck, player_hand, dealer_hand

    # your code goes here
    game_deck = Deck()
    game_deck.shuffle()
    player_hand = Hand()
    dealer_hand = Hand()
 
    player_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())
    player_hand.add_card(game_deck.deal_card())
    dealer_hand.add_card(game_deck.deal_card())

    in_play = True
  
    print "Player: " + str(player_hand)
    print "Dealer: " + str(dealer_hand)
    print "score: " + str(score)
    print "P:" + str(player_hand.get_value()) + " vs. D:" + str(dealer_hand.get_value())
    print ""

def hit():
    global outcome, in_play, score
    # if the hand is in play, hit the player
    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(game_deck.deal_card())
            print "Player (after hit): " + str(player_hand)

    # if busted, assign a message to outcome, update in_play and score
        if player_hand.get_value() > 21:
            in_play = False
            print "You have busted. " + str(player_hand.get_value())        
            outcome = "You have busted."
            score -= 1

        print "score: " + str(score)            
        print "P:" + str(player_hand.get_value()) + " vs. D:" + str(dealer_hand.get_value())
        print ""
        return

def stand():
    global outcome, in_play, score
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play:
        if player_hand.get_value() > 21:
            in_play = False
            print "You have busted. " + str(player_hand.get_value())        
            outcome = "You have busted."
            score -= 1
            print "score: " + str(score)
            print "P:" + str(player_hand.get_value()) + " vs. D:" + str(dealer_hand.get_value())
            print ""
            return

    if in_play:
        while dealer_hand.get_value() < 17:
            dealer_hand.add_card(game_deck.deal_card())
            print "Dealer (while/after stand): " + str(dealer_hand)
            print "P:" + str(player_hand.get_value()) + " vs. D:" + str(dealer_hand.get_value())
        print ""

    # assign a message to outcome, update in_play and score
        if dealer_hand.get_value() > 21:
            in_play = False
            print "Dealer has busted. " + str(dealer_hand.get_value())        
            outcome = "Dealer has busted."
            score += 1
            print "score: " + str(score)
            print "P:" + str(player_hand.get_value()) + " vs. D:" + str(dealer_hand.get_value())
            print ""
            return

        if player_hand.get_value() > dealer_hand.get_value():
            in_play = False            
            print "You win."
            outcome = "You win."
            score += 1
            print "score: " + str(score)
            print "P:" + str(player_hand.get_value()) + " vs. D:" + str(dealer_hand.get_value())
            print ""
            return
        else:
            in_play = False
            print "Dealer win."            
            outcome = "Dealer win."
            score -= 1
            print "score: " + str(score)
            print "P:" + str(player_hand.get_value()) + " vs. D:" + str(dealer_hand.get_value())
            print ""
            return
        
# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric