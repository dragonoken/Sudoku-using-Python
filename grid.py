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

			self.__miniGrids = tuple( tuple( self.__bigGrid[c] for c in range( len(self.__bigGrid) ) if
				( self.__miniCol * ( mg % ( self.__gridLength // self.__miniCol ) ) ) <= c % self.__gridLength < ( self.__miniCol * ( mg % ( self.__gridLength // self.__miniCol ) + 1 ) ) #Column of the Cell within the boundary
				and ( self.__miniRow * ( mg // ( self.__gridLength // self.__miniRow ) ) ) <= c // self.__gridLength < ( self.__miniRow * ( mg % ( self.__gridLength // self.__miniRow ) ) + 1 ) ) #Row of the Cell within the boundary
				 for mg in range( len(self.__bigGrid) // (self.__miniRow * self.__miniCol) )   )

			self.__buildMode = False

	def getGridLen(self):
		"""Returns the length of the side of the grid as an integer"""
		return self.__gridLength

	def getMiniSize(self):
		"""Returns the size of mini grids as (Rows, Columns)"""
		return (self.__miniRow, self.__miniCol)

	def setValueAt(self, row, col, value):
		if 0 <= row < self.__gridLength and 0 <= col < self.__gridLength:
			self.__bigGrid[row * self.__gridLength + col].setValue(int(value))

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

	def __finalizeGrid(self):
		if self.__buildMode == True:
			for cell in self.__bigGrid:
				if cell.getValue() != 0:
					cell.setEditable(False)