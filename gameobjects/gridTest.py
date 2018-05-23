from grid import Grid
from cellTest import cellInfo

class Grid(Grid):
	def isBuilding(self):
		return self.__buildMode

	def isEditableAt(self, row, col):
		return self.__bigGrid[ row * self.__gridLength + col ].isEditable()

	def getCellAt(self, row, col):
		return self.__bigGrid[ row * self.__gridLength + col ]

def rowColInput():
	clear()
	rows = input("Number of rows of each Mini Grid : ")
	rows = rows.replace(" ", "")
	while ( not rows.isdigit() ) or ( rows[0] == "0" ):
		clear()
		print("Invalid Value.\nPlease enter a positive integer for the number of rows.\n")
		rows = input("Number of rows of each Mini Grid : ")
		rows = rows.replace(" ", "")
	rows = int(rows)

	clear()
	print(f"Number of rows of each Mini Grid : {rows}\n")
	cols = input("Number of columns of each Mini Grid : ")
	cols = cols.replace(" ", "")
	while ( not cols.isdigit() ) or ( cols[0] == "0" ):
		clear()
		print("Invalid Value.\nPlease enter a positive integer for the number of columns.\n")
		print(f"Number of rows of each Mini Grid : {rows}\n")
		cols = input("Number of columns of each Mini Grid : ")
		cols = cols.replace(" ", "")
	cols = int(cols)

	return (rows, cols)

def visualizeGrid(grid, showZero=True, indicateUneditable=True, cursor=(False, None, None), scrPosition=3):

	cellSize = len( str( grid.getGridLen() ) ) * 2 - 1

	def printTopLine():
		print( " " * scrPosition, end="" )
		for col in range( grid.getGridLen() ):
			if col % grid.getMiniSize()[1] == 0:
				print( chr(1), end="" )
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(22), end="" )

			elif col % grid.getMiniSize()[1] == grid.getMiniSize()[1] - 1:
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(2), end="" )
				if col < grid.getGridLen() - 1:
					print( " ", end="" )
				else:
					print()
			else:
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(22), end="" )

	def printNumLine(row):
		print( " " * scrPosition, end="" )
		for col in range( grid.getGridLen() ): #Lines with numbers
			val = grid.getValueAt( row, col )
			if ( val == 0 ) and ( showZero == False ):
				cellStr = " "
			else:
				cellStr = " ".join( list( str( val ) ) )
			if len( cellStr ) < cellSize:
				cellStr = ( " " * ( ( cellSize - len( cellStr ) ) // 2 ) ) + cellStr + ( " " * ( ( cellSize - len( cellStr ) ) // 2 ) )

			if ( cursor[1] == row ) and ( cursor[2] == col ) and ( cursor[0] == True ):
				if ( not grid.isEditableAt( row, col ) ) and ( indicateUneditable == True ):
					print( chr(5), "{", cellStr, "}", sep="", end="" )
				else:
					print( chr(5), "[", cellStr, "]", sep="", end="" )
			else:
				if ( not grid.isEditableAt( row, col ) ) and ( indicateUneditable == True ):
					print( chr(5), "<", cellStr, ">", sep="", end="" )
				else:
					print( chr(5), " ", cellStr, " ", sep="", end="" )
			if ( col % grid.getMiniSize()[1] == grid.getMiniSize()[1] - 1 ):
				print( chr(5), end="" )
				if col != grid.getGridLen() - 1:
					print( " ", end="" )
				else:
					print()

	def printMidLine():
		print( " " * scrPosition, end="" )
		for col in range( grid.getGridLen() ):
			if col % grid.getMiniSize()[1] == 0:
				print( chr(25), end="" )
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(16), end="" )

			elif col % grid.getMiniSize()[1] == grid.getMiniSize()[1] - 1:
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(23), end="" )
				if col < grid.getGridLen() - 1:
					print( " ", end="" )
				else:
					print()
			else:
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(16), end="" )

	def printBottomLine():
		print( " " * scrPosition, end="" )
		for col in range( grid.getGridLen() ):
			if col % grid.getMiniSize()[1] == 0:
				print( chr(3), end="" )
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(21), end="" )

			elif col % grid.getMiniSize()[1] == grid.getMiniSize()[1] - 1:
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(4), end="" )
				if col < grid.getGridLen() - 1:
					print( " ", end="" )
				else:
					print()
			else:
				print( chr(6) * ( cellSize + 2 ), end="" )
				print( chr(21), end="" )


	for row in range( grid.getGridLen() ):

		if row % grid.getMiniSize()[0] == 0: #Ceiling
			printTopLine()
		elif row % grid.getMiniSize()[0] <= grid.getMiniSize()[0] - 1:
			printMidLine()

		printNumLine(row)

		if row % grid.getMiniSize()[0] == grid.getMiniSize()[0] - 1:
			printBottomLine()

