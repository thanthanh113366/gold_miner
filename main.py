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
WHITE       = [255, 255, 255] 
YELLOW      = [255, 255, 102]
RED         = [255, 0, 0]
DULL_YELLOW = [186, 124, 0]
# DULL_YELLOW = [166, 124, 0]
SCREEN  = pygame.display.set_mode(SCREEN_SIZE)
SPEED       = 5
FONT_PATH   = "FONT/HARRYP__.TTF"
FONT_SIZE   = 30
FONT = pygame.font.Font(FONT_PATH, FONT_SIZE)
SOUND_INTRO = pygame.mixer.Sound('SOUND/intro.wav')
SOUND_START = pygame.mixer.Sound('SOUND/leviosa.wav')
SOUND_GAME = pygame.mixer.Sound('SOUND/game.wav')
CHARACTER = {
    1: "Harry",
    2: "Hermione",
    3: "Ron",
    4: "Dumbledore",
    5: "MC Gonagall",
    6: "Snape",
    7: "Voldemort",
    8: "DRAW"
}

# pygame.display.set_caption("Gold Miner - Leviosa")
# SCREEN  = pygame.display.set_mode(SCREEN_SIZE)
# clock   = pygame.time.Clock()
# run     = True

game_background  = pygame.image.load("OBJ/background2.png")
game_background  = pygame.transform.scale(game_background, SCREEN_SIZE)

select_background  = pygame.image.load("OBJ/background.png")
select_background  = pygame.transform.scale(select_background, SCREEN_SIZE)

balloon     = pygame.image.load("OBJ/balloon.png")
imgae_of_gold   = pygame.image.load("OBJ/gold.png")
imgae_of_stone  = pygame.image.load("OBJ/stone.png")
imgae_of_dementor  = pygame.image.load("OBJ/dementor.png")
imgae_of_hook1  = pygame.image.load("OBJ/hook1.png")
imgae_of_hook2  = pygame.image.load("OBJ/hook2.png")



# def get_game_time():
#     input_active = True
#     user_input = ''

#     while input_active:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#                 exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_RETURN:
#                     input_active = False
#                 elif event.key == pygame.K_BACKSPACE:
#                     user_input = user_input[:-1]
#                 else:
#                     user_input += event.unicode
        
#         SCREEN.fill(BLACK)
#         prompt_text = FONT.render('Enter game time (seconds):', True, WHITE)
#         input_text = FONT.render(user_input, True, GREEN)
#         SCREEN.blit(prompt_text, (SCREEN_SIZE[0] // 2 - prompt_text.get_width() // 2, SCREEN_SIZE[1] // 2 - 50))
#         SCREEN.blit(input_text, (SCREEN_SIZE[0] // 2 - input_text.get_width() // 2, SCREEN_SIZE[1] // 2))
#         pygame.display.flip()
    
#     try:
#         return int(user_input)
#     except ValueError:
#         return 60  # Nếu người chơi nhập không phải là số, đặt thời gian mặc định là 60 giây



# def clear_screen():
#     SCREEN.fill(BLACK)



