import os, sys, random, pygame
from pygame.locals import *
pygame.init()

class renderingClass(object):
	def __init__(self, _textObject):
		#Screen
		self.screen = None
		self.background = None

		self.textObject = _textObject
		self.fullTextSurface = None

		self.SubSurfaceArray = []

		self.initializeDisplay()

	def initializeDisplay(self):
		backgroundColor = (200, 200, 200)
		self.screen = pygame.display.set_mode((720, 540))
		#Display Title
		pygame.display.set_caption('fo4hacking')
		#create background, a of window size, then converts it for max blit speed reasons, then fills it 
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill(backgroundColor)

		self.fullTextSurface = pygame.Surface(((self.textObject.fullLength*12), 26)) #4896 by default, 12 is char width
		self.fullTextSurface.fill(backgroundColor)

		self.screen.blit(self.background, (0,0))
		pygame.display.flip()


	def createFontSurface(self):
		font = pygame.font.SysFont("Inconsolata", 24) #(12, 26)
		for x in range(self.textObject.fullLength): #works!
			tmp = font.render(self.textObject.fullText[x], True, (10, 10, 10))
			tmppos = tmp.get_rect(centerx=(6 + (12 * x)))
			self.fullTextSurface.blit(tmp, tmppos)

	def createSubSections(self):
		for x in range(34):
			tmpRect = pygame.Rect((144 * x, 0), (144, 26)) #Rect((left, top), (width, height)) 
			self.SubSurfaceArray.append(self.fullTextSurface.subsurface(tmpRect))

	def renderPuzzle(self):
		for x in range(34):
			if x < 17:
				tmppos = pygame.Rect((50, 25 + (x * 30)), (144, 26))
			else:
				tmppos = pygame.Rect((256, 25 + ((x-17) * 30)), (144, 26))
			self.screen.blit(self.SubSurfaceArray[x], tmppos)

	def getUnderMouse(self, location):
		print(location[0], ' ', location[1])



	def FirstTimeGenerate(self):
		self.createFontSurface()
		self.createSubSections()
		self.renderPuzzle()
		pygame.display.flip()