def displayInfo(grid, showZero=True, indicateUneditable=True, scrPosition=3):
	print( " " * scrPosition, "---------------------------------------", sep="" )
	print( " " * scrPosition, "Overall Size (Row,Column): ", grid.getGridLen(), " x ", grid.getGridLen(), sep="" )
	print( " " * scrPosition, "Mini Grid Size (Row,Column): ", grid.getMiniSize()[0], " x ", grid.getMiniSize()[1], sep="" )
	print( " " * scrPosition, "Build Mode : ", grid.isBuilding(), sep="" )
	print()
	print( " " * scrPosition, "Show 0 : ", bool(showZero), sep="" )
	print( " " * scrPosition, "Indicate Non-Editable : ", indicateUneditable, sep="" )
	print( " " * scrPosition, "---------------------------------------", sep="" )

def displayOptions(scrPosition=3):
	print( " " * scrPosition, "0 : Quit", sep="" )
	print( " " * scrPosition, "1 : Change Value", sep="" )
	print( " " * scrPosition, "2 : Toggle Build Mode", sep="" )
	print( " " * scrPosition, "3 : Clear Grid (Build : All Cells / Normal : Except Uneditables)\n", sep="" )
	print( " " * scrPosition, "a : Show/Hide 0", sep="" )
	print( " " * scrPosition, "b : Toggle Uneditable Indicator", sep="" )
	print( " " * scrPosition, "n : Discard and Make a New Grid", sep="" )

def clear():
	print("\n"*100)

def changeValueMode(grid, scrPosition=3):

	def changeValue(cRow, cCol):
		clear()
		visualizeGrid(grid, showZero=True, indicateUneditable=True, cursor=(True, cRow, cCol), scrPosition=scrPosition)
		print()
		print( " " * scrPosition, "( 'B' to go back )\n", sep="" )
		val = input("Set Value to : ").replace(" ", "").lower()
		while ( val != "b" ) and ( ( not val.isdigit() ) or ( len(val) > 1 and val[0] == "0" ) ):
			clear()
			visualizeGrid(grid, showZero=True, indicateUneditable=True, cursor=(True, cRow, cCol), scrPosition=scrPosition)
			print()
			print( " " * scrPosition, "( 'B' to go back )\n", " " * scrPosition, "Please enter a non-negative integer for the Value\n", sep="" )
			val = input("Set Value to : ").replace(" ", "").lower()
		if val != "b":
			val = int(val)
			grid.setValueAt(cRow, cCol, val)

	back = False
	(cRow,cCol) = (0,0)
	while back == False:
		clear()
		visualizeGrid(grid, showZero=True, indicateUneditable=True, cursor=(True, cRow, cCol), scrPosition=scrPosition)
		cellInfo(grid.getCellAt(cRow,cCol))
		print( " " * scrPosition, "*-----------------------( Case Does Not Matter )-----------------------*", sep="" )
		print( " " * scrPosition, "W,A,S,D : Move the Cursor UP/LEFT/DOWN/RIGHT  (Combinations are allowed)", sep="" )
		print( " " * scrPosition, "(Enter) : Change the Value", sep="" )
		print( " " * scrPosition, "BACK : Go Back to the Main Interface", sep="" )
		print( " " * scrPosition, "*----------------------------------------------------------------------*\n", sep="" )
		ctrl = input("Control : ").replace(" ", "").lower()

		if ctrl == "":
			changeValue(cRow, cCol)
		elif ctrl == "back":
			back = True
		elif all( [ c in "wasd" for c in ctrl ] ):
			rowInc = ctrl.count("s") - ctrl.count("w")
			colInc = ctrl.count("d") - ctrl.count("a")
			cRow = ( cRow + rowInc ) % grid.getGridLen()
			cCol = ( cCol + colInc ) % grid.getGridLen()


if __name__ == "__main__":
	screenPosition = 3
	showZero = True
	indicateUneditable = True
	quit = False

	(rows,cols) = rowColInput()
	grid = Grid(rows, cols)

	while quit == False:
		clear()
		visualizeGrid(grid, showZero=showZero, indicateUneditable=indicateUneditable, scrPosition=screenPosition)
		print("\n")
		displayInfo(grid, showZero, indicateUneditable, screenPosition)
		print()
		displayOptions(screenPosition)
		print("\n")
		choice = input("Select an option : ")

		if choice == "0":
			clear()
			sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
			while sure not in ("y","n"):
				clear()
				sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
			if sure == "y":
				quit = True
			else:
				pass
		elif choice == "1":
			changeValueMode(grid, screenPosition)
		elif choice == "2":
			grid.toggleBuildMode()
		elif choice == "3":
			grid.clearGrid()
		elif choice == "a":
			showZero = not showZero
		elif choice == "b":
			indicateUneditable = not indicateUneditable
		elif choice == "n":
			clear()
			sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
			while sure not in ("y","n"):
				clear()
				sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
			if sure == "y":
				(rows,cols) = rowColInput()
				grid = Grid(rows, cols)
			else:
				pass