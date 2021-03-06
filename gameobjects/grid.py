"""
This module contains Grid class
"""
try:
    from gameobjects.cell import Cell
except ModuleNotFoundError:
    from cell import Cell

class Grid:
    """
    Collection of Cell objects and methods for manipulating and getting information out of them
    """
    def __init__(self, miniGridRows, miniGridColumns):
        if (not isinstance(miniGridRows, int)) or (not isinstance(miniGridColumns, int)):
            raise TypeError("Number of rows and columns must be both integers")
        else:
            self.__miniRow = miniGridRows
            self.__miniCol = miniGridColumns
            self.__gridLength = miniGridRows * miniGridColumns
            self.__bigGrid = tuple(Cell(maxVal=self.__gridLength) for num in range(self.__gridLength ** 2))

            for cell in self.__bigGrid:
                cell.setPossibles("".join(list(f"#{x}" for x in range(1, self.__gridLength + 1))))

            self.__miniGrids = [[] for mini in range(self.__miniRow * self.__miniCol)]
            for row in range(self.__gridLength):
                for col in range(self.__gridLength):
                    self.__miniGrids[((row // self.__miniRow) * self.__miniRow) + (col // self.__miniCol)
                                    ].append(self.__bigGrid[(row * self.__gridLength) + col])

            self.__buildMode = False

    def getGridLen(self):
        """
        getGridLen()

        Returns the length of the side of the grid as an integer
        """
        return self.__gridLength

    def getMiniSize(self):
        """
        getMiniSize()

        Returns the size of mini grids as (Rows, Columns)
        """
        return (self.__miniRow, self.__miniCol)

    def setValueAt(self, row, column, value):
        """
        setValueAt(int, int, int)

        Sets the value of a Cell object located in a specific position
        If the value of row or column is invalid, does nothing
        """
        if (isinstance(row, int)) and (isinstance(column, int)) and (isinstance(value, int)) and (0 <= row < self.__gridLength) and (0 <= column < self.__gridLength):
            self.__bigGrid[row * self.__gridLength + column].setValue(int(value))
            self.refreshPossibles(row, column)

    def getValueAt(self, row, column):
        """
        getValueAt(int, int)

        Returns the value of a Cell object located in a specific position
        If the value of row or column is invalid, returns 0
        """
        if isinstance(row, int) and isinstance(column, int) and (0 <= row < self.__gridLength) and (0 <= column < self.__gridLength):
            val = self.__bigGrid[row * self.__gridLength + column].getValue()
        else:
            val = 0
        return val

    def getAllValues(self):
        """
        getAllValues()

        Returns a string that contains all values of cells in the grid in order
        """
        values = ""
        for cell in self.__bigGrid:
            values += str(cell.getValue())
        return values

    def isEditableAt(self, row, column):
        """
        isEditableAt(int, int)

        Returns a boolean that indicates whether that cell is editable or not
        True if the cell is editable
        False if the cell is not editable or the inputs are invalid
        """
        if isinstance(row, int) and isinstance(column, int) and (0 <= row < self.__gridLength) and (0 <= column < self.__gridLength):
            editable = self.__bigGrid[9 * row + column].isEditable()
        else:
            editable = False
        return editable

    def getAllEditableStates(self):
        """
        getAllEditableStates()

        Returns a string with 0s and 1s indicating which cell is editable
        """
        editable_states = ""
        for cell in self.__bigGrid:
            editable_states += str(int(cell.isEditable()))
        return editable_states

    def isBuilding(self):
        """
        isBuilding()

        Returns a boolean that indicates whether the build mode is on or off
        True if the build mode is on
        False otherwise
        """
        return self.__buildMode

    def toggleBuildMode(self):
        """
        toggleBuildMode()

        If the build mode is False, set it to True and make all cells editable
        If the build mode is True, set it to False and finalize the grid
        """
        self.__buildMode = not self.__buildMode
        if self.__buildMode is True:
            for cell in self.__bigGrid:
                cell.setEditable(True)
        else:
            self.__finalizeGrid()
            self.refreshPossibles()

    def clearGrid(self):
        """
        clearGrid()

        Sets all values of editable cells to 0
        """
        for cell in self.__bigGrid:
            cell.setValue(0)
        self.refreshPossibles()

    def isSolved(self):
        """
        isSolved()

        Returns True if the puzzle is solved
        Returns False otherwise
        """
        solved = True
        for cell in self.__bigGrid:
            if not len(cell.getPossibles().split("#")) == 2:
                solved = False
                break
            elif cell.getValue() != int(cell.getPossibles().split("#")[1]):
                solved = False
                break
        return solved

    def isSolvable(self):
        """
        isSolvable()

        Returns True if the puzzle can be solved with the current grid
        Returns False otherwise
        """
        solvable = True
        for cell in self.__bigGrid:
            if cell.getValue() != 0 and ("#" + str(cell.getValue())) not in cell.getPossibles():
                solvable = False
                break
        return solvable

    def fundamentallyImpossible(self):
        """
        fundamentallyImpossible()

        Returns True if the puzzle cannot be solved anyhow
        False if that's not the case
        """
        if any(cell.getValue() != 0 and cell.isEditable() for cell in self.__bigGrid):
            simulated = Grid(self.__miniRow, self.__miniCol)
            for row in range(self.__gridLength):
                for col in range(self.__gridLength):
                    cell = self.__bigGrid[self.__gridLength * row + col]
                    if not cell.isEditable() and cell.getValue() != 0:
                        simulated.setValueAt(row, col, cell.getValue())
        else:
            simulated = self
        return not simulated.isSolvable()

    def bruteSolve(self):
        """
        bruteSolve()

        Solves the puzzle using brute force search
        """
        if not self.fundamentallyImpossible() and not self.isSolved():
            if self.__buildMode is True:
                self.toggleBuildMode()
            self.clearGrid()
            minPossibleLen = 10
            minPossibleCell = None
            cellsInProcess = []
            for cell in self.__bigGrid:
                if cell.isEditable() and len(cell.getPossibles().split("#")[1:]) < minPossibleLen:
                    minPossibleCell = cell
                    minPossibleLen = len(cell.getPossibles().split("#")[1:])
            if minPossibleCell is not None:
                cellsInProcess.append((minPossibleCell, minPossibleCell.getPossibles().split("#")[1:]))
            while cellsInProcess != [] and not self.isSolved():
                if cellsInProcess[-1][1] == []:
                    currentCell = cellsInProcess.pop(-1)[0]
                    currentCell.setValue(0)
                    self.refreshPossibles(self.__bigGrid.index(currentCell) // self.__gridLength, self.__bigGrid.index(currentCell) % self.__gridLength)
                else:
                    currentCell = cellsInProcess[-1][0]
                    currentVal = int(cellsInProcess[-1][1].pop(0))
                    currentCell.setValue(currentVal)
                    self.refreshPossibles(self.__bigGrid.index(currentCell) // self.__gridLength, self.__bigGrid.index(currentCell) % self.__gridLength)
                    if self.isSolvable():
                        minPossibleLen = 10
                        minPossibleCell = None
                        for cell in (cell for cell in self.__bigGrid if cell not in (processingCell[0] for processingCell in cellsInProcess)):
                            if cell.isEditable() and len(cell.getPossibles().split("#")[1:]) < minPossibleLen:
                                minPossibleCell = cell
                                minPossibleLen = len(cell.getPossibles().split("#")[1:])
                        if minPossibleCell is not None:
                            cellsInProcess.append((minPossibleCell, minPossibleCell.getPossibles().split("#")[1:]))
            if not self.isSolved():
                self.clearGrid()

    def refreshPossibles(self, *row_col):
        """
        refreshPossibles()          all cells
        refreshPossibles(int, int)  based on the specified location

        Sets correct possibles strings for every cell
        If row and column are given as row_col, refreshes only those that are in the same row, column, or mini grid as the specified cell
        """
        def collectOtherValues(row, col):
            """
            Nested function for getting values of other cells in the same row, column, or mini grid
            """
            thisCell = self.__bigGrid[(row * self.__gridLength) + col]
            otherValues = set()
            for cell in self.__getRow(row):
                if cell != thisCell:
                    otherValues.add(cell.getValue())
            for cell in self.__getCol(col):
                if cell != thisCell:
                    otherValues.add(cell.getValue())
            for cell in self.__getMiniGrid(row, col):
                if cell != thisCell:
                    otherValues.add(cell.getValue())
            return otherValues

        # If no argument is given, refresh all cells
        if row_col == ():
            for row in range(self.__gridLength):
                for col in range(self.__gridLength):
                    currentCell = self.__bigGrid[row * self.__gridLength + col]
                    otherVals = collectOtherValues(row, col)
                    possibles = set(range(1, self.__gridLength + 1)) - otherVals
                    currentCell.setPossibles("#" + "#".join([str(num) for num in sorted(possibles)]))

        # If two arguments are given as row and column
        elif (len(row_col) == 2) and isinstance(row_col[0], int) and isinstance(row_col[1], int) and (0 <= row_col[0] < self.__gridLength) and (0 <= row_col[1] < self.__gridLength):
            count = 0
            for cell in self.__getRow(row_col[0]):
                otherVals = collectOtherValues(row_col[0], count)
                possibles = set(range(1, self.__gridLength + 1)) - otherVals
                cell.setPossibles("#" + "#".join([str(num) for num in sorted(possibles)]))
                count += 1
            count = 0
            for cell in self.__getCol(row_col[1]):
                otherVals = collectOtherValues(count, row_col[1])
                possibles = set(range(1, self.__gridLength + 1)) - otherVals
                cell.setPossibles("#" + "#".join([str(num) for num in sorted(possibles)]))
                count += 1
            for cell in self.__getMiniGrid(row_col[0], row_col[1]):
                otherVals = collectOtherValues((self.__bigGrid.index(cell) // self.__gridLength), (self.__bigGrid.index(cell) % self.__gridLength))
                possibles = set(range(1, self.__gridLength + 1)) - otherVals
                cell.setPossibles("#" + "#".join([str(num) for num in sorted(possibles)]))

    def __finalizeGrid(self):
        """
        finalizeGrid()

        Internal function for finalizing the grid
        """
        for cell in self.__bigGrid:
            if cell.getValue() != 0:
                cell.setEditable(False)

    def __getRow(self, row):
        """
        getRow(int)

        Internal function that returns cells in the corresponding row
        """
        if isinstance(row, int) and (0 <= row < self.__gridLength):
            row_cells = self.__bigGrid[row * self.__gridLength: (row + 1) * self.__gridLength]
        else:
            row_cells = ()
        return row_cells

    def __getCol(self, col):
        """
        getCol(int)

        Internal function that returns cells in the corresponding column
        """
        if isinstance(col, int) and (0 <= col < self.__gridLength):
            col_cells = self.__bigGrid[col: self.__gridLength ** 2: self.__gridLength]
        else:
            col_cells = ()
        return col_cells

    def __getMiniGrid(self, row, col):
        """
        getMiniGrid(int, int)

        Internal function that returns cells in the mini grid the given location is in
        """
        if isinstance(row, int) and isinstance(col, int) and (0 <= row < self.__gridLength) and (0 <= col < self.__gridLength):
            mini_grid = self.__miniGrids[((row // self.__miniRow) * self.__miniRow) + (col // self.__miniCol)]
        else:
            mini_grid = ()
        return mini_grid
