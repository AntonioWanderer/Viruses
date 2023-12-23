from random import randint, random
import pygame, time

width = 1200
height = 800
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
    def border(self):
        if self.x < 0 or self.x > width:
            self.velocity_x = - self.velocity_x
        if self.y < 0 or self.y > height:
            self.velocity_y = - self.velocity_y
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
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

    def border(self):
        if self.x < 0 or self.x > width:
            self.velocity_x = - self.velocity_x
        if self.y < 0 or self.y > height:
            self.velocity_y = - self.velocity_y
    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.border()

def game_init():
    pygame.init()
    screen = pygame.display.set_mode((width,height))
    screen.fill((0,0,0))
    return screen

def drawing(screen, viruses, circles):
    screen.fill((0,0,0))
    for item in viruses:
        pygame.draw.circle(screen,item.color, (item.x, item.y),item.radius)
    for item in circles:
        pygame.draw.circle(screen, item.color, (item.x, item.y), item.radius)
    pygame.display.update()

if __name__ == "__main__":
    screen1 = game_init()
    viruses = [virus() for i in range(100)]
    mans = [man() for i in range(100)]

    timer = 1
    running = True
    while running:
        timer += 1
        time.sleep(0.005)
        drawing(screen1,viruses,mans)
        for item in viruses:
            item.move()
        for item in mans:
            item.move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case 27: running = False