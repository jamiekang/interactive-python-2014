# implementation of card game - Memory

import simplegui
import random

deck = []
exposed = []
state = 0
first_index = 0
second_index = 0
turn = 0

# helper function to initialize globals
def new_game():
    global deck, exposed, turn, state
    list1 = range(8)
    list2 = range(8)
    deck = list1 + list2
    random.shuffle(deck)
    exposed = [False] * 16
    turn = 0
    state = 0

# define event handlers
def mouseclick(pos):
    global click_pos, state, turn, first_index, second_index
    click_pos = list(pos)
    if click_pos[1] < 100:
        if click_pos[0] < 800:
            click_index = click_pos[0] // 50
            if exposed[click_index] == False:
                exposed[click_index] = True
                # add game state logic here
                if state == 0:
                    state = 1    
                    first_index = click_index
                elif state == 1:
                    state = 2
                    turn = turn + 1        
                    second_index = click_index
                else:
                    state = 1
                    if deck[first_index] != deck[second_index]:
                        exposed[first_index] = False
                        exposed[second_index] = False
                    first_index = click_index

# cards are logically 50x100 pixels in size    
def draw(canvas):
    label.set_text("Turns = " + str(turn))
    for index, elem in enumerate(deck):
        if exposed[index] == True:
            canvas.draw_text(str(elem), [13 + index * 50,75], 50, "White")
        else:
            canvas.draw_polygon([(index * 50,0), ((index+1) * 50,0), ((index+1) * 50,100), (index * 50,100)], 1,"Yellow","Green")

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric