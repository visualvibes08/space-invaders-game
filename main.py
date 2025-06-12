import pygame
import random
import math
from scripts.loader import load_img,load_sound,play_sfx

# initialize pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Create clock object for controlling frame rate
clock = pygame.time.Clock()
FPS = 60  # Set desired frame rate

# screen Title and icon
pygame.display.set_caption("Space Invaders")
icon=load_img("ufo.png")
pygame.display.set_icon(icon) 
    
# background
background=load_img("background.png")

# background music
load_sound('background.wav')
pygame.mixer.music.play(-1) 


# player
playerIMG=load_img("player.png")
playerX=370
playerY=480
player_change=0

# draw enemy
enemyImg=[]
enemyX=[]
enemyY=[]

n=6
enemyY_change=[]
enemyX_change=[]
speed=4
for i in range (0,n):    
    enemyImg.append(load_img("enemy.png"))
    enemyX.append(random.randint(0,800))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(speed)
    enemyY_change.append(40)

# Bullet
bulletImg=load_img("bullet.png")
bulletX=0
bulletY=480
bulletX_change=0
bulletY_change=12
bullet_state="ready"

# socre
score=0
score_list=[]
font=pygame.font.Font('freesansbold.ttf',32)
textX=10
textY=10
global high_score
high_score=0
global bool_new_score

# Game over
over_font=pygame.font.Font('freesansbold.ttf',68)
more_font=pygame.font.SysFont('Times New Roman', 32, bold=True)
global game_over_bool
global play

# restart button
button=load_img('restart.png')

game_over_bool=False
play=False
def Enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

# draw player 
def Player(x,y):
    screen.blit(playerIMG,(playerX,playerY))


def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x+16,y+16))

def isCollision(enemyX,enemyY,bulletX,bulletY):
     distance=math.sqrt(math.pow((enemyX-bulletX),2)+math.pow((enemyY-bulletY),2))
     if distance<=27:
          return True
     
def show_score(x,y):
    
    score1=font.render(f"Score : {score} ",True,(255,255,255))
    screen.blit(score1,(x,y))

def new_high_score():
    new_text=over_font.render('New HIGH score!!',True,(255,255,255))
    screen.blit(new_text,(120,100))

def Game_over_text():
    over_text=over_font.render('Game Over',True,(255,255,255))
    screen.blit(over_text,(200,250))
    screen.blit(button,(300,320))
    
    try:
        with open('scripts/Data.txt', 'r') as f:
            high_score = int(f.read().strip())
    except FileNotFoundError:
            high_score = 0  

    if score > high_score:        
        with open('scripts/Data.txt', 'w') as f:
            f.write(str(score))
    
    if score==high_score:
        new_high_score()
    
    display_high_score=more_font.render(f'High Score : {high_score}',True,(255,255,255))
    screen.blit(display_high_score,(500,450))
    current_score=more_font.render(f'Score : {score}',True,(255,255,255))
    screen.blit(current_score,(100,450))

# open window
screen=pygame.display.set_mode((800,600))

# game Loop
running=True
# Pre-calculate some values outside the loop
PLAYER_BOUNDARY_LEFT = 0
PLAYER_BOUNDARY_RIGHT = 736
ENEMY_BOUNDARY_LEFT = 5
ENEMY_BOUNDARY_RIGHT = 736
BULLET_RESET_Y = 480

while running:
    # Control frame rate
    clock.tick(FPS)

    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    if not game_over_bool:

        for event in pygame.event.get():     
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RIGHT:
                    player_change = 5
                if event.key==pygame.K_LEFT:
                    player_change = -5
                if event.key==pygame.K_SPACE:
                    if bullet_state=="ready":
                        fire_bullet(playerX,bulletY)
                        bulletX=playerX
                        play_sfx("laser.wav")
            if event.type==pygame.KEYUP :
                if event.key==pygame.K_RIGHT or pygame.K_LEFT:
                    player_change=0

        playerX+=player_change

        # Optimize boundary checks using pre-calculated values
        if playerX <= PLAYER_BOUNDARY_LEFT:
                playerX = PLAYER_BOUNDARY_LEFT
        elif playerX >= PLAYER_BOUNDARY_RIGHT:
            playerX = PLAYER_BOUNDARY_RIGHT    

        for i in range (n):
            # game over
            if enemyY[i]>440:
                game_over_bool=True
                play = True
                for j in range(n):
                    enemyY[j]=2000

            enemyX[i]+=enemyX_change[i]
            if enemyX[i] <= ENEMY_BOUNDARY_LEFT:
                    enemyX_change[i] = speed
                    enemyY[i]+=enemyY_change[i]
            elif enemyX[i] >= ENEMY_BOUNDARY_RIGHT:
                enemyX[i]= ENEMY_BOUNDARY_RIGHT
                enemyX_change[i]=-speed
                enemyY[i]+=enemyY_change[i]

        # Bullet movement
        if bullet_state == "fire":
             fire_bullet(bulletX,bulletY)
             bulletY+= -bulletY_change
        if bulletY<=0:
             bulletY=BULLET_RESET_Y
             bullet_state="ready"

        # collison detection
        for i in range(n):
            collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
            if collision:
                bulletY=BULLET_RESET_Y
                bullet_state="ready"
                score+=1
                play_sfx("explosion.wav")            
                enemyX[i]=random.randint(0,800)
                enemyY[i]=random.randint(50,150)
            Enemy(enemyX[i],enemyY[i],i)

        Player(playerX,playerY)
        show_score(textX,textY)
    else:
        for event in pygame.event.get():   
            if event.type==pygame.QUIT:
                running=False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_x, pos_y = pygame.mouse.get_pos()
                if 300<pos_x<500 and 320<pos_y<398:
                    running=True
                    game_over_bool=False
                    pos_x,pos_y=0,0
                    enemyX.clear()
                    enemyY.clear()
                    score=0
                    load_sound('background.wav')
                    pygame.mixer.music.play(-1) 
                    for i in range (0,6): 
                           
                        enemyImg.append(load_img("enemy.png"))
                        enemyX.append(random.randint(0,800))
                        enemyY.append(random.randint(50,150))
                        enemyX_change.append(2)
                        enemyY_change.append(40)
        
        if play:
            pygame.mixer.music.stop()
            play_sfx('gameover.mp3')
            play = False
        Game_over_text()         
        if score>high_score:
            high_score=score

    pygame.display.update()

