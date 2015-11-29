import sys, os

class gracie(object):
	def __init__(self):
		self.var = 1


class mom(object):
	def __init__(self, arg1):
		self.gracieObject = arg1

	def setVar(self):
		self.gracieObject.var = 0

g = gracie()
m = mom(g)
print("gracie: ", g.var)
m.setVar()
print("new gracie: ", g.var)
