import os, sys, random, pygame, math
from pygame.locals import *

class Sequence(object):
	def __init__(self, _index, _phraseLength, _gameClass=None, _isWord =False,
		_isRemoveDud=False, _isResetTries=False,):
		#super(gameArray, self).__init__()
		self.index = _index
		self.phraseLength = _phraseLength
		self.phraseText = None
		self.gameClass = _gameClass

		self.isWord = _isWord

		#for braces
		self.isRemoveDud = _isRemoveDud
		self.isResetTries = _isResetTries

		self.buildPhraseText()

	def buildPhraseText(self):
		tmp = []
		for x in range(self.index, self.index + self.phraseLength):
			tmp.append(self.gameClass.fullText[x])
		self.phraseText = ''.join(tmp)


class text(object):
	def __init__(self, arg1, arg2=408):
		# super(text, self).__init__()
		self.wordLength = arg1
		self.fullLength = arg2

		self.lArray = [] #array for the Sequence objects
		self.winningWord = None
		self.numTries = 4

		self.gameOver = False

		self.fullText = []
		self.curatedList = []

		self.displayObject = None

	def getGameOver(self):
		return self.gameOver

	def charDecider(self, percent=.3): #tweak percent as needed
		fillerArr = ['!', '@', '#', '?', '$', '%', '^', '*', '-', '+', '=', ',', '.', '\\', '/', ':', ';', '|']
		bracesArr = ['<', '>', '{', '}', '(', ')']
		if random.random() <= percent: #the higher percent is, the more likely braces are to be selected
			return(bracesArr[random.randint(0, 5)])
		else:
			return(fillerArr[random.randint(0, 17)])
		
	#34 rows x 12 chars per line = 408 total chars
	def charGen(self):		
		#canonical Python idiom is to add items to a list and then use str.join to concatenate them all at the end
		for x in range(self.fullLength):
			self.fullText.append(self.charDecider())
		 #0-407
		

	def wordPopulator(self):
		inFile = open('wordlists/' + str(self.wordLength) + 'list.txt', 'r')
		fullListofWords = inFile.readlines()
		inFile.close()

		for y in range(35):#35 is plenty with a minimum of 4 length words
			self.curatedList.append(str(fullListofWords[random.randint(0, len(fullListofWords)-1)]).rstrip('\n'))


	def findBraces(self):
		openBrace = ['<', '{', '(']
		#closeBrace = ['>', '}', ')']
		lArrayPreSize = len(self.lArray)
		numBracesFound = 0
		for x in range(self.fullLength):
			if (self.fullText[x] in openBrace):
				if self.fullText[x] == '<':
					brace = ['<', '>']
				elif self.fullText[x] == '{':
					brace = ['{', '}']
				elif self.fullText[x] == '(':
					brace = ['(', ')']

				lRange = x
				#next multiple of 12 above x
				uRange = math.ceil((x+1)/12) * 12
				for y in range(lRange, uRange):
					#if there's a letter, stop
					if not self.fullText[y].isupper():
						#if correct closing bracket found
						if self.fullText[y] == brace[1]:
							numBracesFound += 1
							self.lArray.append(Sequence(x, y - x + 1, _isRemoveDud=True, _gameClass=self))
							break
					else:
						break

		#triesReset
		if numBracesFound < 3 or numBracesFound > 10:
			return(False)

		if (random.random() >= .3): #adjust to change likeliness of triesReset
			#print("lArrayPreSize: ", lArrayPreSize, "||numBracesFound: ", numBracesFound)
			rando = random.randint(lArrayPreSize, lArrayPreSize + numBracesFound - 1) #decide which to change
			self.lArray[rando].isResetTries = True
			self.lArray[rando].isRemoveDud = False

		return(True)


#inserts words into fullText from curatedList. Also populates lArray.
	def wordInserter(self):  
		minGap = 3
		maxGap = 20 #add a way to tend towards lower numbers, look up beta distributions
		listcounter = 0
		pointer = random.randint(minGap, maxGap)
		
		while pointer < (self.fullLength - self.wordLength):
			for x in range(0, self.wordLength):
				self.fullText[pointer+x] = self.curatedList[listcounter][x] #the pointer is at the end of the word. after this for loop
			self.lArray.append(Sequence(pointer, self.wordLength, _isWord=True, _gameClass=self)) #at end of every word, add its stuff to the lArray
			listcounter += 1
			pointer += (random.randint(minGap, maxGap) + self.wordLength)
			#end of while loop
		rando = random.randint(0, len(self.lArray) - 1)
		self.winningWord = self.lArray[rando] #decide winning word
		return

	def FirstTimeGenerate(self):
		while(True):
			self.charGen()
			self.wordPopulator()
			self.wordInserter()
			if (self.findBraces()):
				return
			else:
				self.__init__(self.wordLength)		

	def numCorrect(self, seq):
		count = 0
		for x in range(self.wordLength):
			if (self.winningWord.phraseText[x] == seq.phraseText[x]):
				count += 1
		return(count)		

	def userClicked(self, mouseLocation):
		counter = 0
		for SeqObject in self.lArray:
			iiP = self.displayObject.isInPhrase(SeqObject, mouseLocation)
			if (iiP == 'word'):
				if SeqObject == self.winningWord:
					self.displayObject.ConsoleRender(SeqObject.phraseText, 'You Won!')
					self.displayObject.ConsoleRender(lowerLine="Click to exit.")
					self.gameOver = True
					return
				#if wrong word	
				else:
					self.numTries -= 1
					if self.numTries <= 0:
						self.displayObject.renderTries()
						self.displayObject.ConsoleRender(SeqObject.phraseText, 'Out of tries.')
						self.displayObject.ConsoleRender(lowerLine="Click to exit.")
						self.gameOver = True
						return
					self.displayObject.ConsoleRender(SeqObject.phraseText, ''.join([str(self.numCorrect(SeqObject)), '/', str(self.wordLength), ' correct.']))
					self.lArray.pop(counter)
					counter -= 1
					self.displayObject.createFontSurface()

			if (iiP == 'brace'):
				#if the brace set is RemoveDud
				if SeqObject.isRemoveDud:
					while True:
						rando = random.randint(0, len(self.lArray))
						#if the randomly selected doomed item is a word and isn't the winning word
						if self.lArray[rando].isWord and not (self.lArray[rando] == self.winningWord):
							self.displayObject.ConsoleRender(SeqObject.phraseText, 'Dud Removed.')
							for x in range(self.lArray[rando].index, self.lArray[rando].index + self.lArray[rando].phraseLength):
								self.fullText[x] = '.'
							self.lArray.pop(counter)
							self.lArray.pop(rando)
							counter -= 2
							break

				elif SeqObject.isResetTries:
					self.displayObject.ConsoleRender(SeqObject.phraseText, 'Tries Reset.')
					self.numTries = 4
					self.lArray.pop(counter)
					counter -= 1

			#this keeps track of which item in lArray we're accessing. Necessary for removing items.
			counter += 1
		self.displayObject.renderTries()
		self.displayObject.createFontSurface()
		self.displayObject.renderFontSurface()