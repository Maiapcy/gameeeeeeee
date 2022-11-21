import pygame, sys
from setting import * 
from level import Level
from game_data import level_0
from overworld import Overworld
from ui import UI
# from menu import *
import menu
import csv 
from pathlib import Path
BG = pygame.image.load("BGYAY.jpg")
highscore_file = 'highscore.csv'
scoreboard = []
if Path(highscore_file).is_file() == False:
    tmp_list1 = ['xxx', 0]
    tmp_list2 = ['xxx', 0]
    tmp_list3 = ['xxx', 0]
    tmp_list4 = ['xxx', 0]
    tmp_list5 = ['xxx', 0]
    tmp_list6 = ['xxx', 0]
    tmp_list7 = ['xxx', 0]
    tmp_list8 = ['xxx', 0]
    tmp_list9 = ['xxx', 0]
    tmp_list10 = ['xxx', 0]
    scoreboard.append(tmp_list1)
    scoreboard.append(tmp_list2)
    scoreboard.append(tmp_list3)
    scoreboard.append(tmp_list4)
    scoreboard.append(tmp_list5)
    scoreboard.append(tmp_list6)
    scoreboard.append(tmp_list7)
    scoreboard.append(tmp_list8)
    scoreboard.append(tmp_list9)
    scoreboard.append(tmp_list10)

    with open("highscore.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        for x in range(10):
            writer.writerow(scoreboard[x])
else:
    with open("highscore.csv", 'r', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for x in reader:
            scoreboard.append(x)

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("./assets/font.ttf", size)


class Game:
    def __init__(self):

        # game attributes
        self.max_level = 0
        self.max_health = 100
        self.cur_health = 100
        self.coins = 0
        self.score = 0

        #audio
        self.level_bg_music = pygame.mixer.Sound('./audio/London_Boy.mp3')
        self.overworld_bg_music = pygame.mixer.Sound('./audio/Cruel_Summer.mp3')
        
        # overworld creation
        self.overworld = Overworld(0,self.max_level,screen,self.create_level)
        self.status = 'menu'
        self.overworld_bg_music.play(loops = -1)
        self.overworld_bg_music.set_volume(0.5)

        #user interface
        self.ui = UI(screen)
    

        

    def create_level(self,current_level):
        self.level = Level(current_level,screen,self.create_overworld,self.change_coins,self.change_health)
        self.status = 'level'
        self.overworld_bg_music.stop()
        self.level_bg_music.play(loops = -1)

    def create_overworld(self,current_level,new_max_level):
        if new_max_level > self.max_level:
            self.max_level = new_max_level
        self.overworld = Overworld(current_level,self.max_level,screen,self.create_level)
        self.status = 'overworld'
        self.overworld_bg_music.play(loops = -1)
        self.level_bg_music.stop()

    def change_coins(self,amount):
        self.coins += amount   

    def change_health(self,amount):
        self.cur_health += amount

    def check_game_over(self):
        if self.cur_health <= 0 or self.max_level == 6:
            self.cur_health = 100
            self.score = self.coins

            #self.overworld = Overworld(0,self.max_level,screen,self.create_level)
            self.level_bg_music.stop()
            self.status = 'gameover'
            self.overworld_bg_music.play(loops = -1)

    def gameover(self):
        base_font = pygame.font.Font(None,32)
        user_text = ''

        input_rect = pygame.Rect(640,550,140,32)
        color_active = pygame.Color('White')
        color_passive = pygame.Color('White')
        color = color_passive

        active = False
        
        eiei = True
        while eiei:
            for event in pygame.event.get():
                keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_rect.collidepoint(event.pos):
                        active = True
                    else:
                        active = False
                
                if event.type == pygame.KEYDOWN:
                    if active == True:
                        if event.key == pygame.K_BACKSPACE:
                            user_text = user_text[:-1]
                        else:
                            user_text += event.unicode
        
                if keys[pygame.K_1]:
                    eiei = False
                    name = []
                    text = user_text.strip("1")
                    name.append(text) 
                    name.append(self.score)
                    scoreboard.append(name)
                    for x in range(10):
                        if self.score > int(scoreboard[x][1]):
                            tmp = 1
                            scoreboard.remove(scoreboard[9])
                            while 9 - tmp >= x:
                                scoreboard[9 - tmp + 1] = scoreboard[9 - tmp]
                                tmp += 1
                                print(scoreboard)
                            scoreboard[x] = name
                            print(scoreboard)
                            break

                    with open("highscore.csv", 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile, delimiter=',')
                        for x in range(10):
                            writer.writerow(scoreboard[x]) 
                    
                    self.coins = 0
                    self.max_level = 0
                    self.overworld = Overworld(0,self.max_level,screen,self.create_level) #another level 
                    self.status = 'menu'
                    

            screen.blit(BG,(0,0))

            if active == True:
                color = color_active
            else:
                color = color_passive
            pygame.draw.rect(screen,color,input_rect,2)

            #ydagj
            GOVER_TEXT = get_font(40).render("You did a great job!", True, "white")
            GOVER_RECT = GOVER_TEXT.get_rect(center=(640, 260))
            screen.blit(GOVER_TEXT, GOVER_RECT)
            
            #score
            GOVER_TEXT = get_font(45).render("score : " + str(self.score), True, "white")
            GOVER_RECT = GOVER_TEXT.get_rect(center=(640, 360))
            screen.blit(GOVER_TEXT, GOVER_RECT)
            
            #name
            PLAYER_TEXT = get_font(25).render("your name: ", True, "white")
            PLAYER_RECT = PLAYER_TEXT.get_rect(center=(450, 575))
            screen.blit(PLAYER_TEXT, PLAYER_RECT)


            text_surface = base_font.render(user_text,True,(255,255,255))
            screen.blit(text_surface,(input_rect.x+ 5,input_rect.y+5))
            input_rect.w = max(100,text_surface.get_width()+10)
            pygame.display.flip()
            clock.tick(60)
            if self.status != 'gameover':
                break
            pygame.display.update()

    def run(self):
        if self.status == 'menu':
            self.status = menu.main_menu()
        elif self.status == 'scoreboard':
            self.status = menu.scoreboard()
        elif self.status == 'gameover':
            self.gameover()
        elif self.status == 'overworld':
            self.overworld.run()
        else:
            self.level.run()
            self.ui.show_health(self.cur_health,self.max_health)
            self.ui.show_coins(self.coins)
            self.check_game_over()



# Pygame setup
pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))



clock = pygame.time.Clock()
pygame.display.set_caption('Corgi eats Bacon')
icon = pygame.image.load('iconcorgii.png')
pygame.display.set_icon(icon)
game = Game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('grey')
    game.run()  
    
    pygame.display.update()
    clock.tick(60)