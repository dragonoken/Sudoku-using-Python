"""
This module contains Game class for 9x9 size square Sudoku
"""

import os
import os.path
from random import randint
try:
    from gameobjects.grid import Grid
except ModuleNotFoundError:
    from grid import Grid

class Game:
    """
    Game class is basically the middleman between Grid and the user interaction
    This class takes care of interactions with the grid

    Specifically for 9x9 sudoku puzzle with 3x3 mini grids
    """
    def __init__(self):
        self.__savePath = os.path.dirname(os.path.abspath(__file__))[:-12] + "\\saves"
        self.__puzzlePath = os.path.dirname(os.path.abspath(__file__))[:-12] + "\\puzzles"
        self.__gamegrid = None
        self.__currentlySaved = True
        self.__maxUndo = 30
        self.__undo = []
        self.__redo = []

    def newGrid(self, build=False):
        """
        newGrid()

        Makes a new empty grid
        If build is True, turns on the build mode
        """
        self.__gamegrid = Grid(3, 3)
        if build is True:
            if not self.__gamegrid.isBuilding():
                self.__gamegrid.toggleBuildMode()

    def setValueAt(self, row, column, value):
        """
        setValueAt(int, int, int)

        Sets the value of a cell
        When changes are being made, adds the previous value to the undo list
        Does nothing if:
            1)  there is no current grid
            2)  the input value equals the current value of the cell
            3)  the cell is not editable
            4)  the inputs for row and column are invalid
        """
        if self.__gamegrid is not None:
            if isinstance(row, int) and isinstance(column, int) and (0 <= row < self.__gamegrid.getGridLen()) and (0 <= column < self.__gamegrid.getGridLen()):
                if self.__gamegrid.isEditableAt(row, column):
                    if self.__gamegrid.getValueAt(row, column) != value:
                        self.__undo.append((row, column, self.__gamegrid.getValueAt(row, column)))
                        if len(self.__undo) > self.__maxUndo:
                            self.__undo.pop(0)
                        self.__redo.clear()
                        self.__gamegrid.setValueAt(row, column, value)
                        self.__currentlySaved = False

    def undo(self):
        """
        undo()

        Reverts the last change made to the grid
        Does nothing if the current grid is None
        """
        if self.__gamegrid is not None:
            rcv = self.__undo.pop()
            self.__redo.append((rcv[0], rcv[1], self.__gamegrid.getValueAt(rcv[0], rcv[1])))
            self.setValueAt(rcv[0], rcv[1], rcv[2])

    def undoable(self):
        """
        undoable()

        Returns a boolean
        True if the undo list is not empty
        False otherwise
        """
        return self.__undo != []

    def redo(self):
        """
        redo()

        Reverts the last undo done to the grid
        Does nothing if the current grid is None
        """
        if self.__gamegrid is not None:
            rcv = self.__redo.pop()
            self.__undo.append((rcv[0], rcv[1], self.__gamegrid.getValueAt(rcv[0], rcv[1])))
            self.setValueAt(rcv[0], rcv[1], rcv[2])

    def redoable(self):
        """
        redoable()

        Returns a boolean
        True if the redo list is not empty
        False otherwise
        """
        return self.__redo != []

    def exitGrid(self):
        """
        exitGrid()

        Sets the current grid to None and clears undo and redo lists
        """
        self.__gamegrid = None
        self.__undo.clear()
        self.__redo.clear()
        self.__currentlySaved = True

    def getAllValues(self):
        """
        getAllValues()

        Gets all values of the cells in the current grid and returns a tuple of integers
        If the current grid does not exist, returns None
        """
        if self.__gamegrid is not None:
            vals = tuple(int(val) for val in self.__gamegrid.getAllValues())
        else:
            vals = None
        return vals

    def getAllEditableStates(self):
        """
        getAllEditableStates()

        Gets all editable states of the cells in the current grid and returns a tuple of booleans
        If the current grid does not exist, returns None
        """
        if self.__gamegrid is not None:
            editables = tuple(bool(int(edit)) for edit in self.__gamegrid.getAllEditableStates())
        else:
            editables = None
        return editables

    def isSolved(self):
        """
        isSolved()

        Returns a boolean
        True if the current grid, or puzzle, is solved
        False if the current grid is not solved or does not exist
        """
        if self.__gamegrid is not None:
            solved = self.__gamegrid.isSolved()
        else:
            solved = False
        return solved

    def isSolvable(self):
        """
        isSolvable()

        Returns a boolean
        True if the current grid can be solved with the current state
        False if the current grid cannot be solved without changing existing values or does not exist
        """
        if self.__gamegrid is not None:
            solvable = self.__gamegrid.isSolvable()
        else:
            solvable = False
        return solvable

    def isImpossible(self):
        """
        isImpossible()

        Returns a boolean
        True if the current puzzle is just impossible to solve or does not exist in the first place
        False otherwise
        """
        if self.__gamegrid is not None:
            impossible = self.__gamegrid.fundamentallyImpossible()
        else:
            impossible = True
        return impossible

    def currentGameExists(self):
        """
        currentGameExists()

        Returns a boolean
        True if the game grid is not None
        False otherwise
        """
        return self.__gamegrid is not None

    def lastGameExists(self):
        """
        lastGameExists()

        Returns a boolean
        True if "autosave.assv" exists and is written in a correct format
        False otherwise
        """
        return os.path.exists(self.__savePath + "\\autosave.assv") and self.__checkSaveFormat("\\autosave.assv")

    def isSaved(self):
        """
        isSaved()

        Returns a boolean
        True if the current state of the game is saved
        False otherwise
        """
        return self.__currentlySaved

    def saveGame(self, *save_name):
        """
        saveGame()      autosave(temporary)
        saveGame(str)   saves as (str)

        Saves the current state of the puzzle grid as 'save_name.ssv' to the save directory if save_name is given
        If the save_name is not given, saves the current puzzle as 'autosave.assv'
        If the save directory does not exist, makes one
        If the current grid does not exist, does nothing

        Note::If the save file name is not valid, it does nothing
              If there is a save file with the same name, it will override it
        """
        if self.__gamegrid is not None:
            if (len(save_name) >= 1 and all(letter not in '\\/:*?"<>|' for letter in str(save_name[0]))) or save_name == ():
                all_values = self.__gamegrid.getAllValues()
                editable_states = self.__gamegrid.getAllEditableStates()
                bi_log, chr_log = "", ""
                for bi in (bin(int(n))[2:] for n in all_values):
                    bi_log += "0" * (4 - len(bi)) + bi
                for is_original in (int(editable == "0") for editable in editable_states):
                    bi_log += str(is_original)
                for r in (randint(0, 1) for left_over_spaces in range(len(bi_log) % 8)):
                    bi_log += str(r)
                for byte in (bi_log[8 * l:8 * (l + 1)] for l in range(len(bi_log) // 8)):
                    chr_log += chr(int(byte, 2))
                if not os.path.exists(self.__savePath):
                    os.mkdir(self.__savePath)
                if len(save_name) >= 1:
                    with open(self.__savePath + "\\" + str(save_name[0]) + ".ssv", mode="w", encoding="utf8") as save:
                        save.write(chr_log)
                    self.__currentlySaved = True
                else:
                    with open(self.__savePath + "\\autosave.assv", mode="w", encoding="utf8") as save:
                        save.write(chr_log)

    def savePuzzle(self, puzzle_name):
        """
        savePuzzle(str)

        Saves the current state of the puzzle grid that is being built or edited as 'puzzle_name.pzl' to the puzzle directory
        If the puzzle directory does not exist, makes one
        If the current grid does not exist, does nothing

        Note::If the puzzle file name is not valid, it does nothing
              If there is a puzzle file with the same name, it will override it
        """
        if self.__gamegrid is not None:
            if all(letter not in '\\/:*?"<>|' for letter in str(puzzle_name[0])):
                all_values = self.__gamegrid.getAllValues()
                bi_log, chr_log = "", ""
                for bi in (bin(int(n))[2:] for n in all_values):
                    bi_log += "0" * (4 - len(bi)) + bi
                for r in (randint(0, 1) for left_over_spaces in range(len(bi_log) % 8)):
                    bi_log += str(r)
                for byte in (bi_log[8 * l:8 * (l + 1)] for l in range(len(bi_log) // 8)):
                    chr_log += chr(int(byte, 2))
                if not os.path.exists(self.__puzzlePath):
                    os.mkdir(self.__puzzlePath)
                with open(self.__puzzlePath + "\\" + puzzle_name + ".pzl", mode="w", encoding="utf8") as puzzle:
                    puzzle.write(chr_log)
                self.__currentlySaved = True

    def getSaves(self):
        """
        getSaves()

        Returns a tuple containing the names of saved game files without file extensions
        If there is no save file or save directory, returns None
        """
        if os.path.exists(self.__savePath) and tuple(save for save in os.scandir(path=self.__savePath) if save.name.endswith(".ssv")) != ():
            saves = tuple(save.name.replace(".ssv", "") for save in os.scandir(path=self.__savePath) if save.name.endswith(".ssv"))
        else:
            saves = None
        return saves

    def getPuzzles(self):
        """
        getPuzzles()

        Returns a tuple containing the names of saved puzzle files without file extensions
        If there is no puzzle file or puzzle directory, returns None
        """
        if os.path.exists(self.__puzzlePath) and tuple(puzzle for puzzle in os.scandir(path=self.__puzzlePath) if puzzle.name.endswith(".pzl")) != ():
            puzzles = tuple(puzzle.name.replace(".pzl", "") for puzzle in os.scandir(path=self.__puzzlePath) if puzzle.name.endswith(".pzl"))
        else:
            puzzles = None
        return puzzles

    def loadSave(self, *save_name):
        """
        loadSave([original_cells_only=bool])        loads autosave.assv
        loadSave(str[, original_cells_only=bool])   loads str.ssv

        Reads a save file and initiates a Grid object according to the information in the save file
        If no save_name is given, reads 'autosave.assv'

        If the save file does not exist or is written in a wrong format, set the current grid to None
        """
        if save_name != ():
            save_name = str(save_name[0]) + ".ssv"
        else:
            save_name = "autosave.assv"
        if os.path.exists(self.__savePath + "\\" + save_name) and self.__checkSaveFormat(save_name):
            with open(self.__savePath + "\\" + save_name, mode="r", encoding="utf8") as sf:
                chr_log = sf.read(100)
            bi_log, values = "", ""
            for character in chr_log[:51]:
                bi_log += "0" * (8 - len(bin(ord(character))[2:])) + bin(ord(character))[2:]
            for half_byte in (bi_log[4 * n: 4 * (n + 1)] for n in range(81)):
                values += str(int(half_byte, 2))
            editable_states = bi_log[4 * 81 + 1:4 * 81 + 82]
            self.__gamegrid = Grid(3, 3)
            self.__gamegrid.toggleBuildMode()
            for row in range(9):
                for col in range(9):
                    self.__gamegrid.setValueAt(row, col, int(values[9 * row + col]) * int(editable_states[9 * row + col]))
            self.__gamegrid.toggleBuildMode()
            for row in range(9):
                for col in range(9):
                    self.__gamegrid.setValueAt(row, col, int(values[9 * row + col]))
        else:
            self.__gamegrid = None
        self.__currentlySaved = True

    def loadPuzzle(self, puzzle_name, editing=False):
        """
        loadPuzzle(str)

        Reads a puzzle file and initiates a Grid object according to the information in the puzzle file

        If editing is True, sets all cells to be editable

        If the puzzle file does not exist or is written in a wrong format, set the current grid to None
        """
        puzzle_name = puzzle_name + ".pzl"
        if os.path.exists(self.__puzzlePath + "\\" + puzzle_name) and self.__checkSaveFormat(puzzle_name):
            with open(self.__puzzlePath + "\\" + puzzle_name, mode="r", encoding="utf8") as pz:
                chr_log = pz.read(100)
            bi_log, values = "", ""
            for character in chr_log[:41]:
                bi_log += "0" * (8 - len(bin(ord(character))[2:])) + bin(ord(character))[2:]
            for half_byte in (bi_log[4 * n:4 * (n + 1)] for n in range(81)):
                values += str(int(half_byte, 2))
            self.__gamegrid = Grid(3, 3)
            self.__gamegrid.toggleBuildMode()
            for row in range(9):
                for col in range(9):
                    self.__gamegrid.setValueAt(row, col, int(values[9 * row + col]))
            print(self.__gamegrid.isBuilding())
            if editing is not True:
                self.__gamegrid.toggleBuildMode()
                print(self.__gamegrid.isBuilding())
        else:
            self.__gamegrid = None
        self.__currentlySaved = True

    def __checkSaveFormat(self, file_name):
        """
        checkSaveFormat(str)    checks the file named (str)

        Internal function that checks if the saved file is written in a correct format
        Returns a boolean
        True if the file is in correct format
        False otherwise, including the case where the file does not exist
        """
        valid = True
        if file_name.endswith(".ssv") or file_name.endswith(".assv"):
            path = self.__savePath
        elif file_name.endswith(".pzl"):
            path = self.__puzzlePath
        else:
            valid = False
        if valid is True:
            with open(path + "\\" + file_name, encoding="utf8") as save:
                raw = save.read(100)
            if file_name.endswith(".pzl") and len(raw) != 41:
                valid = False
            elif (file_name.endswith(".ssv") or file_name.endswith(".assv")) and len(raw) != 51:
                valid = False
            else:
                bi = "".join("0" * (8 - len(str(bin(ord(raw_chr))[2:]))) + str(bin(ord(raw_chr))[2:]) for raw_chr in raw)
                vals = tuple(int(bi[n * 4:(n + 1) * 4], 2) for n in range(81))
                if any(num < 0 or num > 9 for num in vals):
                    valid = False
                elif any(vals.count(val) > 9 for val in range(1, 10)):
                    valid = False
        return valid
        