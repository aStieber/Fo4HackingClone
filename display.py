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

		#game.text object
		self.textObject = _textObject
		#assigning this display object to game.text.displayObject
		_textObject.displayObject = self

		self.charObjectArray = []
		self.consoleArray = []

		self.backgroundColor = (200, 200, 200)
		#for mouseover detection
		self.prevMouseOver = 0

		self.font = pygame.font.SysFont("Inconsolata", 24) #(12, 26)

		self.initializeDisplay()

	def initializeDisplay(self):
		self.screen = pygame.display.set_mode((720, 540))
		#Display Title
		pygame.display.set_caption('fo4hacking')
		#create background, a of window size, then converts it for max blit speed reasons, then fills it 
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill(self.backgroundColor)

		self.screen.blit(self.background, (0,0))
		pygame.display.flip()

#this function builds charObjectArray[]
	def createFontSurface(self):
		self.charObjectArray = []
		
			
		tmpY = 25
		for x in range(self.textObject.fullLength): #works!
			tmp = self.font.render(self.textObject.fullText[x], True, (10, 10, 10), self.backgroundColor)

			tmpX = 50
		
			if (x == 204):
				tmpY = 25
			if (x >= 204): #408/2
				tmpX = 256

			if (x%12 == 0 and x != 0 and x != 204):
				tmpY += 30
			tmpX += ((x%12)*12)
			
			tmppos = tmp.get_rect(x = tmpX, y = tmpY)

			self.charObjectArray.append(charObject(tmp, tmppos))
			
	def renderFontSurface(self):
		for x in range(self.textObject.fullLength):
			self.screen.blit(self.charObjectArray[x].charGraphic, self.charObjectArray[x].charPos)

	def highlightFontSurface(self, charIndex):
			inv = pygame.Surface((12, 26), pygame.SRCALPHA)
			inv.fill((255,255,255))
			inv.blit(self.charObjectArray[charIndex].charGraphic, (0,0), None, BLEND_RGB_SUB)
			return inv

	def getMouseLocation(self, _mousePos):
			for x in range(self.textObject.fullLength):
				if (self.charObjectArray[x].charPos.collidepoint(_mousePos[0], _mousePos[1])):
					return(x)
			return(-1)

	#returns whether the selected char is part of a word, a brace, or nothing (-1)
	def isInPhrase(self, sequenceObject, mouseLocation):
		x = sequenceObject
			#if word
		if x.isWord == True:
			if (x.index <= mouseLocation <= (x.index + x.phraseLength - 1)):
	 			return('word')
		#if brace sequence
		else:
			if (x.index == mouseLocation):
				return('brace')
		return -1

	def runHighlights(self, _mousePos):
		mouseLocation = self.getMouseLocation(_mousePos)

		#unhighlights when mouse isn't on screen
		if (mouseLocation == -1):
			self.renderFontSurface()
			pygame.display.flip()
			return

		#unhighlight previous mouseover
		self.screen.blit(self.charObjectArray[self.prevMouseOver].charGraphic, self.charObjectArray[self.prevMouseOver].charPos)

		multiHighlight = False
		#check to see if given char is index of a Sequence
		#Words are highlighted when any of their letters are moused over
		#brace strings require the index of the phrase to be moused over
		for y in self.textObject.lArray:
			iiP = self.isInPhrase(y, mouseLocation)
			if (iiP == 'word'):		
				multiHighlight = True
				self.renderFontSurface()
				for z in range(y.phraseLength):
					#blit an inverted version of the font to each char in the word
					self.screen.blit(self.highlightFontSurface(y.index+z), self.charObjectArray[y.index+z].charPos)
		#if brace sequence
			elif (iiP == 'brace'):	
				multiHighlight = True
				self.renderFontSurface()
				for z in range(y.phraseLength):
					#blit an inverted version of the font to each char in the brace phrase
					self.screen.blit(self.highlightFontSurface(y.index+z), self.charObjectArray[y.index+z].charPos)
		if not multiHighlight:
			self.renderFontSurface()


		self.screen.blit(self.highlightFontSurface(mouseLocation), self.charObjectArray[mouseLocation].charPos)
		self.prevMouseOver = mouseLocation
		return


	def ConsoleRender(self, upperLine=None, lowerLine=None): #450, 490
		consoleBG = pygame.Surface((260, 480))
		consoleBG.fill(self.backgroundColor)
		self.screen.blit(consoleBG, (450, 50))

		self.consoleArray.insert(0, upperLine)
		self.consoleArray.insert(0, lowerLine)

		consoleLength = len(self.consoleArray)
		for x in range(consoleLength):
			tmp = self.font.render(self.consoleArray[x], True, (10, 10, 10), self.backgroundColor)
			consoleBG.blit(tmp, (0, 450 - (30 * x)))
		self.screen.blit(consoleBG, (450, 50))
		

	def renderTries(self):
		triesFont = pygame.font.SysFont("Consolas", 28) #(12, 26)
		triesBG = pygame.Surface((90, 32))
		triesBG.fill(self.backgroundColor)
		self.screen.blit(triesBG, (450, 10))
		pygame.display.flip()

		for x in range(self.textObject.numTries):
			#u"\u25A0" is unicode square
			tmp = triesFont.render(u"\u25A0", True, (10, 10, 10), self.backgroundColor)
			triesBG.blit(tmp, (x * 22, 0))
		self.screen.blit(triesBG, (450, 10))



	def FirstTimeGenerate(self):
		#for x in range(len(self.textObject.lArray)):
		#	print("index: ", self.textObject.lArray[x].index, "\nphrase length: ", self.textObject.lArray[x].phraseLength)
		self.renderTries()
		self.createFontSurface()
		self.renderFontSurface()
		pygame.display.flip()