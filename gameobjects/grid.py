from cell import Cell

class Grid:
	def __init__(self, miniGridRows, miniGridColumns):
		if ( not isinstance(miniGridRows, int) ) or ( not isinstance(miniGridColumns, int) ):
			raise TypeError("Number of rows and columns must be both integers")
		else:
			self.__miniRow = miniGridRows
			self.__miniCol = miniGridColumns
			self.__gridLength = miniGridRows * miniGridColumns
			self.__bigGrid = tuple( Cell( maxVal=self.__gridLength ) for num in range(self.__gridLength ** 2))

			for cell in self.__bigGrid:
				cell.setPossibles( "".join( list( f"#{x}" for x in range(1, self.__gridLength + 1) ) ) )

			self.__miniGrids = [ [] for mini in range( self.__miniRow * self.__miniCol ) ]
			for row in range( self.__gridLength ):
				for col in range ( self.__gridLength ):
					self.__miniGrids[ ( ( row // self.__miniRow ) * self.__miniRow ) + ( col // self.__miniCol ) ].append(self.__bigGrid[ ( row * self.__gridLength ) + col ])

			self.__buildMode = False

	def getGridLen(self):
		"""Returns the length of the side of the grid as an integer"""
		return self.__gridLength

	def getMiniSize(self):
		"""Returns the size of mini grids as (Rows, Columns)"""
		return (self.__miniRow, self.__miniCol)

	def setValueAt(self, row, col, value):
		if ( isinstance(row, int) ) and ( isinstance(col, int) ) and ( isinstance(value, int) ) and ( 0 <= row < self.__gridLength ) and ( 0 <= col < self.__gridLength ):
			self.__bigGrid[row * self.__gridLength + col].setValue(int(value))
			self.__refreshPossibles(row, col)

	def getValueAt(self, row, col):
		if 0 <= row < self.__gridLength and 0 <= col < self.__gridLength:
			return self.__bigGrid[row * self.__gridLength + col].getValue()

	def toggleBuildMode(self):
		self.__buildMode = not self.__buildMode
		if self.__buildMode == True:
			for cell in self.__bigGrid:
				cell.setEditable(True)
		else:
			self.__finalizeGrid()

	def clearGrid(self):
		if self.__buildMode == True:
			for cell in self.__bigGrid:
				cell.setEditable(True)
				cell.setValue(0)
		else:
			for cell in self.__bigGrid:
				cell.setValue(0)
		self.__refreshPossibles()

	def isSolved(self):
		solved = True
		for cell in self.__bigGrid:
			if ( len( cell.getPossibles().split("#") ) == 2 ) and ( cell.getValue() == int( cell.getPossibles().split("#")[1] ) ):
				solved = False
				break
		return solved

	def __refreshPossibles(self, *rc):

		def collectOtherValues(row, col):
			if ( isinstance(row, int) ) and ( isinstance(col, int) ) and ( 0 <= row < self.__gridLength ) and ( 0 <= col < self.__gridLength ):
				thisCell = self.__bigGrid[ ( row * self.__gridLength ) + col ]
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

		if len(rc) == 0: #If no argument is given, refresh all cells
			for row in range(self.__gridLength):
				for col in range(self.__gridLength):
					currentCell = self.__bigGrid[ row * self.__gridLength + col ]
					otherVals = collectOtherValues(currentCell, row, col)
					possibles = set( range( 1, self.__gridLength + 1 ) ) - otherVals
					currentCell.setPossibles( "#" + "#".join( [ str(num) for num in sorted( possibles ) ] ) )

		#If two arguments are given as row and column
		elif ( len(rc) == 2 ) and ( isinstance(rc[0], int) ) and ( isinstance(rc[1], int) ) and ( 0 <= rc[0] < self.__gridLength ) and ( 0 <= rc[1] < self.__gridLength ):
			count = 0
			for cell in self.__getRow(rc[0]):
				otherVals = collectOtherValues(rc[0], count)
				possibles = set( range( 1, self.__gridLength + 1 ) ) - otherVals
				cell.setPossibles( "#" + "#".join( [ str(num) for num in sorted( possibles ) ] ) )
				count += 1
			count = 0
			for cell in self.__getCol(rc[1]):
				otherVals = collectOtherValues(count, rc[1])
				possibles = set( range( 1, self.__gridLength + 1 ) ) - otherVals
				cell.setPossibles( "#" + "#".join( [ str(num) for num in sorted( possibles ) ] ) )
				count += 1
			for cell in self.__getMiniGrid(rc[0], rc[1]):
				otherVals = collectOtherValues(( self.__bigGrid.index(cell) // self.__gridLength ), ( self.__bigGrid.index(cell) % self.__gridLength ))
				possibles = set( range( 1, self.__gridLength + 1 ) ) - otherVals
				cell.setPossibles( "#" + "#".join( [ str(num) for num in sorted( possibles ) ] ) )

	def __finalizeGrid(self):
		if self.__buildMode == True:
			for cell in self.__bigGrid:
				if cell.getValue() != 0:
					cell.setEditable(False)

	def __getRow(self, row): #Get the cells of the corresponding row number
		if isinstance(row, int) and 0 <= row < self.__gridLength:
			return self.__bigGrid[ row * self.__gridLength : ( row + 1 ) * self.__gridLength ]

	def __getCol(self, col): #Get the cells of the corresponding column number
		if isinstance(col, int) and 0 <= col < self.__gridLength:
			return self.__bigGrid[ col : self.__gridLength ** 2 : self.__gridLength ]

	def __getMiniGrid(self, row, col): #Get all the cells in the mini grid where the coordinates are located in
		if isinstance(row, int) and isinstance(col, int) and 0 <= row < self.__gridLength and 0 <= col < self.__gridLength:
			return self.__miniGrids[ ( ( row // self.__miniRow ) * self.__miniRow ) + ( col // self.__miniCol ) ]