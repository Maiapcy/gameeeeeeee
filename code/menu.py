import pygame, sys
from button import Button
import csv

pygame.init()

SCREEN = pygame.display.set_mode((1200, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("BGMN.jpg")

Test = False

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("font.ttf", size)

def play():
    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(20).render("This is the PLAY screen.", True, "White")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(640, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(640, 460), 
                            text_input="BACK", font=get_font(20), base_color="White", hovering_color="Green")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    main_menu()
                    

        pygame.display.update()
    
    
def scoreboard():
    status = 'scoreboard'
    while True:
        SCOREBOARD_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("white")

        SCOREBOARD_TEXT = get_font(50).render("SCOREBOARD", True, "Black")
        SCOREBOARD_RECT = SCOREBOARD_TEXT.get_rect(center=(640, 100))
        SCREEN.blit(SCOREBOARD_TEXT, SCOREBOARD_RECT)

        SCOREBOARD_BACK = Button(image=None, pos=(640, 600), 
                            text_input="BACK", font=get_font(20), base_color="Black", hovering_color="gray")

        SCOREBOARD_BACK.changeColor(SCOREBOARD_MOUSE_POS)
        SCOREBOARD_BACK.update(SCREEN)

        with open("highscore.csv", 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for x, x1 in enumerate(reader):
                for y, y1 in enumerate(x1):
                    if x%2 == 0:

                    #player name
                        BOARD_TEXT = get_font(25).render(f"{y1}", True, "Black")
                        BOARD_RECT = BOARD_TEXT.get_rect(center=(450 +(y *370), 200 + ((x+1)* 35)))
                        SCREEN.blit(BOARD_TEXT, BOARD_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if SCOREBOARD_BACK.checkForInput(SCOREBOARD_MOUSE_POS):
                    status = 'menu'
        if status != 'scoreboard':
            break
        pygame.display.update()
    return status


def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))
        status = 'menu'

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(600, 320), 
                            text_input="PLAY", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        SCOREBOARD_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(600, 467), 
                            text_input="SCOREBOARD", font=get_font(20), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(600, 610), 
                            text_input="QUIT", font=get_font(20), base_color="#d7fcd4", hovering_color="White")

        

        for button in [PLAY_BUTTON, SCOREBOARD_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    status = 'overworld'
                if SCOREBOARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    status = 'scoreboard'
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        return status

# main_menu()