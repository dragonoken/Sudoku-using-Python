from time import sleep
from random import randrange

class SudokuProgram:
	
	def __init__(self):
		#Dictionary of selectable main options
		self.__menu = {"0":self.__quit, "1":'something', "2":'something', "3":'something', "4":'something'}
		#Shapes and some other stuff for text-based-art
		self.__shapes = {0:" ", "V":chr(5), "H":chr(6), 1:chr(3), 2:chr(4), 3:chr(2), 4:chr(1), 5:chr(25), 6:chr(21), 7:chr(23), 8:chr(22), 9:chr(16)}

		#Spaces from the left side (part of the settings?)
		self.__leftSpace = 3

		#While the user is not quitting the game
		self.__quitting = False

		#Main Loop
		while self.__quitting == False:
			self.__changeScreen() #Wipe the Screen!
			self.__displayMain() #Display main menu!
		
			choice = self.__optionChoice()
			while not self.__validOptChoice(choice, 0, 0): ###Third argument is 0 just for now. It should be len(self.__menu) - 1 when the program is complete.
				self.__changeScreen()
				self.__displayMain()
				print(self.__quitting)
				choice = self.__optionChoice()

			chosen = self.__menu[choice] #Chosen option(method)

			if chosen == self.__quit: #If the user chose "Quit" option,
				self.__quitting = chosen() #Assign the return value of the quitting method to the sentinel variable
			else:
				chosen() #Otherwise, just call the function

		self.__exit()


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
		print(" "*self.__leftSpace, "2 : Settings\n", sep="")
		print(" "*self.__leftSpace, "3 : Something else\n", sep="")
		print(" "*self.__leftSpace, "0 : Quit\n", sep="")
		print("\n")


	def __changeScreen(self):
		#Prints next-line many times so that the old texts will disappear from the current screen
		print("\n"*100)


	def __optionChoice(self):
		choice = input("Choose an options : ") #Take input
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
		#The program will keep prompting until the user enters a valid input
		while choice not in yeah and choice not in nah:
			self.__changeScreen()
			choice = input("Quit the program? (Y or N)").lower()

		#Returns whether the user is really quitting or not
		return choice in yeah


	#Just to make the exiting look a little nice
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
