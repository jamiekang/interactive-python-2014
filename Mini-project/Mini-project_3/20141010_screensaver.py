# simple "screensaver" program.

# import modules
import simplegui
import random

# define global variables
message = "Python is Fun!"
position = [50, 50]
width = 500
height = 500
interval = 2000

# Handler for text box
def update(text):
    global message
    message = text

# Handler for timer
def tick():
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    position[0] = x
    position[1] = y

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
#def format(t):
#    pass
    
# define event handlers for buttons; "Start", "Stop", "Reset"


# define event handler for timer with 0.1 sec interval


# define draw handler
def draw(canvas):
    canvas.draw_text(message, position, 36, "Red")
    
# create frame
frame = simplegui.create_frame("Home", width, height)

# register event handlers
text = frame.add_input("Message:", update, 150)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# start frame
frame.start()
timer.start()

# Please remember to review the grading rubric

