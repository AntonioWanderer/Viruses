from random import randint, random
import pygame, time

#screen size
width = 1200
height = 800
G = 0.0001

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
        if self.x < 0 or self.x > width:
            self.velocity_x = - self.velocity_x
        if self.y < 0 or self.y > height:
            self.velocity_y = - self.velocity_y

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
        if self.x < 0 or self.x > width:
            self.velocity_x = - self.velocity_x
        if self.y < 0 or self.y > height:
            self.velocity_y = - self.velocity_y

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
def drawing(screen, viruses, circles):
    screen.fill((0,0,0))
    for item in viruses:
        pygame.draw.circle(screen,item.color, (item.x, item.y),item.radius)
    for item in circles:
        pygame.draw.circle(screen, item.color, (item.x, item.y), item.radius)
    pygame.display.update()
#virus2man infection
def collisions(viruses, mans):
    for item_v in viruses:
        item_v.acceleration_x = 0
        item_v.acceleration_y = 0
        for item_m in mans:
            distance = line(item_v.x,item_m.x,item_v.y,item_m.y)
            if distance <= item_v.radius + item_m.radius:
                item_v.infect = True
                item_v.score += 1
                item_m.infected = True
                item_m.color = (255,255,255)
                item_m.infected_time = 100
            else:
                item_v.acceleration_x += G * 1 / abs(item_m.x-item_v.x)**3 * (item_m.x-item_v.x)
                item_v.acceleration_y += G * 1 / abs(item_m.y-item_v.y)** 3 * (item_m.y - item_v.y)
    for item_m in mans:
        item_m.acceleration_x = 0
        item_m.acceleration_y = 0
        for item_v in viruses:
            distance = line(item_v.x, item_m.x, item_v.y, item_m.y)
            if distance <= item_v.radius + item_m.radius:
                pass
            else:
                item_m.acceleration_x += G * 1 / abs(item_m.x - item_v.x) ** 3 * (item_m.x - item_v.x)
                item_m.acceleration_y += G * 1 / abs(item_m.y - item_v.y) ** 3 * (item_m.y - item_v.y)

    #man2man infection
    # for item_v in mans:
    #     for item_m in mans:
    #         distance = line(item_v.x,item_m.x,item_v.y,item_m.y)
    #         if distance <= item_v.radius + item_m.radius:
    #             if item_v.infected and not item_m.infected:
    #                 item_m.infected = True
    #                 item_m.color = (255,255,255)
    #                 item_m.infected_time = 100
    #             elif not item_v.infected and item_m.infected:
    #                 item_v.infected = True
    #                 item_v.color = (255,255,255)
    #                 item_v.infected_time = 100

if __name__ == "__main__":
    screen1 = game_init()
    viruses = [virus() for i in range(20)]
    mans = [man() for i in range(100)]

    timer = 0 #timer of steps
    running = True
    while running:
        timer += 1
        time.sleep(0.005)
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