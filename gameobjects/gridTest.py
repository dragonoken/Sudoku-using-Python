"""
This is a program made for testing the Grid module
"""

from grid import Grid
from cellTest import cellInfo


class Grid(Grid):
    """
    This class inherits all features of 'Grid' class and overwrites it

    It has a few additional functions for this specific program
    """

    def isBuilding(self):
        """
        Returns bool
        True if the build/edit mode is on
        False otherwise
        """
        return self.__buildMode

    def isEditableAt(self, row, column):
        """
        Returns bool
        True if the corresponding cell is editable
        False otherwise

        Returns False if the value of row or column is invalid
        """
        if 0 <= row < self.__gridLength and 0 <= column < self.__gridLength:
            iseditable = self.__bigGrid[row *
                                        self.__gridLength + column].isEditable()
        else:
            iseditable = False
        return iseditable

    def getCellAt(self, row, column):
        """
        Returns the corresponding Cell object

        Returns None if the value of row or column is invalid
        """
        if 0 <= row < self.__gridLength and 0 <= column < self.__gridLength:
            cell = self.__bigGrid[row * self.__gridLength + column]
        else:
            cell = None
        return cell


def row_col_input():
    """
    Function for taking valid row value and column value for Grid object
    """
    clear()
    mini_rows = input("Number of rows of each Mini Grid : ")
    mini_rows = mini_rows.replace(" ", "")
    while not mini_rows.isdigit() or mini_rows[0] == "0":
        clear()
        print("Invalid Value.\nPlease enter a positive integer for the number of rows.\n")
        mini_rows = input("Number of rows of each Mini Grid : ")
        mini_rows = mini_rows.replace(" ", "")
    mini_rows = int(mini_rows)

    clear()
    print(f"Number of rows of each Mini Grid : {mini_rows}\n")
    mini_cols = input("Number of columns of each Mini Grid : ")
    mini_cols = mini_cols.replace(" ", "")
    while not mini_cols.isdigit() or mini_cols[0] == "0":
        clear()
        print(
            "Invalid Value.\nPlease enter a positive integer for the number of columns.\n")
        print(f"Number of rows of each Mini Grid : {mini_rows}\n")
        mini_cols = input("Number of columns of each Mini Grid : ")
        mini_cols = mini_cols.replace(" ", "")
    mini_cols = int(mini_cols)

    return (mini_rows, mini_cols)


