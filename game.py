import pygame, sys, time
import math
from pygame.locals import *
from random import *

class game2048:
    def __init__(self):

        self.sizeofboard = 4
        self.totalpoints = 0
        self.defaultscore = 2
        self.win = False

        pygame.init()

        self.surface = pygame.display.set_mode((400, 500), 0, 32)
        pygame.display.set_caption("Game_2048_HanlinWang ")

        self.font = pygame.font.SysFont("monospace", 40)
        self.fontofscore = pygame.font.SysFont("monospace", 30)
        self.button_font = pygame.font.SysFont("monospace", 20) 

        self.tileofmatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.undomatrix = []
        self.black = (0, 0, 0)
        self.grey = (125, 125, 125)
        self.red = (255, 0, 0)

        self.colordict = {
            0: self.black,
            2: self.grey,
            4: self.grey,
            8: self.grey,
            16: self.grey,
            32: self.grey,
            64: self.grey,
            128: self.grey,
            256: self.grey,
            512: self.grey,
            1024: self.grey,
            2048: self.red
        }

    def getcolor(self, i):
        return self.colordict[i]

    def draw_restart_button(self):
        button_color = self.grey  # Light gray color for button
        button_rect = pygame.Rect(250, 12, 100, 40)  # Button position and size
        pygame.draw.rect(self.surface, button_color, button_rect)  # Draw button rectangle
        button_text = self.fontofscore.render("Restart", False, (255, 255, 255))  # Black text
        self.surface.blit(button_text, (button_rect.x + 10, button_rect.y + 5))  # Place text on button

    def draw_win_button(self):
        button_color = (0, 255, 0)  # Green color for Win button
        button_rect = pygame.Rect(150, 200, 100, 40)  # Button position and size
        pygame.draw.rect(self.surface, button_color, button_rect)  # Draw button rectangle
        button_text = self.fontofscore.render("You Win!", False, (255, 255, 255))  # White text
        self.surface.blit(button_text, (button_rect.x + 10, button_rect.y + 5))  # Place text on button

    def check_for_win(self):
        for row in self.tileofmatrix:
            if 2048 in row:  # Check if any tile has the value 2048
                self.win = True
                break

    def mainfunction(self, fromLoaded=False):
        if not fromLoaded:
            self.placerandomtile()
            self.placerandomtile()
        self.printmatrix()

        while True:
            self.draw_restart_button()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    # Check if the mouse click is within the "Restart" button area
                    mouse_x, mouse_y = event.pos
                    if 250 <= mouse_x <= 350 and 12 <= mouse_y <= 52:
                        self.reset()  # Call reset() to restart the game when "Restart" button is clicked

                if self.win:
                    self.gameover_win()
                if self.checkIfCanGo() and not self.win:
                    if event.type == KEYDOWN:  # Detects any key press
                        if self.isArrow(event.key):
                            print(f"before rotate: {self.tileofmatrix}")
                            rotations = self.getrotations(event.key)

                            for i in range(0, rotations):
                                self.rotatematrixclockwise()
                            print(f"after rotate: {self.tileofmatrix}")

                            if self.canmove():
                                self.movetiles()
                                print(f'after move: {self.tileofmatrix}')
                                self.mergetiles()
                                print(f'after merge: {self.tileofmatrix}')
                                self.placerandomtile()

                            for j in range(0, (4 - rotations) % 4):
                                self.rotatematrixclockwise()
                            print(f"after second rotate: {self.tileofmatrix}")
                            self.printmatrix()
                            self.check_for_win()

                if not self.checkIfCanGo():
                    self.gameover_lose()

                if event.type == KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()

            pygame.display.update()

    def canmove(self):
        for i in range(1, self.sizeofboard):
            for j in range(0, self.sizeofboard):
                # Check if the current tile has an empty space to the left
                if self.tileofmatrix[i - 1][j] == 0 and self.tileofmatrix[i][j] > 0:
                    return True 
                # Check if the current tile can merge with the tile to its left
                elif (self.tileofmatrix[i - 1][j] == self.tileofmatrix[i][j]) and self.tileofmatrix[i - 1][j] != 0:
                    return True
        return False

    def movetiles(self):
        for j in range(self.sizeofboard):  # Loop through each column
            for i in range(self.sizeofboard - 1):  # Loop through each row, except the last row
                while self.tileofmatrix[i][j] == 0 and sum(row[j] for row in self.tileofmatrix[i:]) > 0:
                    # Shift all elements in the column up by one position
                    for k in range(i, self.sizeofboard - 1):
                        self.tileofmatrix[k][j] = self.tileofmatrix[k + 1][j]
                    self.tileofmatrix[self.sizeofboard - 1][j] = 0  # Set the bottom-most cell to 0 after shifting

    def mergetiles(self):
        for j in range(self.sizeofboard):  # Loop through each column
            for i in range(self.sizeofboard - 1):  # Loop through each row except the last one
                # Check if the current tile can merge with the one below
                if self.tileofmatrix[i][j] == self.tileofmatrix[i + 1][j] and self.tileofmatrix[i][j] != 0:
                    # Merge the tiles by doubling the current tile's value
                    self.tileofmatrix[i][j] *= 2
                    self.tileofmatrix[i + 1][j] = 0  # Set the tile below to 0 after merging
                    self.totalpoints += self.tileofmatrix[i][j]  # Update the score with the merged tile's value
                    self.movetiles()  # Shift tiles up after each merge to fill gaps

    def placerandomtile(self):
        k = math.floor(random() * self.sizeofboard * self.sizeofboard)
        while self.tileofmatrix[math.floor(k / self.sizeofboard)][k % self.sizeofboard] != 0:
            k = math.floor(random() * self.sizeofboard * self.sizeofboard)
        self.tileofmatrix[math.floor(k / self.sizeofboard)][k % self.sizeofboard] = 2

    def printmatrix(self):
        self.surface.fill(self.grey)

        for i in range(0, self.sizeofboard):
            for j in range(0, self.sizeofboard):
                pygame.draw.rect(
                    self.surface, 
                    self.getcolor(self.tileofmatrix[i][j]), 
                    (j * (400 / self.sizeofboard), i * (400 / self.sizeofboard) + 100, 400 / self.sizeofboard, 400 / self.sizeofboard)
                )
                label = self.font.render(str(self.tileofmatrix[i][j]), 1, (255, 255, 255))
                label2 = self.fontofscore.render("Score:" + str(self.totalpoints), 1, (255, 255, 255))
                self.surface.blit(label, (j * (400 / self.sizeofboard) + 30, i * (400 / self.sizeofboard) + 130))
                self.surface.blit(label2, (10, 20))

    def checkIfCanGo(self):
        for i in range(self.sizeofboard): 
            for j in range(self.sizeofboard):
                if self.tileofmatrix[i][j] == 0:
                    return True
        return False

    def rotatematrixclockwise(self):
        for i in range(0, int(self.sizeofboard / 2)):
            for k in range(i, self.sizeofboard - i - 1):
                # Store the top element temporarily
                temp1 = self.tileofmatrix[i][k]

                # Move the left element to the top
                self.tileofmatrix[i][k] = self.tileofmatrix[self.sizeofboard - 1 - k][i]

                # Move the bottom element to the left
                self.tileofmatrix[self.sizeofboard - 1 - k][i] = self.tileofmatrix[self.sizeofboard - 1 - i][self.sizeofboard - 1 - k]

                # Move the right element to the bottom
                self.tileofmatrix[self.sizeofboard - 1 - i][self.sizeofboard - 1 - k] = self.tileofmatrix[k][self.sizeofboard - 1 - i]

                # Move the top element to the right
                self.tileofmatrix[k][self.sizeofboard - 1 - i] = temp1

    def gameover_win(self):
        self.surface.fill(self.grey)

        label = self.font.render("you win", 1, (255, 255, 255))
        label2 = self.font.render("score : " + str(self.totalpoints), 1, (255, 255, 255))
        small_font = pygame.font.SysFont("monospace", 25)  
        label3 = small_font.render("press 'r' to restart", 1, (255, 255, 255))

        self.surface.blit(label, (50, 100))
        self.surface.blit(label2, (50, 200))
        self.surface.blit(label3, (50, 300))

    def gameover_lose(self):
        self.surface.fill(self.grey)

        label = self.font.render("you lose", 1, (255, 255, 255))
        label2 = self.font.render("score : " + str(self.totalpoints), 1, (255, 255, 255))
        small_font = pygame.font.SysFont("monospace", 25)  
        label3 = small_font.render("press 'r' to restart", 1, (255, 255, 255))

        self.surface.blit(label, (50, 100))
        self.surface.blit(label2, (50, 200))
        self.surface.blit(label3, (50, 300))

    def reset(self):
        self.win = False  
        self.totalpoints = 0
        self.surface.fill(self.black)
        self.tileofmatrix = [[0 for i in range(0, self.sizeofboard)] for j in range(0, self.sizeofboard)]
        self.mainfunction()

    def isArrow(self, k):
        return (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT) or (k == pygame.K_w or k == pygame.K_s or k == pygame.K_a or k == pygame.K_d)

    def getrotations(self, k):
        if k == pygame.K_UP or k == pygame.K_w:
            return 0
        elif k == pygame.K_LEFT or k == pygame.K_a:
            return 1
        elif k == pygame.K_DOWN or k == pygame.K_s:
            return 2 
        elif k == pygame.K_RIGHT or k == pygame.K_d:
            return 3

if __name__ == "__main__":
    game = game2048()
    game.mainfunction()
