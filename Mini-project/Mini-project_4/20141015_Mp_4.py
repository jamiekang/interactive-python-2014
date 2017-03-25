# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
paddle1_vel = 0
paddle2_vel = 0 
score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel_x = random.randrange(120/60, 240/60)  
    ball_vel_y = random.randrange(60/60, 180/60)

    if direction == RIGHT:  # RIGHT
        ball_vel = [ball_vel_x, - ball_vel_y]
    else:                   # LEFT
        ball_vel = [- ball_vel_x, - ball_vel_y]

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints

    paddle1_pos = [HALF_PAD_WIDTH, HEIGHT / 2]
    paddle2_pos = [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2]
    paddle1_vel = 0
    paddle2_vel = 0 
    score1 = 0
    score2 = 0

    direction = random.randrange(0,2)   # 0 or 1
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # check left/right gutter boundaries
    if (ball_pos[0] <= (PAD_WIDTH + BALL_RADIUS)):
        if (ball_pos[1] <= paddle1_pos[1]+HALF_PAD_HEIGHT) and (ball_pos[1] >= paddle1_pos[1]-HALF_PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0]   
            ball_vel[0] += 0.1 * ball_vel[0]
        else:
            score2 += 1
            spawn_ball(RIGHT)            
    elif (ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS)):
        if (ball_pos[1] <= paddle2_pos[1]+HALF_PAD_HEIGHT) and (ball_pos[1] >= paddle2_pos[1]-HALF_PAD_HEIGHT):
            ball_vel[0] = - ball_vel[0]            
            ball_vel[0] += 0.1 * ball_vel[0]            
        else:        
            score1 += 1
            spawn_ball(LEFT)

    # check verical boundaries
    if (ball_pos[1] <= BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    elif (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    if paddle1_pos[1] <= HALF_PAD_HEIGHT:
        paddle1_pos[1] = HALF_PAD_HEIGHT
    elif paddle1_pos[1] >= (HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos[1] = (HEIGHT - HALF_PAD_HEIGHT)

    paddle2_pos[1] += paddle2_vel
    if paddle2_pos[1] <= HALF_PAD_HEIGHT:
        paddle2_pos[1] = HALF_PAD_HEIGHT
    elif paddle2_pos[1] >= (HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos[1] = (HEIGHT - HALF_PAD_HEIGHT)
    
    # draw paddles
    p1pt1 = [paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT]
    p1pt2 = [paddle1_pos[0]-HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT]
    p1pt3 = [paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]+HALF_PAD_HEIGHT]
    p1pt4 = [paddle1_pos[0]+HALF_PAD_WIDTH,paddle1_pos[1]-HALF_PAD_HEIGHT]
    canvas.draw_polygon([(p1pt1[0],p1pt1[1]),(p1pt2[0],p1pt2[1]),(p1pt3[0],p1pt3[1]),(p1pt4[0],p1pt4[1])],1,"Red","Red")

    p2pt1 = [paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT]
    p2pt2 = [paddle2_pos[0]-HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT]
    p2pt3 = [paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]+HALF_PAD_HEIGHT]
    p2pt4 = [paddle2_pos[0]+HALF_PAD_WIDTH,paddle2_pos[1]-HALF_PAD_HEIGHT]
    canvas.draw_polygon([(p2pt1[0],p2pt1[1]),(p2pt2[0],p2pt2[1]),(p2pt3[0],p2pt3[1]),(p2pt4[0],p2pt4[1])],1,"Blue","Blue")
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 4,100], 50, "Red")
    canvas.draw_text(str(score2), [WIDTH / 4 * 3,100], 50, "Blue")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    acc = 5
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = acc
    elif key == simplegui.KEY_MAP['up']:
        paddle2_vel = - acc
    elif key == simplegui.KEY_MAP['s']:
        paddle1_vel = acc
    elif key == simplegui.KEY_MAP['w']:
        paddle1_vel = - acc
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button("Restart", new_game, 200)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# start frame
new_game()
frame.start()

