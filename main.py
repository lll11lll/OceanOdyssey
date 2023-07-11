import pygame
import random
from trash import Trash
from fish import Fish
from shark import Shark
from bullets import Bullet
from bulletHit import BulletHit
from button import Button

pygame.init()

# Settings 
WIDTH = 1400
HEIGHT = 650
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 60
clock = pygame.time.Clock()
pygame.display.set_caption("Floppy Fish")
pixelFont = pygame.font.Font('font/Pixeltype.ttf', 36)
# //

# Game state
MENU = "menu"
RUNNING = "running"
PAUSED = "paused"
gameState = MENU
menuOptions = ["Start", "Settings", "Quit"]

buttonGroup = pygame.sprite.Group()



def drawMenu():
    global gameState
    activeButtons = pygame.sprite.Group()
    for i, option in enumerate(menuOptions):
        button = Button(WIDTH//2 - 150 , 350 + i * 100, 300, 80, option, gameState)
        buttonGroup.add(button)
        activeButtons.add(button)
    for button in buttonGroup:
        #button.draw(WIN)
        mousePos = pygame.mouse.get_pos()
        if button.collisionRect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0]:
                button.handleClick(mousePos)
                gameState = button.gameState
                
            else:
                button.handleHover(mousePos)
        else:
            button.handleDefault()
        button.draw(WIN)
        for button in buttonGroup:
            if button not in activeButtons:
                button.kill()
        activeButtons.empty()
        



# Background Setup 
background = pygame.transform.scale(pygame.image.load('spriteSheets/underwater.png'), (WIDTH, 700))
menuBackground = pygame.transform.scale(pygame.image.load('spriteSheets/Back.png'), (WIDTH, HEIGHT))
scrollSpeed = 2
bgX = 0

def updateBG():
    global bgX
    bgX -= scrollSpeed
    if bgX <= -WIDTH:
        bgX = 0
    return bgX
# //

# Navbar setup
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
navbarWidth = 1400
navbarHeight = 75
navbarFrame = pygame.transform.scale(pygame.image.load('spriteSheets/frame.png'), (navbarWidth + 10 , navbarHeight ))
navbarRect = pygame.Rect(0, 0, navbarWidth , navbarHeight - 10)
navbarFont = pixelFont
navbarColor = (100, 100, 100)
life = 3
score = 0
distance = 0 


def displayNavBar(life, score):
    lifeText = navbarFont.render(f'Lives: {life}', True, WHITE)
    distanceText = navbarFont.render(f'Distance:  {distance} m', True, WHITE)
    scoreText = navbarFont.render(f'Score: {score}', True, WHITE)

    pygame.draw.rect(WIN, navbarColor, navbarRect)
    WIN.blit(navbarFrame, (-10, 0))
    
    alpha = 128 

    lifeRect = pygame.Surface((lifeText.get_width() + 10, lifeText.get_height() + 15), pygame.SRCALPHA)
    lifeRect.fill((0, 0, 0, alpha))

    timerRect = pygame.Surface((distanceText.get_width() + 20, distanceText.get_height() + 15), pygame.SRCALPHA)
    timerRect.fill((0, 0, 0, alpha))

    scoreRect = pygame.Surface((scoreText.get_width() + 10, scoreText.get_height() + 15), pygame.SRCALPHA)
    scoreRect.fill((0, 0, 0, alpha))
    
    WIN.blit(lifeRect, (195, 20))
    WIN.blit(timerRect, (595, 20))
    WIN.blit(scoreRect, (995, 20))

    WIN.blit(lifeText, (200, 30))
    WIN.blit(distanceText, (600, 30))
    WIN.blit(scoreText, (1000, 30))