class character():
    '''Doi tuong nhan vat gap vang'''
    def __init__(self, image, size, position, point):
        self.__image    = image
        self.__size     = size
        self.__image    = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
        self.__point    = point

    def draw(self, balloon):
        '''Ve nhan vat len man hinh'''
        SCREEN.blit(self.__image, self.__position)
        balloon = pygame.transform.scale(balloon, self.__size)
        SCREEN.blit(balloon, self.__position)

    def position(self):
        '''Tra ve vi tri cua doi tuong nay'''
        return self.__position

    def size(self):
        '''Tra ve kich thuoc cua doi tuong nay'''
        return self.__size

    def point(self, name, pos, color):
        '''Ve diem cua nhan vat len man hinh tai vi tri x, y'''
        score = FONT.render(f'Score of {name}: {self.__point}', True, color)
        SCREEN.blit(score, pos)
        return self.__point

    def draw_magic_beam(self, enermy, color, width):
        '''Tao duong phep thuat den ke thua'''
        pygame.draw.line(SCREEN, color, self.__position, enermy.position(), width)



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
        # SCREEN.blit(self.__image, (self.__position[0], self.__position[1]))
        rotated_image, new_rect = hook(self.__image, self.__size, self.__position, self.__angle).rotate_image()
        SCREEN.blit(rotated_image, new_rect.topleft)

    def position(self):
        '''Tra ve vi tri cua doi tuong nay'''
        return self.__position

    def size(self):
        '''Tra ve kich thuoc cua doi tuong nay'''
        return self.__size

    def angle(self):
        '''Tra ve so do goc hien tai cua doi tuong nay'''
        return self.__angle

    def point(self):
        '''Tru diem khi hai moc cau gap nhau'''
        return -50

    def new_positon(self, x, y):
        '''Cap nhat lai gia tri vi tri'''
        self.__position = (x, y)
    
    def miner(self, obj):
        '''Kiem tra moc cau co cau trung doi tuong nao khong'''
        for i in range(len(obj)):
            center_x    = self.__position[0] + self.__size[0]//2
            center_y    = self.__position[1] + self.__size[1]//2
            obj_x       = [obj[i].position()[0], obj[i].position()[0] + obj[i].size()[0]]
            obj_y       = [obj[i].position()[1], obj[i].position()[1] + obj[i].size()[1]]
            if ( obj_x[0] <= center_x <= obj_x[1] or obj_x[0] <= center_x - self.__size[0] // 4 <= obj_x[1] or obj_x[0] <= center_x + self.__size[0] // 4 <= obj_x[1] ) and ( obj_y[0] <= center_y <= obj_y[1] or obj_y[0] <= center_y - self.__size[1] // 4 <= obj_y[1] or obj_y[0] <= center_y + self.__size[1] // 4 <= obj_y[1] ):
                return True, i, obj[i].point()
        return False, -1, 0



class obj():
    '''Doi tuong vang, nhan vat gap duoc vang se nhan duoc tien thuong'''
    def __init__(self, image, size, position):
        self.__image    = image
        self.__size     = size
        self.__image    = pygame.transform.scale(self.__image, self.__size)
        self.__position = position
    
    def draw(self):
        '''Ve vang len man hinh'''
        SCREEN.blit(self.__image, self.__position)

    def position(self):
        '''Tra ve vi tri cua doi tuong nay'''
        return self.__position

    def size(self):
        '''Tra ve kich thuoc cua doi tuong nay'''
        return self.__size

    def point(self):
        '''Tra ve so diem tuong ung'''
        return self.__size[0]



class system():
    ''' Doi tuong he thong, quan li moi hoat dong cua tro choi'''
    def __init__(self):
        pygame.display.set_caption("Gold Miner - Leviosa")
        self.__clock   = pygame.time.Clock()
        self.__run     = True
        self.__GAME_TIME = 0
        self.__DEATH_TIME = 0
        self.__image1 = pygame.image.load('CHARACTER/1.png')
        self.__image2 = pygame.image.load('CHARACTER/1.png')
        self.__name1  = 1
        self.__name2  = 1

        

    def get_game_time(self):
        '''Phuong thuc lay thoi gian gameplay theo lua chon cua nguoi choi'''
        input_active = True
        user_input = ''

        while input_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    else:
                        user_input += event.unicode
            
            SCREEN.fill(BLACK)
            prompt_text = FONT.render('Enter game time (seconds):', True, WHITE)
            input_text = FONT.render(user_input, True, GREEN)
            SCREEN.blit(prompt_text, (SCREEN_SIZE[0] // 2 - prompt_text.get_width() // 2, SCREEN_SIZE[1] // 2 - 50))
            SCREEN.blit(input_text, (SCREEN_SIZE[0] // 2 - input_text.get_width() // 2, SCREEN_SIZE[1] // 2))
            pygame.display.flip()
        
        try:
            return int(user_input)
        except ValueError:
            return 60  # Nếu người chơi nhập không phải là số, đặt thời gian mặc định là 60 giây

        # try:
        #     self.__GAME_TIME = int(user_input)
        # except ValueError:
        #     self.__GAME_TIME = 60  # Nếu người
        

    def play_game(self):
        '''Phuong thuc vong lap cua game, qua lai giua cac che do chon nhan vat, thoi gian, gameplay va man hinh chien thang'''
        while self.__run:
            selected = False
            selected1, selected2 = False, False

            self.__name1 = 'x'
            self.__name2 = 'y'

            SCREEN.blit(select_background, (0, 0))
            SOUND_GAME.stop()
            SOUND_START.stop()
            SOUND_INTRO.play()


            # if selected:
            #     self.__name1      = pygame.image.load(f"CHARACTER/character1/{self.__name1}.png")
            #     self.__name2      = pygame.image.load(f"CHARACTER/character2/character2.png")    
            #     main(self.__name1, self.__name2)

            while not selected:

                instructions = FONT.render("""Press 1 for Harry, 2 for Hermione, 3 for Ron, 4 for Dumbledore, 5 for MC Gonagall, 6 for Snape, 7 for Voldemort""", True, DULL_YELLOW)
                SCREEN.blit(instructions, (SCREEN_SIZE[0]//2 - instructions.get_width()//2, SCREEN_SIZE[1]//2+200))

                string = FONT.render("Press Q for Quit", True, DULL_YELLOW)
                SCREEN.blit(string, (SCREEN_SIZE[0]//2 - string.get_width()//2, SCREEN_SIZE[1] - 100))
                
                # screen.blit(select_background, (0, 0))
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:    
                        self.__run = False                  
                        exit()
                        # system.exit()
                    elif event.type == pygame.KEYDOWN:
                        # selected, selected1, self.__name1 = select(event)
                        if event.key == pygame.K_q:
                            self.__run = False
                            exit()
                            # system.exit()

                        elif selected1 == False and event.key - pygame.K_0 in range(1,8):
                            self.__name1 = event.key - pygame.K_0
                            self.__image1 = pygame.image.load(f'CHARACTER/{self.__name1}.png')
                            self.__image1 = pygame.transform.scale(self.__image1, (200, 200))
                            SCREEN.blit(self.__image1, (0 + 200, SCREEN_SIZE[1]//2 - 100))
                        
                            string = FONT.render(CHARACTER[self.__name1], True, DULL_YELLOW)
                            SCREEN.blit(string, (0 + 220, SCREEN_SIZE[1]//2 + 100))
                            
                            selected1 = True

                        elif selected1 == True and event.key - pygame.K_0 in range(1,8):
                            self.__name2 = event.key - pygame.K_0
                            self.__image2 = pygame.image.load(f'CHARACTER/{self.__name2}.png')
                            self.__image2 = pygame.transform.flip(self.__image2, True, False)
                            self.__image2 = pygame.transform.scale(self.__image2, (200, 200))
                            SCREEN.blit(self.__image2, (SCREEN_SIZE[0] - string.get_width()//2 - 200, SCREEN_SIZE[1]//2 - 100))
                            # screen.fill()

                            old_string = FONT.render(CHARACTER[self.__name1], True, DULL_YELLOW)
                            SCREEN.blit(old_string, (0 + 220, SCREEN_SIZE[1]//2 + 100))
                            
                            string = FONT.render(CHARACTER[self.__name2], True, DULL_YELLOW)
                            SCREEN.blit(string, (SCREEN_SIZE[0] - string.get_width()//2 - 220, SCREEN_SIZE[1]//2 + 100))

                            string = FONT.render("Press Enter", True, DULL_YELLOW)
                            SCREEN.blit(string, (SCREEN_SIZE[0]//2 - string.get_width()//2 - 30, SCREEN_SIZE[1]//2 - 10))

                            selected2 = True

                        elif selected2 == True and event.key == pygame.K_RETURN:
                            selected = True

                    # print(self.__name1, self.__name2, selected1

            self.__GAME_TIME   = system().get_game_time()

            if selected:
                character_win, name = system().main(self.__GAME_TIME, self.__image1, self.__image2)
                if name == 1: name = self.__name1
                elif name == 2: name = self.__name2
                elif name == 0: name = 8
                for i in range(len(character_win)):
                    character_win[i].draw(balloon)
                character_win[0].point(CHARACTER[name], (SCREEN_SIZE[0]//2-90, SCREEN_SIZE[1]//2), GREEN) 
                waiting = True
                # clear_screen()
                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                waiting = False
                    
                    prompt_text = FONT.render('Press Enter to continue', True, WHITE)
                    SCREEN.blit(prompt_text, (SCREEN_SIZE[0] // 2 - prompt_text.get_width() // 2, SCREEN_SIZE[1] // 2 + 300))
                    pygame.display.flip()



    def main(self, GAME_TIME, image1, image2):
        '''Phuong thuc chua vong lap chinh, noi dien ra gameplay chinh thuc'''
        SOUND_INTRO.stop()
        SOUND_START.play()
        SOUND_GAME.play()
        run_game        = True

        start_sticks    = pygame.time.get_ticks()
        paused          = False
        paused_start    = 0
        total_paused_time = 0
        elapsed_time    = GAME_TIME
        self.__DEATH_TIME  = GAME_TIME - GAME_TIME // 3

        angle           = random.randint(0, 360)
        speed           = 4
        point_1, point_2 = [0, 0]
        
        num_of_gold = random.randint(10, 15)
        golds = []
        for i in range(num_of_gold):
            size = random.randint(50, 100)
            x   = random.randint(0, SCREEN_SIZE[0]-size)
            y   = random.randint(300, SCREEN_SIZE[1]-size)
            golds.append(obj(imgae_of_gold, (size, size), (x, y)))

        num_of_stone = random.randint(10, 13)
        stones = []
        for i in range(num_of_stone):
            size = random.randint(50, 100)
            x = random.randint(0, SCREEN_SIZE[0]-size)
            y = random.randint(300, SCREEN_SIZE[1]-size)
            stones.append(obj(imgae_of_stone, (size, size), (x, y)))
            
        dementors = []

        character1  = character(image1, (150, 150), (60, 150), 0)
        hook1_x, hook1_y = [60 + 150//2 - 100//2, 150 + 150]
        hook1       = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)

        character2  = character(image2, (140, 140), (1200, 160), 0)
        hook2_x, hook2_y = [1200 + 140//2 - 100//2, 160 + 140]
        hook2       = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)
        
        while run_game:
            speed     %= 60  
            angle   += speed #ti mo lai nhaaaaaaaaaaaaaaaaaaaaaaaaaaaa

            #Tao 2 nhan vat
            character1 = character(image1, (150, 150), (60, 150), point_1)
            character2 = character(image2, (140, 140), (1200, 160), point_2)

            #Tao 2 cai can cau
            hook1_x, hook1_y = hook1.position()
            hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
            hook1.new_positon(hook1_x, hook1_y)

            hook2_x, hook2_y = hook2.position()
            hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)
            hook2.new_positon(hook2_x, hook2_y)

            if self.__DEATH_TIME - 0.01 <= elapsed_time <= self.__DEATH_TIME + 0.01:
                num_of_dementor = random.randint(4, 6)
                for i in range(num_of_dementor):
                    size = random.randint(50, 100)
                    x   = random.randint(0, SCREEN_SIZE[0]-size)
                    y   = random.randint(300, SCREEN_SIZE[1]-size)
                    dementors.append(obj(imgae_of_dementor, (size, size), (x, y)))
                    
            event = pygame.event.poll()
        
            if event.type == pygame.QUIT:
                run_game = False
                if paused:
                    paused = False
                    total_paused_time += pygame.time.get_ticks() - paused_start
                else:
                    paused = True
                    paused_start = pygame.time.get_ticks()
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                num_of_gold = random.randint(10, 15)
                golds = []
                for i in range(num_of_gold):
                    size = random.randint(50, 100)
                    x = random.randint(0, SCREEN_SIZE[0]-size)
                    y = random.randint(450, SCREEN_SIZE[1]-size)
                    golds.append(obj(imgae_of_gold, (size, size), (x, y)))

                num_of_stone = random.randint(10, 13)
                stones = []
                for i in range(num_of_stone):
                    size = random.randint(50, 100)
                    x = random.randint(0, SCREEN_SIZE[0]-size)
                    y = random.randint(450, SCREEN_SIZE[1]-size)
                    stones.append(obj(imgae_of_stone, (size, size), (x, y)))

                angle = 0
                hook1_x, hook1_y = [60 + 150//2 - 100//2, 150 + 150]
                hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
                hook2_x, hook2_y = [1200 + 140//2 - 100//2, 160 + 140]
                hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:        
                hook1_x, hook1_y = hook1.position()
                
                if 0 <= hook1_x + hook1.size()[0]//2 <= SCREEN_SIZE[0] and 0 <= hook1_y + hook1.size()[1]//2 <= SCREEN_SIZE[1]:
                    angle_radian = math.pi * hook1.angle() / 180
                    dx = hook1.size()[1] * math.sin(angle_radian)
                    dy = hook1.size()[1] * math.cos(angle_radian)
                    hook1_x += dx
                    hook1_y += dy
                    hook1.new_positon(hook1_x, hook1_y)
                    hook1.draw()
                    # print(hook1_x, hook1_y, hook1.size()[1], angle, math.sin(angle), math.cos(angle))
                else:
                    hook1_x, hook1_y = [60 + 150//2 - 100//2, 150 + 150]
                    hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
                    # print(hook1_x, hook1_y, hook1.size()[1], angle)
                
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                hook2_x, hook2_y = hook2.position()
                
                if 0 <= hook2_x + hook2.size()[0]//2 <= SCREEN_SIZE[0] and 0 <= hook2_y + hook2.size()[1]//2 <= SCREEN_SIZE[1]:
                    angle_radian = math.pi * hook2.angle() / 180
                    dx = hook2.size()[1] * math.sin(angle_radian)
                    dy = hook2.size()[1] * math.cos(angle_radian)
                    hook2_x += dx
                    hook2_y += dy
                    hook2.new_positon(hook2_x, hook2_y)
                    hook2.draw()
                    # print(hook2_x, hook2_y, hook1.size()[1], angle, math.sin(angle), math.cos(angle))
                else:
                    hook2_x, hook2_y = [1200 + 140//2 - 100//2, 160 + 140]
                    hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)
                    # print(hook2_x, hook2_y, hook1.size()[1], angle)

            #Ve hinh nen, nhan vat, can cau
            SCREEN.blit(game_background, (0, 0)) 
            character1.draw(balloon)
            character2.draw(balloon)
            character1.point(CHARACTER[self.__name1], (355, 70), DULL_YELLOW)
            character2.point(CHARACTER[self.__name2], (910, 70), DULL_YELLOW)
            hook1.draw()
            hook2.draw()

            #Ve vang va da
            for i in range(len(golds)):
                golds[i].draw()
            for i in range(len(stones)):
                stones[i].draw()
            for i in range(len(dementors)):
                dementors[i].draw()
            
                
            #Kiem tra moc cau co cham vao vat the nao hay khong
            gold_check_1, gold_index_1, plus_point_1 = hook1.miner(golds)
            if gold_check_1:
                plus_point = FONT.render(f'+ {plus_point_1}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (520, 70))
                point_1 += plus_point_1
                golds.pop(gold_index_1)
            stone_check_1, stone_index_1, plus_point_1 = hook1.miner(stones)
            if stone_check_1:
                plus_point = FONT.render(f'+ {plus_point_1}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (520, 70))
                point_1 += plus_point_1
                stones.pop(stone_index_1)
                hook1_x, hook1_y = [random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])]
                hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
            dementor_check_1, dementor_index_1, plus_point_1 = hook1.miner(dementors)
            if dementor_check_1:
                plus_point = FONT.render(f'- {plus_point_1}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (520, 70))
                point_1 -= plus_point_1
                dementors.pop(dementor_index_1)
                hook1_x, hook1_y = [random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])]
                hook1 = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)

            gold_check_2, gold_index_2, plus_point_2 = hook2.miner(golds)
            if gold_check_2:
                plus_point = FONT.render(f'+ {plus_point_2}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (1115, 70))
                point_2 += plus_point_2
                golds.pop(gold_index_2)
            stone_check_2, stone_index_2, plus_point_2 = hook2.miner(stones)
            if stone_check_2:
                plus_point = FONT.render(f'+ {plus_point_2}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (1115, 70))
                point_2 += plus_point_2
                stones.pop(stone_index_2)
                hook2_x, hook2_y = [random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])]
                hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)
            dementor_check_2, dementor_index_2, plus_point_2 = hook2.miner(dementors)
            if dementor_check_2:
                plus_point = FONT.render(f'- {plus_point_2}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (520, 70))
                point_2 -= plus_point_2
                dementors.pop(dementor_index_2)
                hook2_x, hook2_y = [random.randint(0, SCREEN_SIZE[0]), random.randint(0, SCREEN_SIZE[1])]
                hook2 = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), angle)


            hook_check, aa, plus_point_0 = hook1.miner([hook2])
            if hook_check:
                plus_point = FONT.render(f' {plus_point_0}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (520, 70))
                point_1 += plus_point_0
                
                plus_point = FONT.render(f' {plus_point_0}', True, DULL_YELLOW)
                SCREEN.blit(plus_point, (1115, 70))
                point_2 += plus_point_0
                
                hook1_x, hook1_y = [60 + 150//2 - 100//2, 150 + 150]
                hook1            = hook(imgae_of_hook1, (100, 75), (hook1_x, hook1_y), angle)
                hook2_x, hook2_y = [1200 + 140//2 - 100//2, 160 + 140]
                hook2            = hook(imgae_of_hook2, (100, 75), (hook2_x, hook2_y), -angle)


            #Tinh toan va in ra thoi gian tran dau   
            if not paused:
                elapsed_time    = (pygame.time.get_ticks() - start_sticks - total_paused_time) / 1000
                time_left       = GAME_TIME - elapsed_time
                if time_left <= 0:
                    run_game = False
            else:
                elapsed_time = (paused_start - start_sticks - total_paused_time) / 1000
            # print(f"Start sticks: {start_sticks}, Total paused time: {total_paused_time}")
            # print(f"Elapsed time: {elapsed_time}, GAME_TIME: {self.__GAME_TIME}")
            time_sticks = FONT.render(f'{int(time_left)}', True, DULL_YELLOW)
            SCREEN.blit(time_sticks, (715, 0))

            pygame.display.update()
            SCREEN.fill(BLACK)
            self.__clock.tick(60)

        if character1.point('', (0, 0), BLACK) > character2.point('', (0, 0), BLACK):
            # character1.draw_magic_beam(character2, GREEN, 7)
            return [character1], 1
        elif character1.point('', (0, 0), BLACK) < character2.point('', (0, 0), BLACK):
            # character2.draw_magic_beam(character1, RED, 7)
            return [character2], 2
        elif character1.point('', (0, 0), BLACK) == character2.point('', (0, 0), BLACK):
            return [character1, character2], 0

# help(character)
# help(hook)
# help(obj)
help(system)

game = system()
game.play_game()

pygame.quit()
exit()