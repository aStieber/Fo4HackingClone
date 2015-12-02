import os, sys, random, pygame, game, display
from pygame.locals import *
#this doesn't work yet






clock = pygame.time.Clock()





theGame = game.text(8)
theGame.textRunner()#calls the function that runs everything

theDisplay = display.renderingClass(theGame)#start here
theDisplay.FirstTimeGenerate()

# for x in theGame.lArray:
# 	print(x.index)

#MAIN LOOP
while True:
 	for event in pygame.event.get():
 		if (event.type == QUIT):
 			sys.exit()
 		elif (event.type == MOUSEMOTION):
 			theDisplay.runHighlights((event.pos[0], event.pos[1]))
 		elif (event.type == MOUSEBUTTONDOWN):
 			#if valid click
 			mousePos = theDisplay.getMouseLocation((event.pos[0], event.pos[1]))
 			if (mousePos != -1):
 				theGame.userClicked(mousePos)

 		else:
 			pygame.event.clear() #use this to clear the queue when the mouse leaves the window.
