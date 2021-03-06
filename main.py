import os, sys, random, pygame, game, display
from pygame.locals import *

#adjust this for difficulty
wordLength = 4
theGame = game.text(wordLength)

theGame.FirstTimeGenerate()

theDisplay = display.renderingClass(theGame)
theDisplay.FirstTimeGenerate()

#MAIN LOOP
while not theGame.getGameOver():
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
 		pygame.display.flip()
#this is triggered after the game ends
while True:
	for event in pygame.event.get():
		if (event.type == MOUSEBUTTONDOWN):
			sys.exit()
		else:
			pygame.event.clear()
