import os, sys, random, pygame
from pygame.locals import *
pygame.init()

class charObject(object):
	def __init__(self, _tmpText, _tmpPos):
		self.charGraphic = _tmpText
		self.charPos = _tmpPos

class renderingClass(object):
	def __init__(self, _textObject):
		#Screen
		self.screen = None
		self.background = None

		self.textObject = _textObject
		self.charObjectArray = []

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

		self.screen.blit(self.background, (0,0))
		pygame.display.flip()


	def createFontSurface(self):
		font = pygame.font.SysFont("Inconsolata", 24) #(12, 26)
			
		tmpY = 25
		

		for x in range(self.textObject.fullLength): #works!
			tmp = font.render(self.textObject.fullText[x], True, (10, 10, 10))

			tmpX = 50
		
			if (x == 204):
				tmpY = 25
			if (x >= 204): #408/2
				tmpX = 256

			if (x%12 == 0 and x != 0 and x != 204):
				print("yehyaernst")
				tmpY += 30
			tmpX += ((x%12)*12)
			
			tmppos = tmp.get_rect(x = tmpX, y = tmpY)

			self.charObjectArray.append(charObject(tmp, tmppos))
			



	def renderFontSurface(self):
		for x in range(self.textObject.fullLength):
			self.screen.blit(self.charObjectArray[x].charGraphic, self.charObjectArray[x].charPos)

	def highlightFontSurface(self, charIndex):
		inv = pygame.Surface(self.charObjectArray[charIndex].charGraphic.get_rect().size, pygame.SRCALPHA)
		inv.fill((255,255,255))
		inv.blit(self.charObjectArray[charIndex].charGraphic, (0,0), None, BLEND_RGB_SUB)
		return inv
				



	def getUnderMouse(self, location):
		for x in range(self.textObject.fullLength):
			if (self.charObjectArray[x].charPos.collidepoint(location[0], location[1])):
				print('oh fuku yes')
				self.screen.blit(self.highlightFontSurface(x), self.charObjectArray[x].charPos)
				pygame.display.flip()
				return
			print ('shit')



	def FirstTimeGenerate(self):
		self.createFontSurface()
		self.renderFontSurface()
		pygame.display.flip()