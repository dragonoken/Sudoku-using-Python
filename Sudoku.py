from time import sleep
from random import randrange
from os import system

class SudokuProgram:
	
	def __init__(self):
		#Dictionary of selectable main options
		self.__menu = {"0":self.__quit, "1":'something', "2":self.__showRules, "3":'something', "4":'something'}
		#Shapes and some other stuff for text-based-art
		self.__shapes = {0:" ", "V":chr(5), "H":chr(6), 1:chr(3), 2:chr(4), 3:chr(2), 4:chr(1), 5:chr(25), 6:chr(21), 7:chr(23), 8:chr(22), 9:chr(16)}

		#Spaces from the left side (part of the settings?)
		self.__leftSpace = 3

		#Go to the main menu (Actual start)
		return self.__mainMenu()


	def __mainMenu(self):
		self.__changeScreen() #Wipe the Screen!
		self.__displayMain() #Display main menu!
		
		choice = self.__optionChoice()
		while not self.__validOptChoice(choice, 0, 0) and not self.__validOptChoice(choice, 2, 2): ###Third argument is 0 and 2 just for now. It should be len(self.__menu) - 1 when the program is complete.
			self.__changeScreen()
			self.__displayMain()
			choice = self.__optionChoice()

		chosen = self.__menu[choice] #Chosen option(method)

		#Call the chosen method
		return chosen()


	def __showRules(self):
		self.__changeScreen()

		print(" "*self.__leftSpace, "*****************", sep="")
		print(" "*self.__leftSpace, "      Rules      ", sep="")
		print(" "*self.__leftSpace, "*****************", sep="")
		print()
		print(" "*self.__leftSpace, "# Each puzzle consists of a 9x9 grid (with nine 3x3 boxes)", sep="")
		print(" "*self.__leftSpace, "  containing given clues in various places.", sep="")
		print()
		print(" "*self.__leftSpace, "# Each of the nine 3x3 boxes has to contain all the numbers 1-9 within its squares.", sep="")
		print()
		print(" "*self.__leftSpace, "# Each number can only appear once in a row, column or box.\n", sep="")

		H, V = "H", "V" #Horizontal line, Vertical line
		N = "N" #Number
		nums=[1,2,3,4,5,6,7,8,9]
		aBox =(
				(4,H,H,H,8,H,H,H,8,H,H,H,3),
				(V,0,N,0,V,0,N,0,V,0,N,0,V),
				(5,H,H,H,9,H,H,H,9,H,H,H,7),
				(V,0,N,0,V,0,N,0,V,0,N,0,V),
				(5,H,H,H,9,H,H,H,9,H,H,H,7),
				(V,0,N,0,V,0,N,0,V,0,N,0,V),
				(1,H,H,H,6,H,H,H,6,H,H,H,2)
			  )
		box = "There are 9 boxes like this --->   "
		for rowNum in range(len(aBox)):
			if rowNum == 3:
				print(" "*self.__leftSpace, box, sep="", end="")
			else:
				print(" "*self.__leftSpace, " "*len(box), sep="", end="")
			for letter in aBox[rowNum]:
				if letter == "N":
					print(nums.pop(randrange(len(nums))), end="")
				else:
					print(self.__shapes[letter], end="")
			print()
		nums=[1,2,3,4,5,6,7,8,9]
		aRow =(
				(4,H,H,H,8,H,H,H,8,H,H,H,8,H,H,H,8,H,H,H,8,H,H,H,8,H,H,H,8,H,H,H,8,H,H,H,3),
				(V,0,N,0,V,0,N,0,V,0,N,0,V,0,N,0,V,0,N,0,V,0,N,0,V,0,N,0,V,0,N,0,V,0,N,0,V),
				(1,H,H,H,6,H,H,H,6,H,H,H,6,H,H,H,6,H,H,H,6,H,H,H,6,H,H,H,6,H,H,H,6,H,H,H,2)
			  )
		row = "A row with numbers --->   "
		for rowNum in range(len(aRow)):
			if rowNum == 1:
				print(" "*self.__leftSpace, row, sep="", end="")
			else:
				print(" "*self.__leftSpace, " "*len(row), sep="", end="")
			for letter in aRow[rowNum]:
				if letter == "N":
					print(nums.pop(randrange(len(nums))), end="")
				else:
					print(self.__shapes[letter], end="")
			print()
		print()

		input("Press Enter to go back to the main menu >>>")

		return self.__mainMenu()


	def __displayMain(self):
		H, V = "H", "V" #Horizontal line, Vertical line
		N = "N" #Number
		nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		#SUDOKU art!
		SUDOKU =(
				(4,H,H,H,H,H,H,H,H,3,0,4,H,H,3,0,0,4,H,H,3,0,4,H,H,H,H,H,H,3,0,0,0,0,0,4,H,H,H,H,3,0,0,0,4,H,H,3,0,0,0,4,H,3,0,4,H,H,3,0,0,4,H,H,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
				(V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,0,0,0,0,1,H,3,0,4,H,2,0,0,0,0,1,H,3,0,V,0,0,V,0,0,0,V,0,V,0,V,0,0,V,0,0,V,0,0,V,0,4,H,H,H,8,H,H,H,8,H,H,H,3),
				(V,0,0,4,H,H,H,H,H,2,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,4,H,H,3,0,0,V,0,V,0,0,4,H,H,3,0,0,V,0,V,0,0,V,0,4,H,2,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,N,0,V,0,N,0,V,0,N,0,V),
				(V,0,0,1,H,H,H,H,H,3,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,1,H,2,0,4,H,2,0,V,0,0,V,0,0,V,0,0,V,0,5,H,H,H,9,H,H,H,9,H,H,H,7),
				(V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,0,0,0,0,V,0,0,0,V,0,0,V,0,0,V,0,0,V,0,V,0,N,0,V,0,N,0,V,0,N,0,V),
				(1,H,H,H,H,H,3,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,V,0,0,4,H,3,0,1,H,3,0,V,0,0,V,0,0,V,0,0,V,0,5,H,H,H,9,H,H,H,9,H,H,H,7),
				(4,H,H,H,H,H,2,0,0,V,0,V,0,0,1,H,H,2,0,0,V,0,V,0,0,1,H,H,2,0,0,V,0,V,0,0,1,H,H,2,0,0,V,0,V,0,0,V,0,1,H,3,0,V,0,V,0,0,1,H,H,2,0,0,V,0,V,0,N,0,V,0,N,0,V,0,N,0,V),
				(V,0,0,0,0,0,0,0,0,V,0,V,0,0,0,0,0,0,0,0,V,0,V,0,0,0,0,0,0,4,H,2,0,1,H,3,0,0,0,0,4,H,2,0,V,0,0,V,0,0,0,V,0,V,0,V,0,0,0,0,0,0,0,0,V,0,1,H,H,H,6,H,H,H,6,H,H,H,2),
				(1,H,H,H,H,H,H,H,H,2,0,1,H,H,H,H,H,H,H,H,2,0,1,H,H,H,H,H,H,2,0,0,0,0,0,1,H,H,H,H,2,0,0,0,1,H,H,2,0,0,0,1,H,2,0,1,H,H,H,H,H,H,H,H,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
				)
		print(" "*self.__leftSpace, "-"*79, "\n", " "*self.__leftSpace, "-"*79, sep="")
		for row in SUDOKU:
			print(" "*self.__leftSpace, end="")
			for letter in row:
				if letter == "N":
					print(nums.pop(randrange(len(nums))), end="")
				else:
					print(self.__shapes[letter], end="")
			print() #Next line
		print(" "*self.__leftSpace, "-"*79, "\n", " "*self.__leftSpace, "-"*79, sep="")
		#SUDOKU art finished

		#Display options
		print(" "*self.__leftSpace, "1 : Play\n", sep="")
		print(" "*self.__leftSpace, "2 : Rules\n", sep="")
		print(" "*self.__leftSpace, "3 : Settings\n", sep="")
		print(" "*self.__leftSpace, "0 : Quit\n", sep="")
		print("\n")


	def __changeScreen(self):
		#If the game is running on a Windows Command Prompt, this will clear the screen
		system("cls")
		#Just to make sure, print next-line many times so that the old texts will definately disappear from the current screen
		print("\n"*100)


	def __optionChoice(self):
		choice = input("Choose an option : ") #Take input
		choice = choice.replace(" ", "") #Remove any empty space
		return choice


	def __validOptChoice(self, userInput, startN, endN):
		#This method takes the user's input and two numbers as its arguments.
		#Then checks if the input value is valid -- an integer between startN and endN, including both ends
		if userInput.isdigit() and int(userInput) in range(startN, endN+1):
			return True
		else:
			return False


	def __quit(self):
		self.__changeScreen()

		#Ways you can say "Yes" or "No"
		yeah = ["y", "yes", "yep", "yeah", "quit"]
		nah = ["n", "no", "nope", "nah", "back"]

		#Input is NOT case-sensitive since the upper case letters would be all converted to lower cases here
		choice = input("Quit the program? (Y or N) : ").lower()
		#The program will keep prompting until the player enters a valid input
		while choice not in yeah and choice not in nah:
			self.__changeScreen()
			choice = input("Quit the program? (Y or N)").lower()

		#If choice is "No", then the main menu method is chosen (index [False] == [0]).
		#If choice is "Yes", then the exiting method is chosen (index [True] == [1])
		chosen = (self.__mainMenu, self.__exit)[choice in yeah] #Again, True is 1, False is 0 (Just to make it clear)

		return chosen()


	#Just to make the exiting look a little nice (Also to provide a method that __quit() can return when quitting)
	def __exit(self):
		self.__changeScreen()
		print("Closing.")
		sleep(0.5)
		self.__changeScreen()
		print("Closing..")
		sleep(0.5)
		self.__changeScreen()
		print("Closing...")
		sleep(0.5)
		self.__changeScreen()


if __name__ == '__main__':
	program = SudokuProgram()
