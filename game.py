import os, sys, random, pygame, math
from pygame.locals import *

class Sequence(object):
	def __init__(self, _index, _phraseLength, _isWinningWord=False,
		_isRemoveDud=False, _isResetTries=False):
		#super(gameArray, self).__init__()
		self.index = _index
		self.phraseLength = _phraseLength
		self.isWinningWord = _isWinningWord

		#for braces
		self.isRemoveDud = _isRemoveDud
		self.isResetTries = _isResetTries

class text(object):
	def __init__(self, arg1, arg2=408):
		# super(text, self).__init__()
		self.wordLength = arg1
		self.fullLength = arg2
		self.lArray = [] #array for the Sequence objects

		self.fullText = []
		self.curatedList = []

	def charDecider(self, percent=.25): #tweak percent as needed
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
		inFile = open(str(self.wordLength) + 'list.txt', 'r')
		fullListofWords = inFile.readlines()
		inFile.close()

		for y in range(35):#35 is plenty with a minimum of 4 length words
			self.curatedList.append(str(fullListofWords[random.randint(0, len(fullListofWords)-1)]).rstrip('\n'))


	def findBraces(self):
		openBrace = ['<', '{', '(']
		#closeBrace = ['>', '}', ')']
		lArrayPreSize = len(self.lArray)
		numBracesFound = 0
		for x in range(0, self.fullLength):
			if (self.fullText[x] in openBrace):
				if self.fullText[x] == '<':
					brace = ['<', '>']
				elif self.fullText[x] == '{':
					brace = ['{', '}']
				elif self.fullText[x] == '(':
					brace = ['(', ')']

				for y in range(x%12, (math.ceil((x%12)/12)*12)): #rofl, sets the range from x%12 to the next multiple of 12 above x%12
					print(y)
					if self.fullText[y] == brace[1]: #if appropriate closing bracket found
						numBracesFound += 1
						self.lArray.append(Sequence(x, y - (x%12), False, True))
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
				#print("pointer: ", pointer, "fullText: ", len(self.fullText), "listcounter: ", listcounter, "curatedList: ", len(self.curatedList))
				self.fullText[pointer+x] = self.curatedList[listcounter][x] #the pointer is at the end of the word. after this for loop
			self.lArray.append(Sequence(pointer, self.wordLength)) #at end of every word, add its stuff to the lArray
			listcounter += 1
			pointer += (random.randint(minGap, maxGap) + self.wordLength)
			#end of while loop
		self.lArray[random.randint(0, len(self.lArray) - 1)].isWinningWord = True #decide the winning word
		return


	def textRunner(self):
		while(True):
			self.charGen()
			self.wordPopulator()
			self.wordInserter()
			if (self.findBraces()):
				return
			else:
				self.__init__(self.wordLength)
			
		#at this point we have a text object with everything for the game set up.
		return