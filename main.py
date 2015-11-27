import os, sys, random, pygame, game, display
from pygame.locals import *


#https://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html


clock = pygame.time.Clock()





puzzleText = game.text(8)
puzzleText.textRunner()#calls the function that runs everything

theDisplay = display.renderingClass(puzzleText)#start here
theDisplay.FirstTimeGenerate()

#MAIN LOOP
while True:
 	for event in pygame.event.get():
 		if (event.type == QUIT):
 			sys.exit()
 		if (event.type == MOUSEMOTION):
 			theDisplay.getUnderMouse((event.pos[0], event.pos[1]))




		#pygame.event.clear() #use this to clear the queue when the mouse leaves the window.