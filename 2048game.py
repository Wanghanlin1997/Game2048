import pygame,sys,time
import math
from pygame.locals import *
#from constants import *
from random import *


sizeofboard = 4
totalpoints = 0
defaultscore = 2
win = False

pygame.init()

surface = pygame.display.set_mode((400,500),0,32)
pygame.display.set_caption("Game_2048_HanlinWang ")

font = pygame.font.SysFont("monospace",40)
fontofscore = pygame.font.SysFont("monospace",30)
button_font = pygame.font.SysFont("monospace", 20) 

tileofmatrix = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
undomatrix = []
black = (0,0,0)
grey = (125, 125, 125)
red = (255,0,0)


colordict = {
    0:black,
    2:grey,
    4:grey,
    8:grey,
    16:grey,
    32:grey,
    64:grey,
    128:grey,
    256:grey,
    512:grey,
    1024:grey,
    2048:red
}
def getcolor(i):
    return colordict[i]

def draw_restart_button():
    button_color = grey  # Light gray color for button
    button_rect = pygame.Rect(250, 12, 100, 40) # Button position and size
    pygame.draw.rect(surface, button_color, button_rect)  # Draw button rectangle
    button_text = fontofscore.render("Restart", False, (255, 255, 255))  # Black text

    surface.blit(button_text, (button_rect.x + 10, button_rect.y + 5))  # Place text on button

def draw_win_button():
    button_color = (0, 255, 0)  # Green color for Win button
    button_rect = pygame.Rect(150, 200, 100, 40)  # Button position and size
    pygame.draw.rect(surface, button_color, button_rect)  # Draw button rectangle
    button_text = fontofscore.render("You Win!", False, (255, 255, 255))  # White text
    surface.blit(button_text, (button_rect.x + 10, button_rect.y + 5))  # Place text on button


def check_for_win():
    global win
    for row in tileofmatrix:
        if 2048 in row:  # Check if any tile has the value 8
            win = True
            break

def mainfunction(fromLoaded = False):
    global win
    if not fromLoaded:
        placerandomtile()
        placerandomtile()
    printmatrix()


    while True:

        draw_restart_button()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == MOUSEBUTTONDOWN:
                # Check if the mouse click is within the "Restart" button area
                mouse_x, mouse_y = event.pos
                if 250 <= mouse_x <= 350 and 12 <= mouse_y <= 52:
                    reset()  # Call reset() to restart the game when "Restart" button is clicked

            if win:
                gameover_win()
            if checkIfCanGo() and not win:
                if event.type == KEYDOWN: # Detects any key press
                    if isArrow(event.key):
                        print(
                            f"before rotate: {tileofmatrix}"
                        )
                        rotations = getrotations(event.key)
                        addToUndo() # copy the previous matrix named mat
                        for i in range(0,rotations):
                            rotatematrixclockwise()
                        print(f"after rotate: {tileofmatrix}")

                        if canmove():
                            movetiles()
                            print(f'after move: {tileofmatrix}')
                            mergetiles()
                            print(f'after merge: {tileofmatrix}')
                            placerandomtile()

                        for j in range(0,(4-rotations)%4):
                            rotatematrixclockwise()
                        print(f"after second rorate: {tileofmatrix}")
                        printmatrix()
                        check_for_win()

            if not checkIfCanGo():
                gameover_lose()

            if event.type == KEYDOWN:
                global sizeofboard

                if event.key == pygame.K_r:
                 
                    reset()
                if 50<event.key and 56 > event.key:
                    
                    sizeofboard = event.key - 48
                    reset()
                if event.key == pygame.K_s:
                   
                    savegame()
                elif event.key == pygame.K_l:
                    loadgame()
                    
                elif event.key == pygame.K_u:
                    undo()
                   
        pygame.display.update()



def canmove():
    for i in range(1, sizeofboard):
        for j in range(0, sizeofboard):
            # Check if the current tile has an empty space to the left
            if tileofmatrix[i-1][j] == 0 and tileofmatrix[i][j] > 0:
                return True 
            # Check if the current tile can merge with the tile to its left
            elif (tileofmatrix[i-1][j] == tileofmatrix[i][j]) and tileofmatrix[i-1][j] != 0:
                return True
    return False



def movetiles():
    for j in range(sizeofboard):  # Loop through each column
        for i in range(sizeofboard - 1):  # Loop through each row, except the last row
            while tileofmatrix[i][j] == 0 and sum(row[j] for row in tileofmatrix[i:]) > 0:
                # Shift all elements in the column up by one position
                for k in range(i, sizeofboard - 1):
                    tileofmatrix[k][j] = tileofmatrix[k + 1][j]
                tileofmatrix[sizeofboard - 1][j] = 0  # Set the bottom-most cell to 0 after shifting


def mergetiles():
    global totalpoints

    for j in range(sizeofboard):  # Loop through each column
        for i in range(sizeofboard - 1):  # Loop through each row except the last one
            # Check if the current tile can merge with the one below
            if tileofmatrix[i][j] == tileofmatrix[i + 1][j] and tileofmatrix[i][j] != 0:
                # Merge the tiles by doubling the current tile's value
                tileofmatrix[i][j] *= 2
                tileofmatrix[i + 1][j] = 0  # Set the tile below to 0 after merging
                totalpoints += tileofmatrix[i][j]  # Update the score with the merged tile's value
                movetiles()  # Shift tiles up after each merge to fill gaps

