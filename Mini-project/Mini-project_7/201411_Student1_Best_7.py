# Spacegame
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim

# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.acc = 5. / 60
        self.dec = 0.99
        self.thrust = False
        self.angle = angle
        self.angle_vel = math.pi / 60
        self.rotation_dir = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()

    def draw(self,canvas):
        canvas.draw_image(ship_image,        # image
                          self.image_center, # center_source
                          self.image_size,   # width_height_source
                          self.pos,          # center_dest
                          self.image_size,   # width_heitht_dest
                          self.angle)        # rotation

    def update(self):
        self.vel[0] = self.vel[0] * self.dec + angle_to_vector(self.angle)[0] * self.thrust * self.acc
        self.vel[1] = self.vel[1] * self.dec + angle_to_vector(self.angle)[1] * self.thrust * self.acc
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle = self.angle + self.angle_vel * self.rotation_dir

    def rotate_left(self):
        self.rotation_dir = -1

    def rotate_right(self):
        self.rotation_dir = 1

    def stop_rotation(self):
        self.rotation_dir = 0

    def thrusters_on(self):
        self.thrust = True
        self.image_center[0] = self.image_center[0] + self.image_size[0]
        ship_thrust_sound.play()

    def thrusters_off(self):
        self.thrust = False
        self.image_center[0] = self.image_center[0] - self.image_size[0]
        ship_thrust_sound.rewind()

    def shoot(self):
        global a_missile
        pos = [self.pos[0] + angle_to_vector(self.angle)[0] * self.radius, # pos x
               self.pos[1] + angle_to_vector(self.angle)[1] * self.radius] # pos y
        vel = [self.vel[0] + angle_to_vector(self.angle)[0] * 3,           # vel x
               self.vel[1] + angle_to_vector(self.angle)[1] * 3]           # vel y
        a_missile = Sprite(pos, vel, 0, 0, missile_image, missile_info, missile_sound) # sound

# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def draw(self, canvas):
        canvas.draw_image(self.image,        # image
                          self.image_center, # center_source
                          self.image_size,   # width_height_source
                          self.pos,          # center_dest
                          self.image_size,   # width_heitht_dest
                          self.angle)        # rotation

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle = self.angle + self.angle_vel

def draw(canvas):
    global time

    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)

    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()

    # Draw score and lives
    fontFace = 'monospace'
    fontColor = 'White'
    fontSize = 20
    vertDist = 25
    horiDist = 10
    livesTxt = 'Lives: ' + str(lives)
    scoreTxt = 'Score: ' + str(score)
    canvas.draw_text(livesTxt, (horiDist, vertDist), fontSize, fontColor, fontFace)
    scoreWidth = frame.get_canvas_textwidth(scoreTxt, fontSize, fontFace)
    canvas.draw_text(scoreTxt, (WIDTH-scoreWidth-horiDist, vertDist), fontSize, fontColor, fontFace)

def keydown(key):
    for i in keydown_dict:
        if key==simplegui.KEY_MAP[i]:
            keydown_dict[i]()

def keyup(key):
    for i in keyup_dict:
        if key==simplegui.KEY_MAP[i]:
            keyup_dict[i]()

# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    pos = [random.randrange(0, WIDTH),        # pos x
           random.randrange(0, HEIGHT)]       # pos y
    vel = [random.randrange(-10,10)/10.,      # vel x
           random.randrange(-10,10)/10.]      # vel y
    ang = random.randrange(0,360)*math.pi/180 # angle
    ang_vel = random.randrange(-10,10)/100.   # angle velocity
    a_rock = Sprite(pos,vel,ang,ang_vel,asteroid_image,asteroid_info)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], # pos
               [0, 0],     # vel
               0,          # angle
               ship_image, # image
               ship_info)  # info

a_rock = Sprite([WIDTH / 3, HEIGHT / 3], # pos
                [1, 0],         # vel
                0,              # angle
                3.14/60,        # ang_vel
                asteroid_image, # image
                asteroid_info)  # info

a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], # pos
                   [-1,1],        # vel
                   0,             # ang
                   0,             # ang_vel
                   missile_image, # image
                   missile_info,  # info
                   missile_sound) # sound

keydown_dict = {'left': my_ship.rotate_left,
                'right': my_ship.rotate_right,
                'up': my_ship.thrusters_on,
                'space': my_ship.shoot}
keyup_dict =   {'left': my_ship.stop_rotation,
                'right': my_ship.stop_rotation,
                'up': my_ship.thrusters_off}

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()

