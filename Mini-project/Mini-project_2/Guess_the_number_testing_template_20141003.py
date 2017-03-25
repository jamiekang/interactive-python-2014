# Testing template for "Guess the number"

###################################################
# Student should add code for "Guess the number" here
# helper function to start and restart the game    





# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

# initialize global variables
secret_number = 28
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
    print "Secret number:", secret_number

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
#new_game()

# always remember to check your completed program against the grading rubric







###################################################
# Start our test #1 - assume global variable secret_number
# is the the "secret number" - change name if necessary

#secret_number = 74  
#input_guess("50")
#input_guess("75")
#input_guess("62")
#input_guess("68")
#input_guess("71")
#input_guess("73")
#input_guess("74")

###################################################
# Output from test #1
#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#Guess was 50
#Number of remaining guesses is 6
#Higher!
#
#Guess was 75
#Number of remaining guesses is 5
#Lower!
#
#Guess was 62
#Number of remaining guesses is 4
#Higher!
#
#Guess was 68
#Number of remaining guesses is 3
#Higher!
#
#Guess was 71
#Number of remaining guesses is 2
#Higher!
#
#Guess was 73
#Number of remaining guesses is 1
#Higher!
#
#Guess was 74
#Number of remaining guesses is 0
#Correct!
#
#New game. Range is from 0 to 100
#Number of remaining guesses is 7

###################################################
# Start our test #2 - assume global variable secret_number
# is the the "secret number" - change name if necessary

#range1000()
#secret_number = 375    
#input_guess("500")
#input_guess("250")
#input_guess("375")

###################################################
# Output from test #2
#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#New game. Range is from 0 to 1000
#Number of remaining guesses is 10
#
#Guess was 500
#Number of remaining guesses is 9
#Lower!
#
#Guess was 250
#Number of remaining guesses is 8
#Higher!
#
#Guess was 375
#Number of remaining guesses is 7
#Correct!
#
#New game. Range is from 0 to 1000
#Number of remaining guesses is 10



###################################################
# Start our test #3 - assume global variable secret_number
# is the the "secret number" - change name if necessary

secret_number = 28 
input_guess("50")
input_guess("50")
input_guess("50")
input_guess("50")
input_guess("50")
input_guess("50")
input_guess("50")

###################################################
# Output from test #3
#New game. Range is from 0 to 100
#Number of remaining guesses is 7
#
#Guess was 50
#Number of remaining guesses is 6
#Lower!
#
#Guess was 50
#Number of remaining guesses is 5
#Lower!
#
#Guess was 50
#Number of remaining guesses is 4
#Lower!
#
#Guess was 50
#Number of remaining guesses is 3
#Lower!
#
#Guess was 50
#Number of remaining guesses is 2
#Lower!
#
#Guess was 50
#Number of remaining guesses is 1
#Lower!
#
#Guess was 50
#Number of remaining guesses is 0
#You ran out of guesses.  The number was 28
#
#New game. Range is from 0 to 100
#Number of remaining guesses is 7