import pygame
import random

pygame.font.init()
pygame.mixer.init()
pygame.init()

SCREEN_SIZE = [1500, 1000]
BLUE = [51, 102, 255]
GREEN = [0, 255, 0]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 102]
SPEED = 5
FONT = pygame.font.SysFont('Arial', 25)

pygame.display.set_caption("Gold Miner")
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()
run = True

background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, SCREEN_SIZE)
image1 = pygame.image.load("character1.png")
image2 = pygame.image.load("character2.png")
imgae_of_gold = pygame.image.load("gold.png")
imgae_of_stone = pygame.image.load("stone.png")


def clear_screen():
    screen.fill(BLACK)

class vector():
    '''Khoi tao mot vecto voi hai thong so toa do x, y'''
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        '''cong hai vector'''
        new_vector = vector(self.x + other.x, self.y + other.y)
        return new_vector

    def __sub__(self, other):
        '''tru hai vector'''
        new_vector = vector(self.x - other.x, self.y - other.y)
        return new_vector

    def __mul__(self, other):
        '''nhan hai vector'''
        if isinstance(other, (int, float)):
            new_vector = vector(self.x * other, self.y * other)
        else:
            new_vector = vector(self.x * other.x, self.y * other.y)
        return new_vector

    def __str__(self):
        '''in ra vecto'''
        return f'({self.x}, {self.y})'

    #static_method: cac vecto chi huong
    def RIGHT():
        return vector(1, 0)
    def LEFT():
        return vector(-1, 0)
    def UP():
        return vector(0, -1)
    def DOWN():
        return vector(0, 1)

class character():
    '''Doi tuong nhan vat gap vang'''
    def __init__(self, image, size, position):
        self.__image = image
        self.__size = size
        self.__image = pygame.transform.scale(self.__image, self.__size)
        self.__position = position

    def draw(self):
        '''Ve nhan vat len man hinh'''
        screen.blit(self.__image, self.__position)

class gold():
    '''Doi tuong vang, nhan vat gap duoc vang se nhan duoc tien thuong'''
    def __init__(self, imgae, size, position):
        self.__image = imgae
        self.__size = size
        self.__image = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
    
    def draw(self):
        '''Ve vang len man hinh'''
        screen.blit(self.__image, self.__position)

class stone():
    '''Doi tuong vang, nhan vat gap duoc vang se nhan duoc tien thuong'''
    def __init__(self, imgae, size, position):
        self.__image = imgae
        self.__size = size
        self.__image = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
    
    def draw(self):
        '''Ve vang len man hinh'''
        screen.blit(self.__image, self.__position)

def main():
    run_game = True

    while run_game:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            run_game = False
        ###
        character1 = character(image1, (150, 150), (360, 150))
        character2 = character(image2, (140, 140), (930, 160))

        screen.blit(background, (0, 0))  # Vẽ ảnh nền
        character1.draw()
        character2.draw()

        num_of_gold = random.randint(5, 10)
        golds = []
        for i in range(num_of_gold):
            size = random.randint(50, 100)
            x = random.randint(0, SCREEN_SIZE[0]-size)
            y = random.randint(380, SCREEN_SIZE[1]-size)
            golds.append(gold(imgae_of_gold, (size, size), (x, y)))
            golds[i].draw()

        num_of_stone = random.randint(3, 6)
        stones = []
        for i in range(num_of_stone):
            size = random.randint(50, 100)
            x = random.randint(0, SCREEN_SIZE[0]-size)
            y = random.randint(380, SCREEN_SIZE[1]-size)
            stones.append(stone(imgae_of_stone, (size, size), (x, y)))
            stones[i].draw()

        pygame.display.update()
        clear_screen()
        clock.tick(30)

    return

while run:
    main()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    run = False
                    waiting = False

pygame.quit()