import pygame
import random
import math

pygame.font.init()
pygame.mixer.init()
pygame.init()

SCREEN_SIZE = [1500, 1000]
BLUE        = [51, 102, 255]
GREEN       = [0, 255, 0]
BLACK       = [0, 0, 0]
YELLOW      = [255, 255, 102]
SPEED       = 5
FONT        = pygame.font.SysFont('comic sans ms', 25)

pygame.display.set_caption("Gold Miner")
screen  = pygame.display.set_mode(SCREEN_SIZE)
clock   = pygame.time.Clock()
run     = True

background  = pygame.image.load("background.jpg")
background  = pygame.transform.scale(background, SCREEN_SIZE)
image1      = pygame.image.load("character1.png")
image2      = pygame.image.load("character2.png")
imgae_of_gold   = pygame.image.load("gold.png")
imgae_of_stone  = pygame.image.load("stone.png")
imgae_of_hook1  = pygame.image.load("hook1.png")
imgae_of_hook2  = pygame.image.load("hook2.png")


def clear_screen():
    screen.fill(BLACK)


class character():
    '''Doi tuong nhan vat gap vang'''
    def __init__(self, image, size, position, point):
        self.__image    = image
        self.__size     = size
        self.__image    = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
        self.__point    = point

    def draw(self):
        '''Ve nhan vat len man hinh'''
        screen.blit(self.__image, self.__position)

    def position(self):
        '''Tra ve vi tri cua doi tuong nay'''
        return self.__position

    def size(self):
        '''Tra ve kich thuoc cua doi tuong nay'''
        return self.__size

    def point(self, name, pos, color):
        '''Ve diem cua nhan vat len man hinh tai vi tri x, y'''
        score = FONT.render(f'Score of {name}: {self.__point}', True, color)
        screen.blit(score, pos)


