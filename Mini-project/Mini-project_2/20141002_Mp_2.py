# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables
secret_number = 0
num_range = 100
max_try = 7

# helper function to start and restart the game
def new_game():
    # initialize global variables used in your code here
    global secret_number, max_try
    print "\nNew game. Range is from 0 to", num_range
    if num_range == 100:
        max_try = 7
    elif num_range == 1000:
        max_try = 10
    else:
        print "Error! Unexpected num_range"
        return

    print "Number of remaining guesses is", max_try    
    secret_number = random.randrange(0, num_range)

# define event handlers for control panel
def range100():
    global num_range, max_try
    num_range = 100
    max_try = 7
    # button that changes the range to [0,100) and starts a new game 
    new_game()    

def range1000():
    global num_range, max_try
    num_range = 1000    
    max_try = 10
    # button that changes the range to [0,1000) and starts a new game     
    new_game()

def input_guess(guess):
    global max_try
    # main game logic goes here 
    guess_number = int(guess)
    print "\nGuess was", guess_number
    #print "Secret number:", secret_number

    max_try = max_try - 1
    print "Number of remaining guesses is", max_try    

    if guess_number > secret_number:
        print "Lower!"
        check_max_try()
    elif guess_number < secret_number:
        print "Higher!"
        check_max_try()        
    else:
        print "Correct!"
        new_game()

def check_max_try():
    if max_try == 0:
        print "You ran out of guesses. The number was", secret_number
        # run a new game in current mode
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess the number", 200, 200)

# register event handlers for control elements and start frame
frame.add_button("Range: 0 - 100", range100, 200)
frame.add_button("Range: 0 - 1000", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)
frame.start()

# call new_game in default range100 mode 
new_game()

# always remember to check your completed program against the grading rubric
