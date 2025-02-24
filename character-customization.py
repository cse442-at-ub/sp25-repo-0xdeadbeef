import pygame, sys
from pygame.locals import *


pygame.init() #initialize the pygame 

HEIGHT = 600
WIDTH = 1200
DISPLAY = pygame.display.set_mode((WIDTH,HEIGHT))
FPS = pygame.time.Clock()
FONT = pygame.font.SysFont("comicsans", 60)

#-----creates button class to make detection of mouse events easier
class Button():
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self):
        DISPLAY.blit(self.image, self.rect)

    def input_check(self, coordinates):
        if coordinates[0] in range(self.rect.left, self.rect.right) and coordinates[1] in range(self.rect.top, self.rect.bottom):
            return True

#creates the frame of the screen 
def create_screen(display, bg):
    display.blit(bg, (0,0))



def customization_screen(): 
    pygame.display.set_caption("customize")
    BG = pygame.image.load("Assets/customization-screen.png").convert()

     #-----Creates the background screen
    create_screen(DISPLAY, BG)

    #-----Loads Confirm button onto screen
    confirm_button = pygame.image.load("Assets/confirm-button.png")
    confirm_button = pygame.transform.scale(confirm_button, (100, 20))
    confirm_button_class = Button(confirm_button, 1100, 550)

    #-----Loads left and right buttons for changing hair color
    hair_left_button = pygame.image.load("Assets/left-arrow.png")
    hair_left_button = pygame.transform.scale(hair_left_button, (80,80))
    hair_left_button_class = Button(hair_left_button, 760, 90)

    hair_right_button = pygame.image.load("Assets/right-arrow.png")
    hair_right_button = pygame.transform.scale(hair_right_button, (80,80))
    hair_right_button_class = Button(hair_right_button, 1040, 95)

    #-----Loads left and right buttons for changing shirt color
    shirt_left_button = pygame.image.load("Assets/left-arrow.png")
    shirt_left_button = pygame.transform.scale(shirt_left_button, (80,80))
    shirt_left_button_class = Button(shirt_left_button, 760, 195)

    shirt_right_button = pygame.image.load("Assets/right-arrow.png")
    shirt_right_button = pygame.transform.scale(shirt_right_button, (80,80))
    shirt_right_button_class = Button(shirt_right_button, 1040, 200)

    #-----Loads left and right buttons for changing pants color
    pants_left_button = pygame.image.load("Assets/left-arrow.png")
    pants_left_button = pygame.transform.scale(pants_left_button, (80,80))
    pants_left_button_class = Button(pants_left_button, 760, 285)

    pants_right_button = pygame.image.load("Assets/right-arrow.png")
    pants_right_button = pygame.transform.scale(pants_right_button, (80,80))
    pants_right_button_class = Button(pants_right_button, 1040, 290)

    #-----Loads left and right buttons for changing skin color
    skin_left_button = pygame.image.load("Assets/left-arrow.png")
    skin_left_button = pygame.transform.scale(skin_left_button, (80,80))
    skin_left_button_class = Button(skin_left_button, 760, 375)

    skin_right_button = pygame.image.load("Assets/right-arrow.png")
    skin_right_button = pygame.transform.scale(skin_right_button, (80,80))
    skin_right_button_class = Button(skin_right_button, 1040, 380)


    #-----Loads hair color text onto screen
    hair_text = pygame.image.load("Assets/hair-color-text.png")
    hair_text = pygame.transform.scale(hair_text, (200,100))
    DISPLAY.blit(hair_text, (800, 50))

    #-----Loads shirt color text onto screen 
    shirt_text = pygame.image.load("Assets/shirt-color-text.png")
    shirt_text = pygame.transform.scale(shirt_text, (200,100))
    DISPLAY.blit(shirt_text, (800, 150))

    #-----Loads pants color text onto screen 
    pants_text = pygame.image.load("Assets/pants-color-text.png")
    pants_text = pygame.transform.scale(pants_text, (180, 80))
    DISPLAY.blit(pants_text, (810, 250))

    #-----Loads skin color text onto screen 
    skin_text = pygame.image.load("Assets/skin-color-text.png")
    skin_text = pygame.transform.scale(skin_text, (190, 90))
    DISPLAY.blit(skin_text, (800, 330))

    #-----Loads default character model onto screen


    #-----Loads the images for the different shirt, hair, pants, and skin color variants 
    shirt_images = [pygame.image.load(f"Assets/shirt_color/shirt_{i}.png") for i in range(3)]
    hair_images = [pygame.image.load(f"Assets/hair_color/hair_{i}.png") for i in range(3)]
    pants_images = [pygame.image.load(f"Assets/pants_color/pants_{i}.png") for i in range(3)]
    skin_images = [pygame.image.load(f"Assets/skin_color/skin_{i}.png") for i in range(2)]

    #-----Loads shoe onto character model
    shoe_image = pygame.image.load("Assets/shoes.png")
    shoe_image = pygame.transform.scale(shoe_image, (250, 250))
    DISPLAY.blit(shoe_image, (300, 250))

    #-----Tracks the index of customizables
    shirt_index = 0
    hair_index = 0
    pants_index = 0
    skin_index = 0

    #-----Loop fpr game events
    while True:
        
        #-----Updates the screen to include buttons
        hair_left_button_class.update()
        hair_right_button_class.update()
        shirt_left_button_class.update()
        shirt_right_button_class.update()
        pants_left_button_class.update()
        pants_right_button_class.update()
        skin_left_button_class.update()
        skin_right_button_class.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if confirm_button_class.input_check(pygame.mouse.get_pos()) == True:
                    print("Pressed")
                
                #-----Check if the left arrow button for hair customization was clicked
                if (hair_left_button_class.input_check(pygame.mouse.get_pos()) == True):
                    print ("left hair button")
                    if (hair_index == 0):
                        hair_index = len(hair_images)-1
                    else:
                        hair_index = (hair_index-1)
                #-----Check if the right arrow button for hair customization was clicked 
                if (hair_right_button_class.input_check(pygame.mouse.get_pos()) == True):
                    print ("right hair button")
                    if (hair_index == len(hair_images)-1):
                        hair_index = 0
                    else:
                        hair_index = (hair_index+1)
                #-----Check if the left arrow button for skin customization was clicked
                if (skin_left_button_class.input_check(pygame.mouse.get_pos()) == True):
                    if (skin_index == 0):
                        skin_index = len(skin_images)-1
                    else:
                        skin_index = (skin_index-1)
                #-----Check if the right arrow button for skin customization was clicked
                if (skin_right_button_class.input_check(pygame.mouse.get_pos()) == True):
                    if (skin_index == len(skin_images)-1):
                        skin_index = 0
                    else:
                        skin_index = (skin_index+1)

                #-----Check if the left arrow button for shirt customization was clicked
                if (shirt_left_button_class.input_check(pygame.mouse.get_pos()) == True):
                    if (shirt_index == 0):
                        shirt_index = len(shirt_images)-1
                    else:
                        shirt_index = (shirt_index-1)
                #-----Check if the right arrow button for shirt customization was clicked
                if (shirt_right_button_class.input_check(pygame.mouse.get_pos()) == True):
                    if(shirt_index == len(shirt_images)-1):
                        shirt_index = 0
                    else:
                        shirt_index = (shirt_index+1)
                #-----Check if the left arrow button for pants customization was clicked
                if (pants_left_button_class.input_check(pygame.mouse.get_pos()) == True):
                    if (pants_index == 0):
                        pants_index = len(pants_images)-1
                    else:
                        pants_index = (pants_index-1)
                #-----Check if the right arrow button for pants customization was clicked
                if (pants_right_button_class.input_check(pygame.mouse.get_pos()) == True):
                    if(pants_index == len(pants_images)-1):
                        pants_index = 0
                    else:
                        pants_index = (pants_index+1)




        # create_screen(DISPLAY, BG)

        FPS.tick(60)
        pygame.display.update()
        confirm_button_class.update()

        #-----Updates the screen to include buttons
        # hair_left_button_class.update()
        # hair_right_button_class.update()
        # shirt_left_button_class.update()
        # shirt_right_button_class.update()
        # pants_left_button_class.update()
        # pants_right_button_class.update()
        # skin_left_button_class.update()
        # skin_right_button_class.update()

        #-----Make the desired character customizations appear
        shirt_size = pygame.transform.scale(shirt_images[shirt_index], (250,250))
        hair_size = pygame.transform.scale(hair_images[hair_index], (250,250))
        pants_size = pygame.transform.scale(pants_images[pants_index], (250,250))
        skin_size = pygame.transform.scale(skin_images[skin_index], (250,250))

        DISPLAY.blit(hair_size, (300, 266))
        DISPLAY.blit(skin_size, (300, 260))
        DISPLAY.blit(shirt_size, (300, 250))
        DISPLAY.blit(pants_size, (300, 250))

        # DISPLAY.blit(shirt_images[shirt_index], (400, 500))
        # DISPLAY.blit(hair_images[hair_index], (400, 400) )
        # DISPLAY.blit(pants_images[pants_index], (400, 600))


        #creates buttons
        # confirm_button = pygame.image.load("Assets/confirm-button.png")
        # confirm_button = pygame.transform.scale(confirm_button, (400, 150))
        # button = Button(confirm_button, 400, 300)

        MOUSE_POSITION = pygame.mouse.get_pos()
        # pygame.display.update()

        pygame.display.flip()




if __name__ == "__main__":
    customization_screen()

        

