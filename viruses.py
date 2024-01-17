from random import randint, random
import pygame, time
import numpy as np

#screen size
width = 1200
height = 800
G = 0.001

class creature:
    def __init__(self):
        self.color = (255,255,255)
        self.max_hp = 10
        self.hp = 10
        self.lifetime = 0
        self.maxlife = 1e6
        self.radius = 5
        self.x = randint(0, width)
        self.y = randint(0,height)
        self.velocity_x = 2*random()-1
        self.velocity_y = 2*random()-1
        self.score = 0
        self.acceleration_x = 0
        self.acceleration_y = 0

    def __sub__(self, other):
        distance = ((self.x-self.y)**2+(other.x-other.y)**2)**0.5
        return distance

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
        #self.velocity_normalisation()
        self.border()

class virus(creature):
    def __init__(self):
        creature.__init__(self)
        self.maxlife = 1e7
        self.color = (255,0,0)
        self.radius = 5
        self.score = 0

    def __add__(self, other):
        baby = virus()
        return baby

class man(creature):
    def __init__(self):
        creature.__init__(self)
        self.maxlife = 1e8
        self.color = (0,255,0)
        self.radius = 5

    def __add__(self, other):
        baby = man()
        return baby

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
#infection
def collisions(viruses, mans):
    for virus in viruses:
        for man in mans:
            if virus - man < virus.radius + man.radius:
                mans.remove(man)
                man.color = (255,255,255)
    return mans

def dieOld(animals):
    for animal in animals:
        if random()<animal.lifetime/animal.maxlife:
            animals.remove(animal)
    return animals

def comeOld(animals):
    for animal in animals:
        animal.lifetime += 1
def borning(animals):
    children = []
    for mother in animals:
        for father in animals:
            if mother - father < mother.radius + father.radius and random()>0.99:
                children.append(mother+father)
    return children

if __name__ == "__main__":
    screen1 = game_init()
    viruses = [virus() for i in range(100)]
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
        mans = collisions(viruses,mans)
        comeOld(viruses)
        comeOld(mans)
        viruses = dieOld(viruses)
        mans = dieOld(mans)
        mans += borning(mans)
        viruses += borning(viruses)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case 27: running = False