# template for "Stopwatch: The Game"
# import modules
import simplegui

# define global variables
width = 300
height = 150
position = [100, 100]   # main stopwatch text
position_num = [width-70, height-100]   # x/y 

interval = 100  # 100ms = 0.1sec

timer_tick = 0  # running timer
num_trial = 0   # y
num_hit = 0     # x
is_running = False

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    t_sec = t / 10
    # get A
    n_min = t_sec / 60
    t_A = str(n_min)
    # get B
    n_sec = t_sec - (n_min * 60)
    n_B = n_sec / 10
    t_B = str(n_B)
    # get C
    n_C = n_sec % 10
    t_C = str(n_C)
    # get D
    n_D = (t % 10)
    t_D = str(n_D)
    return t_A + ":" + t_B + t_C + "." + t_D
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start_timer():
    global is_running
    timer.start()
    is_running = True

def stop_timer():
    global num_trial, num_hit, is_running
    timer.stop()
    if is_running:
        num_trial += 1
        if timer_tick % 10 == 0:
            num_hit += 1
    is_running = False

def reset_timer():
    global timer_tick, num_hit, num_trial, is_running
    stop_timer()
    timer_tick = 0
    num_hit = 0
    num_trial = 0
    is_running = False

# define event handler for timer with 0.1 sec interval
def tick():
    global timer_tick
    timer_tick += 1
    #print "timer: ", timer_tick

# define draw handler
def draw(canvas):
    canvas.draw_text(format(timer_tick), position, 50, "White")
    canvas.draw_text(str(num_hit)+"/"+str(num_trial), position_num, 36, "Red")

# create frame
frame = simplegui.create_frame("Stopwatch", width, height)

# register event handlers
frame.add_button("Start", start_timer, 200)
frame.add_button("Stop", stop_timer, 200)
frame.add_button("Reset", reset_timer, 200)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick)

# start frame
frame.start()

# Please remember to review the grading rubric
