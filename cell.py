class Cell:
	def __init__(self):
		self.__value = 0
		self.__possibles = "#1#2#3#4#5#6#7#8#9"
		self.__editable = True

	def setValue(self, num):
		if (self.__editable == True) and (isinstance(num, int)) and (str(num) in self.__possibles.split("#") + ["0"]) and (0 <= num < 10):
			self.__value = num
		else:
			pass

	def getValue(self):
		return self.__value

	def setPossibles(self, possibles):
		possibles = str(possibles) #Make sure it is in a string form
		if "#" not in possibles and possibles.isdigit(): #If '#' is not in the string and the string consists of only digits, it assumes that the values are all 1-digit length
			self.__possibles = "#" + "#".join(sorted(list(set(possibles)))) #Making sure no number is repeating, then sorting in order, then put "#"s between digits... ----------(1)
		elif len(possibles) == 0: #If the string has nothing, then the possibles are nothing
			self.__possibles = "" 
		elif "#" in possibles and "".join(possibles.split("#")).isdigit(): #In cases where there are "#" separating numbers (However many #s are separating numbers!)
			while possibles.count("##") != 0: #Make sure there is no #s next to each other before being processed
				possibles = possibles.replace("##","#")
			if possibles[0] != "#": #If the string does not start with #, it will count all each digit before # as a single number
				self.__possibles = "#" + "#".join(sorted(list(set(possibles.split("#")[0]).union(set(possibles.split("#")[1:]))))) #Basically a more complex version of (1) few lines above
			else:
				self.__possibles = "#" + "#".join(sorted(list(set(possibles.split("#")[1:])))) #Similar
		else: #Otherwise, it will not take the input
			pass

	def getPossibles(self):
		return self.__possibles

	def setEditable(self, tf):
		self.__editable = bool(tf)

	def isEditable(self):
		return self.__editable