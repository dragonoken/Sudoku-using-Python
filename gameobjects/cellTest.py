from cell import Cell

def visualizeCell(cell):
	value = str(cell.getValue())
	print("      ", chr(1), chr(6), chr(6), chr(6)*len(value), chr(2), "\n", #By using len(value), the shape of the cell would be adjusted depending on the number of digits
		  "      ", chr(5),  " ",   value,   " ",              chr(5), "\n",
		  "      ", chr(3), chr(6), chr(6), chr(6)*len(value), chr(4), sep="")

def cellInfo(cell):
	print("   -------------------------------------------------------")
	print("   Cell Value :", cell.getValue())
	print("   Possible Value String :", cell.getPossibles())
	print("   Can Be Edited :", cell.isEditable())
	print("   -------------------------------------------------------")

def changeValue(cell):
	value = input("Value to assign : ")
	if value.isdigit() and not (len(value) > 1 and value[0] == 0):
		cell.setValue(int(value))
	else:
		cell.setValue(value)

def changePossible(cell):
	possible = input("Possible values without spaces : ")
	cell.setPossibles(possible)

def optionDisplay():
	print("   0 : Quit\n")
	print("   1 : Change Value\n")
	print("   2 : Change Possibles\n")
	print("   3 : Switch Editable")

def clear():
	print("\n"*100)

if __name__ == "__main__":
	exit_status = False
	cell = Cell()
	while exit_status != True:
		clear()
		visualizeCell(cell)
		print("\n")
		cellInfo(cell)
		print()
		optionDisplay()
		print("\n")

		choice = input("Choose an option : ")

		if choice == "0":
			exit_status = True
		elif choice == "1":
			print()
			changeValue(cell)
		elif choice == "2":
			print()
			changePossible(cell)
		elif choice == "3":
			cell.setEditable(not cell.isEditable())
		else:
			pass