def visualize_grid(grid_object, display_zeros=True, indicate_uneditables=True, cursor=(False, None, None), spaces=3):
    """
    Function for visualizing the grid in a form of text-based design
    """

    cell_size = len(str(grid_object.getGridLen())) * 2 - 1

    def print_top_line():
        """
        Nested function for printing upper layers of mini grids
        """
        print(" " * spaces, end="")
        for col in range(grid_object.getGridLen()):
            if col % grid_object.getMiniSize()[1] == 0:
                print(chr(1), end="")
                print(chr(6) * (cell_size + 2), end="")
                print(chr(22), end="")

            elif col % grid_object.getMiniSize()[1] == grid_object.getMiniSize()[1] - 1:
                print(chr(6) * (cell_size + 2), end="")
                print(chr(2), end="")
                if col < grid_object.getGridLen() - 1:
                    print(" ", end="")
                else:
                    print()
            else:
                print(chr(6) * (cell_size + 2), end="")
                print(chr(22), end="")

    def print_number_line(row):
        """
        Nested function for printing lines with number values
        """
        print(" " * spaces, end="")
        for col in range(grid_object.getGridLen()):  # Lines with numbers
            val = grid_object.getValueAt(row, col)
            if (val == 0) and (display_zeros is False):
                cellStr = " "
            else:
                cellStr = " ".join(list(str(val)))
            if len(cellStr) < cell_size:
                cellStr = (" " * ((cell_size - len(cellStr)) // 2)) + \
                    cellStr + (" " * ((cell_size - len(cellStr)) // 2))

            if (cursor[1] == row) and (cursor[2] == col) and (cursor[0] is True):
                if (not grid_object.isEditableAt(row, col)) and (indicate_uneditables is True):
                    print(chr(5), "{", cellStr, "}", sep="", end="")
                else:
                    print(chr(5), "[", cellStr, "]", sep="", end="")
            else:
                if (not grid_object.isEditableAt(row, col)) and (indicate_uneditables is True):
                    print(chr(5), "<", cellStr, ">", sep="", end="")
                else:
                    print(chr(5), " ", cellStr, " ", sep="", end="")
            if col % grid_object.getMiniSize()[1] == grid_object.getMiniSize()[1] - 1:
                print(chr(5), end="")
                if col != grid_object.getGridLen() - 1:
                    print(" ", end="")
                else:
                    print()

    def print_middle_line():
        """
        Nested function for printing layers between number lines
        """
        print(" " * spaces, end="")
        for col in range(grid_object.getGridLen()):
            if col % grid_object.getMiniSize()[1] == 0:
                print(chr(25), end="")
                print(chr(6) * (cell_size + 2), end="")
                print(chr(16), end="")

            elif col % grid_object.getMiniSize()[1] == grid_object.getMiniSize()[1] - 1:
                print(chr(6) * (cell_size + 2), end="")
                print(chr(23), end="")
                if col < grid_object.getGridLen() - 1:
                    print(" ", end="")
                else:
                    print()
            else:
                print(chr(6) * (cell_size + 2), end="")
                print(chr(16), end="")

    def print_bottom_line():
        """
        Nested function for printing lower layers of mini grids
        """
        print(" " * spaces, end="")
        for col in range(grid_object.getGridLen()):
            if col % grid_object.getMiniSize()[1] == 0:
                print(chr(3), end="")
                print(chr(6) * (cell_size + 2), end="")
                print(chr(21), end="")

            elif col % grid_object.getMiniSize()[1] == grid_object.getMiniSize()[1] - 1:
                print(chr(6) * (cell_size + 2), end="")
                print(chr(4), end="")
                if col < grid_object.getGridLen() - 1:
                    print(" ", end="")
                else:
                    print()
            else:
                print(chr(6) * (cell_size + 2), end="")
                print(chr(21), end="")

    for row in range(grid_object.getGridLen()):

        if row % grid_object.getMiniSize()[0] == 0:  # Ceiling
            print_top_line()
        elif row % grid_object.getMiniSize()[0] <= grid_object.getMiniSize()[0] - 1:
            print_middle_line()

        print_number_line(row)

        if row % grid_object.getMiniSize()[0] == grid_object.getMiniSize()[0] - 1:
            print_bottom_line()


def displayInfo(grid_object, display_zeros=True, indicate_uneditables=True, spaces=3):
    """
    Function for displaying overall information about the Grid object
    """
    print(" " * spaces, "---------------------------------------", sep="")
    print(" " * spaces, "Overall Size (Row,Column): ",
          grid_object.getGridLen(), " x ", grid_object.getGridLen(), sep="")
    print(" " * spaces, "Mini Grid Size (Row,Column): ",
          grid_object.getMiniSize()[0], " x ", grid_object.getMiniSize()[1], sep="")
    print(" " * spaces, "Build Mode : ", grid_object.isBuilding(), sep="")
    print()
    print(" " * spaces, "Show 0 : ", bool(display_zeros), sep="")
    print(" " * spaces, "Indicate Non-Editable : ",
          indicate_uneditables, sep="")
    print(" " * spaces, "---------------------------------------", sep="")


def displayOptions(spaces=3):
    """
    Function for displaying options the user can choose from
    """
    print(" " * spaces, "0 : Quit", sep="")
    print(" " * spaces, "1 : Change Value", sep="")
    print(" " * spaces, "2 : Toggle Build Mode", sep="")
    print(" " * spaces,
          "3 : Clear Grid (Build : All Cells / Normal : Except Uneditables)\n", sep="")
    print(" " * spaces, "a : Show/Hide 0", sep="")
    print(" " * spaces, "b : Toggle Uneditable Indicator", sep="")
    print(" " * spaces, "n : Discard and Make a New Grid", sep="")


def clear():
    """
    Function for "flushing" the screen
    It's just many 'next-line's
    """
    print("\n"*100)


def changeValueMode(grid_object, spaces=3):
    """
    Function that provides interactive interface for changing Cell values
    """

    def changeValue(cRow, cCol):
        """
        Nested function that actually tries to change the value
        """
        clear()
        visualize_grid(grid_object, display_zeros=True, indicate_uneditables=True,
                       cursor=(True, cRow, cCol), spaces=spaces)
        print()
        print(" " * spaces, "( 'B' to go back )\n", sep="")
        val = input("Set Value to : ").replace(" ", "").lower()
        while (val != "b") and ((not val.isdigit()) or (len(val) > 1 and val[0] == "0")):
            clear()
            visualize_grid(grid_object, display_zeros=True, indicate_uneditables=True, cursor=(
                True, cRow, cCol), spaces=spaces)
            print()
            print(" " * spaces, "( 'B' to go back )\n", " " * spaces,
                  "Please enter a non-negative integer for the Value\n", sep="")
            val = input("Set Value to : ").replace(" ", "").lower()
        if val != "b":
            val = int(val)
            grid_object.setValueAt(cRow, cCol, val)

    back = False
    (cRow, cCol) = (0, 0)
    while back is False:
        clear()
        visualize_grid(grid_object, display_zeros=True, indicate_uneditables=True,
                       cursor=(True, cRow, cCol), spaces=spaces)
        cellInfo(grid_object.getCellAt(cRow, cCol))
        print(" " * spaces,
              "*-----------------------( Case Does Not Matter )-----------------------*", sep="")
        print(" " * spaces,
              "W,A,S,D : Move the Cursor UP/LEFT/DOWN/RIGHT  (Combinations are allowed)", sep="")
        print(" " * spaces, "(Enter) : Change the Value", sep="")
        print(" " * spaces, "BACK : Go Back to the Main Interface", sep="")
        print(" " * spaces,
              "*----------------------------------------------------------------------*\n", sep="")
        ctrl = input("Control : ").replace(" ", "").lower()

        if ctrl == "":
            changeValue(cRow, cCol)
        elif ctrl == "back":
            back = True
        elif all([c in "wasd" for c in ctrl]):
            rowInc = ctrl.count("s") - ctrl.count("w")
            colInc = ctrl.count("d") - ctrl.count("a")
            cRow = (cRow + rowInc) % grid.getGridLen()
            cCol = (cCol + colInc) % grid.getGridLen()


if __name__ == "__main__":
    screen_position = 3
    show_zero = True
    indicateUneditable = True
    quitting = False

    (rows, cols) = row_col_input()
    grid = Grid(rows, cols)

    while quitting is False:
        clear()
        visualize_grid(grid, display_zeros=show_zero,
                       indicate_uneditables=indicateUneditable, spaces=screen_position)
        print("\n")
        displayInfo(grid, show_zero, indicateUneditable, screen_position)
        print()
        displayOptions(screen_position)
        print("\n")
        choice = input("Select an option : ")

        if choice == "0":
            clear()
            sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
            while sure not in ("y", "n"):
                clear()
                sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
            if sure == "y":
                quitting = True
            else:
                pass
        elif choice == "1":
            changeValueMode(grid, screen_position)
        elif choice == "2":
            grid.toggleBuildMode()
        elif choice == "3":
            grid.clearGrid()
        elif choice == "a":
            show_zero = not show_zero
        elif choice == "b":
            indicateUneditable = not indicateUneditable
        elif choice == "n":
            clear()
            sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
            while sure not in ("y", "n"):
                clear()
                sure = input("Are you sure (y/n) : ").lower().replace(" ", "")
            if sure == "y":
                (rows, cols) = row_col_input()
                grid = Grid(rows, cols)
            else:
                pass