def placerandomtile():
    c = 0
    for i in range(0,sizeofboard):
        for j in range(0,sizeofboard):
            if tileofmatrix[i][j] == 0:
                c += 1
    
    k = floor(random() * sizeofboard* sizeofboard)

    while tileofmatrix[floor(k/sizeofboard)][k%sizeofboard] != 0:
        k = floor(random() * sizeofboard * sizeofboard)

    tileofmatrix[floor(k/sizeofboard)][k%sizeofboard] = 2



def floor(n):
    return int(n - (n % 1 ))  


def printmatrix():
    surface.fill(grey)
    global sizeofboard
    global totalpoints

    for i in range(0, sizeofboard):
        for j in range(0, sizeofboard):
            pygame.draw.rect(
                surface, 
                getcolor(tileofmatrix[i][j]), 
                (j * (400 / sizeofboard), i * (400 / sizeofboard) + 100, 400 / sizeofboard, 400 / sizeofboard)
            )
            label = font.render(str(tileofmatrix[i][j]), 1, (255, 255, 255))
            label2 = fontofscore.render("Score:" + str(totalpoints), 1, (255, 255, 255))
            surface.blit(label, (j * (400 / sizeofboard) + 30, i * (400 / sizeofboard) + 130))
            surface.blit(label2, (10, 20))


def checkIfCanGo():
    for i in range(sizeofboard): 
        for j in range(sizeofboard):
            if tileofmatrix[i][j] == 0:
                return True
    return False

def convertToLinearMatrix():

    mat = []
    for i in range(0,sizeofboard ** 2):
        mat.append(tileofmatrix[floor(i/sizeofboard)][i%sizeofboard])

    mat.append(totalpoints)
    return mat


def addToUndo():
    undomatrix.append(convertToLinearMatrix())   


def rotatematrixclockwise():
    for i in range(0, int(sizeofboard / 2)):
        for k in range(i, sizeofboard - i - 1):
            # Store the top element temporarily
            temp1 = tileofmatrix[i][k]

            # Move the left element to the top
            tileofmatrix[i][k] = tileofmatrix[sizeofboard - 1 - k][i]

            # Move the bottom element to the left
            tileofmatrix[sizeofboard - 1 - k][i] = tileofmatrix[sizeofboard - 1 - i][sizeofboard - 1 - k]

            # Move the right element to the bottom
            tileofmatrix[sizeofboard - 1 - i][sizeofboard - 1 - k] = tileofmatrix[k][sizeofboard - 1 - i]

            # Move the top element to the right
            tileofmatrix[k][sizeofboard - 1 - i] = temp1

def gameover_win():
    global totalpoints

    surface.fill(grey)

    label = font.render("you win",1,(255,255,255))
    label2 =font.render("score : "+str(totalpoints),1,(255,255,255))
    small_font = pygame.font.SysFont("monospace", 25)  
    label3 = small_font.render("press 'r' to restart",1,(255,255,255))

    surface.blit(label,(50,100))
    surface.blit(label2,(50,200))
    surface.blit(label3,(50,300))

def gameover_lose():
    global totalpoints

    surface.fill(grey)

    label = font.render("you lose",1,(255,255,255))
    label2 =font.render("score : "+str(totalpoints),1,(255,255,255))
    small_font = pygame.font.SysFont("monospace", 25)  
    label3 = small_font.render("press 'r' to restart",1,(255,255,255))

    surface.blit(label,(50,100))
    surface.blit(label2,(50,200))
    surface.blit(label3,(50,300))

def reset():
    global totalpoints, tileofmatrix, win
    win = False  
    totalpoints= 0
    surface.fill(black)
    tileofmatrix = [[0 for i in range(0,sizeofboard)] for j in range(0,sizeofboard) ]
    mainfunction()

def savegame():
    f = open("savedata","w")

    line1 = " ".join([str(tileofmatrix[floor(x/sizeofboard)][x%sizeofboard]) for x in range(0,sizeofboard ** 2)])
    f.write(line1+"\n")
    f.write(str(sizeofboard)+"\n")
    f.write(str(totalpoints))
    f.close


def undo():
    if len(undomatrix) > 0:
        mat = undomatrix.pop()

        for i in range(0,sizeofboard ** 2):
            tileofmatrix[floor(i/sizeofboard)][i%sizeofboard] = mat[i]
        global totalpoints
        totalpoints = mat[sizeofboard ** 2]

        printmatrix()

def loadgame():
    global totalpoints
    global sizeofboard
    global tilematrix

    f = open("savedata","r")

    mat = (f.readline()).split(' ',sizeofboard ** 2)
    sizeofboard = int(f.readline())
    totalpoints= int(f.readline())

    for i in range(0,sizeofboard ** 2):
        tileofmatrix[floor(i/sizeofboard)][i%sizeofboard] = int(mat[i])

    f.close()

    mainfunction(True)


def isArrow(k):
    return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT) or (k == pygame.K_w or k == pygame.K_s or k == pygame.K_a or k == pygame.K_d)

def getrotations(k):

    if k == pygame.K_UP or k == pygame.K_w:
        print('here')
        return 0
    elif k == pygame.K_LEFT or k ==  pygame.K_a:
        return 1
    elif k == pygame.K_DOWN or k == pygame.K_s:
        return 2 
    elif k == pygame.K_RIGHT or k == pygame.K_d:
        return 3
    
mainfunction()