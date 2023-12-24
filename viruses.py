from random import randint, random
import pygame, time, numpy

#screen size
width = 1200
height = 800
G = 0.001

class virus:
    def __init__(self):
        self.color = (255,0,0)
        self.max_hp = 10
        self.hp = 10
        self.radius = 2
        self.x = randint(0, width)
        self.y = randint(0,height)
        self.velocity_x = 2*random()-1
        self.velocity_y = 2*random()-1
        self.infect = False
        self.score = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

    def border(self):
        if self.x < self.radius:
            self.velocity_x = - self.velocity_x
            self.x = self.radius
        if self.x > width - self.radius:
            self.velocity_x = - self.velocity_x
            self.x = width - self.radius
        if self.y < self.radius:
            self.velocity_y = - self.velocity_y
            self.y = self.radius
        if self.y > height - self.radius:
            self.velocity_y = - self.velocity_y
            self.y = height - self.radius

    def velocity_normalisation(self):
        length = line(0,self.velocity_x,0,self.velocity_y)
        self.velocity_x /= length
        self.velocity_y /= length
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y
        self.velocity_normalisation()
        self.border()

class man:
    def __init__(self):
        self.color = (0,255,0)
        self.max_hp = 10
        self.hp = 10
        self.radius = 5
        self.x = randint(0, width)
        self.y = randint(0, height)
        self.velocity_x = 2*random()-1
        self.velocity_y = 2*random()-1
        self.infected = False
        self.infected_time = 0
        self.acceleration_x = 0
        self.acceleration_y = 0
    #reversing in walls
    def border(self):
        if self.x < self.radius:
            self.velocity_x = - self.velocity_x
            self.x = self.radius
        if self.x > width-self.radius:
            self.velocity_x = - self.velocity_x
            self.x = width-self.radius
        if self.y < self.radius:
            self.velocity_y = - self.velocity_y
            self.y = self.radius
        if self.y > height-self.radius:
            self.velocity_y = - self.velocity_y
            self.y = height-self.radius

    def velocity_normalisation(self):
        length = line(0,self.velocity_x,0,self.velocity_y)
        self.velocity_x /= length
        self.velocity_y /= length
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_x += self.acceleration_x
        self.velocity_y += self.acceleration_y
        self.velocity_normalisation()
        self.border()

    def treating(self):
        if self.infected_time > 0:
            self.infected_time -= 1
            if self.infected_time == 0:
                self.color = (0, 255, 0)

def line(x1,x2,y1,y2):
    r = ((x1-x2)**2 + (y1-y2)**2)**0.5
    return r
def game_init():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    screen.fill((0,0,0))
    return screen
#drawing circles
def drawing(screen, viruses, mans):
    screen.fill((0,0,0))
    for item in viruses:
        pygame.draw.circle(screen,item.color, (item.x, item.y),item.radius)
    for item in mans:
        pygame.draw.circle(screen, item.color, (item.x, item.y), item.radius)
    pygame.display.update()
#virus2man infection
def gravity(vector):
    return G * 1 / abs(vector) ** 7 * (vector)
def collisions(viruses, mans):
    distances = numpy.zeros((len(viruses),len(mans)))
    for v in range(len(viruses)):
        for m in range(len(mans)):
            distances[v, m] = line(viruses[v].x, mans[m].x, viruses[v].y, mans[m].y)

    for v in range(len(viruses)):
        viruses[v].acceleration_x = 0
        viruses[v].acceleration_y = 0
        for m in range(len(mans)):
            if distances[v, m] <= viruses[v].radius + mans[m].radius:
                viruses[v].infect = True
                viruses[v].score += 1
                mans[m].infected = True
                mans[m].color = (255,255,255)
                mans[m].infected_time = 100
            elif distances[v, m] <= viruses[v].radius * 10:
                viruses[v].acceleration_x += gravity(mans[m].x-viruses[v].x)
                viruses[v].acceleration_y += gravity(mans[m].y-viruses[v].y)
    for m in range(len(mans)):
        mans[m].acceleration_x = 0
        mans[m].acceleration_y = 0
        for v in range(len(viruses)):
            if distances[v,m] <= mans[m].radius * 10:
                mans[m].acceleration_x -= gravity(mans[m].x - viruses[v].x)
                mans[m].acceleration_y -= gravity(mans[m].y - viruses[v].y)

    #man2man infection
    for item_v in mans:
     for item_m in mans:
         distance = line(item_v.x,item_m.x,item_v.y,item_m.y)
         if distance <= item_v.radius + item_m.radius:
             if item_v.infected and not item_m.infected:
                 item_m.infected = True
                 item_m.color = (255,255,255)
                 item_m.infected_time = 100
             elif not item_v.infected and item_m.infected:
                 item_v.infected = True
                 item_v.color = (255,255,255)
                 item_v.infected_time = 100

if __name__ == "__main__":
    screen1 = game_init()
    viruses = [virus() for i in range(100)]
    mans = [man() for i in range(100)]

    timer = 0 #timer of steps
    running = True
    while running:
        timer += 1
        time.sleep(0.0005)
        drawing(screen1,viruses,mans)
        for item in viruses:
            item.move()
        for item in mans:
            item.move()
            item.treating()
        collisions(viruses,mans)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case 27: running = False