class hook():
    '''Doi tuong can cau de dao vang'''
    def __init__(self, image, size, position, angle):
        self.__image    = image
        self.__size     = size
        self.__angle    = angle
        self.__image    = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
        # self.__position = (character.position()[0] + character.size()[0]//2 - self.__size[0]//2, character.position()[1] + character.size()[1]) 

    def rotate_image(self):
        '''Quay hinh anh moc cau quanh trung diem canh tren theo 1 goc'''
        rotated_image   = pygame.transform.rotate(self.__image, self.__angle)
        image_rect      = self.__image.get_rect(center = (self.__position[0] + self.__size[0]//2, self.__position[1]))
        rotated_rect    = rotated_image.get_rect(center = image_rect.center)

        return rotated_image, rotated_rect

    def draw(self):
        '''Ve can cau len man hinh'''
        # screen.blit(self.__image, (self.__position[0], self.__position[1]))
        rotated_image, new_rect = hook(self.__image, self.__size, self.__position, self.__angle).rotate_image()
        screen.blit(rotated_image, new_rect.topleft)

    def position(self):
        '''Tra ve vi tri cua doi tuong nay'''
        return self.__position

    def size(self):
        '''Tra ve kich thuoc cua doi tuong nay'''
        return self.__size

    def new_positon(self, x, y):
        '''Cap nhat lai gia tri vi tri'''
        self.__position = (x, y)

    def miner(self, obj):
        '''Kiem tra moc cau co cau trung doi tuong nao khong'''
        for i in range(len(obj)):
            if obj[i].position()[0] <= self.__position[0] + self.__size[0]//2 <= obj[i].position()[0] + obj[i].size()[0] and obj[i].position()[1] <= self.__position[1] + self.__size[1]//2 <= obj[i].position()[1] + obj[i].size()[1]:
                return True, i, obj[i].point()
        return False, -1, 0


class gold():
    '''Doi tuong vang, nhan vat gap duoc vang se nhan duoc tien thuong'''
    def __init__(self, image, size, position):
        self.__image    = image
        self.__size     = size
        self.__image    = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
    
    def draw(self):
        '''Ve vang len man hinh'''
        screen.blit(self.__image, self.__position)

    def position(self):
        '''Tra ve vi tri cua doi tuong nay'''
        return self.__position

    def size(self):
        '''Tra ve kich thuoc cua doi tuong nay'''
        return self.__size

    def point(self):
        '''Tra ve so diem tuong ung'''
        return self.__size[0]


class stone():
    '''Doi tuong vang, nhan vat gap duoc vang se nhan duoc tien thuong'''
    def __init__(self, image, size, position):
        self.__image    = image
        self.__size     = size
        self.__image    = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
    
    def draw(self):
        '''Ve da len man hinh'''
        screen.blit(self.__image, self.__position)
    
    def position(self):
        '''Tra ve vi tri cua doi tuong nay'''
        return self.__position

    def size(self):
        '''Tra ve kich thuoc cua doi tuong nay'''
        return self.__size

    def point(self):
        '''Tra ve so diem tuong ung'''
        return self.__size[0]


def main():
    run_game    = True
    
    num_of_gold = random.randint(10, 15)
    golds = []
    for i in range(num_of_gold):
        size = random.randint(50, 100)
        x   = random.randint(0, SCREEN_SIZE[0]-size)
        y   = random.randint(450, SCREEN_SIZE[1]-size)
        golds.append(gold(imgae_of_gold, (size, size), (x, y)))

    num_of_stone = random.randint(10, 13)
    stones = []
    for i in range(num_of_stone):
        size = random.randint(50, 100)
        x = random.randint(0, SCREEN_SIZE[0]-size)
        y = random.randint(450, SCREEN_SIZE[1]-size)
        stones.append(stone(imgae_of_stone, (size, size), (x, y)))
        
    angle   = 35
    tmp     = 1
    point_1, point_2 = [0, 0]

    character1  = character(image1, (150, 150), (360, 150), 0)
    hook1_x, hook1_y = [360 + 150//2 - 100//2, 150 + 150]
    hook1       = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)

    character2  = character(image2, (140, 140), (930, 160), 0)
    hook2_x, hook2_y = [930 + 140//2 - 100//2, 160 + 140]
    hook2       = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)
    
    while run_game:
          
        tmp     %= 360  
        angle   += tmp #ti mo lai nhaaaaaaaaaaaaaaaaaaaaaaaaaaaa

        #Tao 2 nhan vat
        character1 = character(image1, (150, 150), (360, 150), point_1)
        character2 = character(image2, (140, 140), (930, 160), point_2)

        #Tao 2 cai can cau
        hook1_x, hook1_y = hook1.position()
        hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
        hook1.new_positon(hook1_x, hook1_y)

        hook2_x, hook2_y = hook2.position()
        hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)
        hook2.new_positon(hook2_x, hook2_y)
        
              
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            run_game = False
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            num_of_gold = random.randint(10, 15)
            golds = []
            for i in range(num_of_gold):
                size = random.randint(50, 100)
                x = random.randint(0, SCREEN_SIZE[0]-size)
                y = random.randint(450, SCREEN_SIZE[1]-size)
                golds.append(gold(imgae_of_gold, (size, size), (x, y)))

            num_of_stone = random.randint(10, 13)
            stones = []
            for i in range(num_of_stone):
                size = random.randint(50, 100)
                x = random.randint(0, SCREEN_SIZE[0]-size)
                y = random.randint(450, SCREEN_SIZE[1]-size)
                stones.append(stone(imgae_of_stone, (size, size), (x, y)))

            angle = 0
            hook1_x, hook1_y = [360 + 150//2 - 100//2, 150 + 150]
            hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
            hook2_x, hook2_y = [930 + 140//2 - 100//2, 160 + 140]
            hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)

            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:        
            hook1_x, hook1_y = hook1.position()
            
            if 0 <= hook1_x + hook1.size()[0]//2 <= SCREEN_SIZE[0] and 0 <= hook1_y + hook1.size()[1]//2 <= SCREEN_SIZE[1]:
                angle_radian = math.pi * angle / 180
                dx = hook1.size()[1] * math.sin(angle_radian)
                dy = hook1.size()[1] * math.cos(angle_radian)
                hook1_x += dx
                hook1_y += dy
                hook1.new_positon(hook1_x, hook1_y)
                hook1.draw()
                # print(hook1_x, hook1_y, hook1.size()[1], angle, math.sin(angle), math.cos(angle))
            else:
                hook1_x, hook1_y = [360 + 150//2 - 100//2, 150 + 150]
                hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
                # print(hook1_x, hook1_y, hook1.size()[1], angle)
            
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            hook2_x, hook2_y = hook2.position()
            
            if 0 <= hook2_x + hook2.size()[0]//2 <= SCREEN_SIZE[0] and 0 <= hook2_y + hook2.size()[1]//2 <= SCREEN_SIZE[1]:
                angle_radian = - math.pi * angle / 180
                dx = hook2.size()[1] * math.sin(angle_radian)
                dy = hook2.size()[1] * math.cos(angle_radian)
                hook2_x += dx
                hook2_y += dy
                hook2.new_positon(hook2_x, hook2_y)
                hook2.draw()
                # print(hook2_x, hook2_y, hook1.size()[1], angle, math.sin(angle), math.cos(angle))
            else:
                hook2_x, hook2_y = [930 + 140//2 - 100//2, 160 + 140]
                hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)
                # print(hook2_x, hook2_y, hook1.size()[1], angle)

        #Ve hinh nen, nhan vat, can cau
        screen.blit(background, (0, 0)) 
        character1.draw()
        character2.draw()
        character1.point('Harry', (360,80), BLUE)
        character2.point('Hermione', (915,80), GREEN)
        hook1.draw()
        hook2.draw()

        #Ve vang va da
        for i in range(len(golds)):
            golds[i].draw()
        for i in range(len(stones)):
            stones[i].draw()

        #Kiem tra moc cau co cham vao vat the nao hay khong
        gold_check_1, gold_index_1, plus_point_1 = hook1.miner(golds)
        if gold_check_1:
            point_1 += plus_point_1
            golds.pop(gold_index_1)
        stone_check_1, stone_index_1, plus_point_1 = hook1.miner(stones)
        if stone_check_1:
            point_1 += plus_point_1
            stones.pop(stone_index_1)

        gold_check_2, gold_index_2, plus_point_2 = hook2.miner(golds)
        if gold_check_2:
            point_2 += plus_point_2
            golds.pop(gold_index_2)
        stone_check_2, stone_index_2, plus_point_2 = hook2.miner(stones)
        if stone_check_2:
            point_2 += plus_point_2
            stones.pop(stone_index_2)

            
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