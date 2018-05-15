from time import sleep
from random import randrange
from os import system

class SudokuProgram:
	
	def __init__(self):
		#Shapes and some other stuff for text-based-art
		self.__shapes = {0:" ", "V":chr(5), "H":chr(6), 1:chr(3), 2:chr(4), 3:chr(2), 4:chr(1), 5:chr(25), 6:chr(21), 7:chr(23), 8:chr(22), 9:chr(16)}

		#Go to the main menu (Actual start)
		return self.__mainMenu()


	def __mainMenu(self):
		self.__changeScreen() #Wipe the Screen!
		self.__displayMain() #Display main menu!

		#Dictionary of selectable main options
		menu = {"0":self.__quit, "1":self.__playOption, "2":self.__showRules}
		
		choice = self.__optionChoice()
		while not self.__validOptChoice(choice, 0, 3) or choice == "3": ###3 not available yet. Soon to be updated.
			self.__changeScreen()
			self.__displayMain()
			if choice == "3":
				print("Not available yet, Sorry!")
			choice = self.__optionChoice()

		chosen = menu[choice] #Chosen option(method)

		#Call the chosen method
		return chosen()


	def __playOption(self):
		self.__changeScreen() #Wipe the screen
		self.__displayPlayOpt() #Display play options

		#Dictionary of selectable play options
		menu = {"0":self.__mainMenu, "1":'Play', "2":'Build/Edit Game'} ###Soon to be updated

		choice = self.__optionChoice()
		while not self.__validOptChoice(choice, 0, 3) or choice in ("1", "2"): ###No play options are available so far
			self.__changeScreen()
			self.__displayPlayOpt()
			if choice in ("1", "2"):
				print("Playing options are not available yet, Sorry!")
			choice = self.__optionChoice()

		chosen = menu[choice] #Chosen option

		#Call the chosen method
		return chosen()


	def __showRules(self):
		self.__changeScreen()

		print("   @@@@@@@@@@@@@@@@@", sep="")
		print("       R u l e s    ", sep="")
		print("   @@@@@@@@@@@@@@@@@", sep="")
		print()
		print("   # Each puzzle consists of a 9x9 grid (with nine 3x3 boxes)", sep="")
		print("     containing given clues in various places.", sep="")
		print()
		print("   # Each of the nine 3x3 boxes has to contain all the numbers 1-9 within its squares.", sep="")
		print()
		print("   # Each number can only appear once in a row, column or box.\n", sep="")

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
				print("   ", box, sep="", end="")
			else:
				print("   ", " "*len(box), sep="", end="")
			for letter in aBox[rowNum]:
				if letter == "N":
					print(nums.pop(randrange(len(nums))), end="")
				else:
					print(self.__shapes[letter], end="")
			print()
		nums=[1,2,3,4,5,6,7,8,9]
		aRow =(
				(4,H,H,H,8,H,H,H,8,H,H,H,3,0,4,H,H,H,8,H,H,H,8,H,H,H,3,0,4,H,H,H,8,H,H,H,8,H,H,H,3),
				(V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,N,0,V,0,N,0,V,0,N,0,V),
				(1,H,H,H,6,H,H,H,6,H,H,H,2,0,1,H,H,H,6,H,H,H,6,H,H,H,2,0,1,H,H,H,6,H,H,H,6,H,H,H,2)
			  )
		row = "A row with numbers --->   "
		for rowNum in range(len(aRow)):
			if rowNum == 1:
				print("   ", row, sep="", end="")
			else:
				print("   ", " "*len(row), sep="", end="")
			for letter in aRow[rowNum]:
				if letter == "N":
					print(nums.pop(randrange(len(nums))), end="")
				else:
					print(self.__shapes[letter], end="")
			print()
		print("\n\n")

		input("Press Enter to go back to the main menu >>>")

		return self.__mainMenu()


	def __displayMain(self):
		H, V = "H", "V" #Horizontal line, Vertical line
		N = "N" #Number
		nums = [1, 2, 3, 4, 5, 6, 7, 8, 9] #Number list
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
		print("   ", "-"*79, "\n   ", "-"*79, sep="") #Line decoration
		for row in SUDOKU:
			print("   ", end="")
			for letter in row:
				if letter == "N": #Pop and print a random number from the list 'nums'
					print(nums.pop(randrange(len(nums))), end="")
				else: #Print the shape according to the shape dictionary
					print(self.__shapes[letter], end="")
			print() #Next line
		print("   ", "-"*79, "\n   ", "-"*79, sep="") #Line decoration
		#SUDOKU art finished

		#Display options
		print("   1 : Play\n", sep="")
		print("   2 : Rules\n", sep="")
		print("   0 : Quit", sep="")
		print("\n\n")


	def __displayPlayOpt(self):
		H, V = "H", "V" #Horizontal line, Vertical line
		N, n = "N", "n" #Number1, Number2
		nums1 = [1, 2, 3, 4, 5, 6, 7, 8, 9] #Number list 1
		nums2 = [1, 2, 3, 4, 5, 6, 7, 8, 9] #Number list 2
		#PLAY art!
		PLAY =(
				(0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,H,H,H,H,H,H,H,H,3,0,4,H,H,3,0,0,0,0,0,0,0,0,0,4,H,H,H,H,3,0,0,0,4,H,H,3,0,0,4,H,H,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
				(4,H,H,H,8,H,H,H,8,H,H,H,3,0,V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,4,H,2,0,0,0,0,1,H,3,0,V,0,0,V,0,0,V,0,0,V,0,4,H,H,H,8,H,H,H,8,H,H,H,3),
				(V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,0,4,H,H,3,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,4,H,H,3,0,0,V,0,V,0,0,1,3,4,2,0,0,V,0,V,0,n,0,V,0,n,0,V,0,n,0,V),
				(5,H,H,H,9,H,H,H,9,H,H,H,7,0,V,0,0,1,H,H,2,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,V,0,0,V,0,0,V,0,1,3,0,0,1,2,0,0,4,2,0,5,H,H,H,9,H,H,H,9,H,H,H,7),
				(V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,1,H,H,2,0,0,V,0,0,1,H,3,0,0,4,H,2,0,0,V,0,n,0,V,0,n,0,V,0,n,0,V),
				(5,H,H,H,9,H,H,H,9,H,H,H,7,0,V,0,0,4,H,H,H,H,H,2,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,0,0,0,0,0,0,V,0,0,0,0,V,0,0,V,0,0,0,0,5,H,H,H,9,H,H,H,9,H,H,H,7),
				(V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,1,H,H,H,H,H,3,0,V,0,0,4,H,H,3,0,0,V,0,0,0,0,V,0,0,V,0,0,0,0,V,0,n,0,V,0,n,0,V,0,n,0,V),
				(1,H,H,H,6,H,H,H,6,H,H,H,2,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,0,0,0,V,0,0,V,0,0,0,0,1,H,H,H,6,H,H,H,6,H,H,H,2),
				(0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,H,H,2,0,0,0,0,0,0,0,1,H,H,H,H,H,H,H,H,2,0,1,H,H,2,0,0,1,H,H,2,0,0,0,0,1,H,H,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
				)
		print("   ", "-"*71, "\n   ", "-"*71, sep="") #Line decoration
		for row in PLAY:
			print("   ", end="")
			for letter in row:
				if letter == "N": #Pop and print a random number from the list 'nums1'
					print(nums1.pop(randrange(len(nums1))), end="")
				elif letter == "n": #Pop and print a random number from the list 'nums2'
					print(nums2.pop(randrange(len(nums2))), end="")
				else: #Print the shape according to the shape dictionary
					print(self.__shapes[letter], end="")
			print() #Next line
		print("   ", "-"*71, "\n   ", "-"*71, sep="") #Line decoration
		#PLAY art finished

		#Display options
		print("   1 : Play\n", sep="")
		print("   2 : Build/Edit Game\n", sep="")
		print()
		print("   0 : Back", sep="")
		print("\n\n")


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
		if userInput.isdigit() and not (len(userInput) > 1 and userInput[0] == "0") and int(userInput) in range(startN, endN+1):
			return True
		else:
			return False


	def __quit(self):
		self.__changeScreen()

		#Ways you can say "Yes" or "No"
		yes = ["y", "yes", "yep", "yeah", "quit"]
		no = ["n", "no", "nope", "nah", "back"]

		#Input is NOT case-sensitive since the upper case letters would be all converted to lower cases here
		choice = input("Quit the program? (Y or N) : ").lower()
		#The program will keep prompting until the player enters a valid input
		while choice not in yes and choice not in no:
			self.__changeScreen()
			choice = input("Quit the program? (Y or N)").lower()

		#If choice is "No", then the main menu method is chosen (index [False] == [0]).
		#If choice is "Yes", then the exiting method is chosen (index [True] == [1])
		chosen = (self.__mainMenu, self.__exit)[choice in yes] #Again, True is 1, False is 0 (Just to make it clear)

		return chosen()


	#Just to make the exiting look a little nice (Also to provide a method that __quit() can return when quitting)
	def __exit(self):
		self.__changeScreen()
		print("Closing.")
		sleep(0.25)
		self.__changeScreen()
		print("Closing..")
		sleep(0.25)
		self.__changeScreen()
		print("Closing...")
		sleep(0.25)
		self.__changeScreen()


if __name__ == '__main__':
	program = SudokuProgram()