# Trash Group
trashGroup = pygame.sprite.Group()
maxTrashCount = 38
trashList = ['spriteSheets/trash/beer.xcf', 'spriteSheets/trash/bottle.xcf', 'spriteSheets/trash/box.png', 
               'spriteSheets/trash/cup.xcf', 'spriteSheets/trash/jar.xcf', 'spriteSheets/trash/largeCan.xcf', 
               'spriteSheets/trash/laundry.xcf', 'spriteSheets/trash/milk.xcf', 'spriteSheets/trash/mug.xcf', 
               'spriteSheets/trash/news.xcf', 'spriteSheets/trash/pizzabox.xcf', 'spriteSheets/trash/smallCan.xcf', 
               'spriteSheets/trash/sodaCan.xcf', 'spriteSheets/trash/sprayCan.xcf', 'spriteSheets/trash/waterbottle.xcf' ]

def spawnTrash():
    if len(trashGroup) < maxTrashCount: 
        for trashNum in range(maxTrashCount):
            randomX = random.randrange(1202, WIDTH+WIDTH)
            randomY = random.randrange(100, 465)
            randomNum = random.randint(0, len(trashList) - 1)

          # Determine the width and height based on the randomNum
            if randomNum in [0, 1, 11, 12, 13, 14]:
                width = 25
                height = 35
                value = 50
            elif randomNum == 8:
                width = 20
                height = 20
                value = 25
            elif randomNum in [3, 4, 5]:
                width = 30
                height = 40
                value = 75
            elif randomNum in [2, 6, 7, 8, 9, 10]:
                width = 60
                height = 55
                value = 100
            else:
                width = 35
                height = 35
                value = 50
            newTrash = Trash(trashList[randomNum], randomX, randomY, width, height, value)
            
            collidingTrash = pygame.sprite.spritecollide(newTrash, trashGroup, False)
            if collidingTrash:
                randomX = random.randrange(1202, WIDTH + 700)
                randomY = random.randrange(100, 685)
                newTrash.rect.center = [randomX, randomY]

            trashGroup.add(newTrash)

def updateTrash(trashList):
    for trash in trashList:
        trash.update()
bulletGroup = pygame.sprite.Group()
bulletHitGroup = pygame.sprite.Group()
# Fish/Player
myFish = Fish(250, 200, 65, 65, trashGroup, bulletGroup, bulletHitGroup, life, score)
# Shark 
myShark = Shark(1700, 300, 160, 80, trashGroup)

def dropShadowText(screen, text, size, x, y, color, dropColor, font='font/Pixeltype.ttf'):
    # how much 'shadow distance' is best?
    dropShadowOffset = 3 + (size // 15)
    textFont = pygame.font.Font(font, size)
    # make the drop-shadow
    textBitmap = textFont.render(text, True, dropColor)
    screen.blit(textBitmap, (x+dropShadowOffset, y+dropShadowOffset) )
    # make the overlay text
    textBitmap = textFont.render(text, True, color)
    screen.blit(textBitmap, (x, y) )

def drawWindow():
    global distance
    if gameState == MENU:
        updateBG()

        WIN.blit(menuBackground, (bgX, 0))
        WIN.blit(menuBackground, (bgX+WIDTH, 0))
        dropShadowText(WIN, "Ocean", 108, WIDTH//2 - 200, 100, (5, 195, 221), (22, 27, 99) )
        dropShadowText(WIN, "Odyssey", 108, WIDTH//2 - 125, 200, (5, 195, 221), (22, 27, 99) )
        drawMenu()
        
    elif gameState == RUNNING:
        
        spawnTrash()
        updateBG()
        myFish.update()
        updateTrash(trashGroup)
        myShark.update()
        bulletGroup.update()
        bulletHitGroup.update()
        WIN.blit(background, (bgX, 0))
        WIN.blit(background, (bgX + WIDTH, 0))
        myFish.draw(WIN)
        trashGroup.draw(WIN)
        myShark.draw(WIN)
        bulletGroup.draw(WIN)
        bulletHitGroup.draw(WIN)
        life = myFish.life
        score = myFish.score
        distance = int(pygame.time.get_ticks() / 1000)
        displayNavBar(life, score)
        if life <= 0:
           pygame.quit() 
    pygame.display.update()
    
def main():
    run = True
    while run:
        clock.tick(FPS)
        if gameState == MENU:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
        if gameState == RUNNING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        drawWindow()
main()