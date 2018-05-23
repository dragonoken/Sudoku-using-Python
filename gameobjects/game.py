"""
This module contains Game class for 9x9 size square Sudoku
"""

import os
import os.path
from random import randint
from grid import Grid

class Game:
    """
    Game class is basically the middleman between Grid and the user interaction
    This class takes care of interactions with the grid

    Specifically for 9x9 sudoku puzzle with 3x3 mini grids
    """
    def __init__(self):
        self.__savePath = os.path.dirname(os.path.abspath(__file__)) + "\\saves"
        self.__gamegrid = None

    def getAllValues(self):
        """
        Gets all values of the current grid and returns a list of values
        If the current grid does not exist, returns None
        """
        if self.currentGridExists():
            vals = []
            for row in range(9):
                for col in range(9):
                    vals.append(self.__gamegrid.getValueAt(row, col))
        else:
            vals = None
        return vals

    def currentGridExists(self):
        """
        Returns boolean
        True if a grid exists in the game program
        False otherwise
        """
        return not self.__gamegrid is None

    def save(self, *save_name):
        """
        Saves the current state of the puzzle grid as 'save_name.ssv' to the save directory if save_name is given
        If the save_name is not given, saves the current puzzle as 'autosave.asv'
        If the save directory does not exist, makes one
        If the current grid does not exist, does nothing

        Note::If the save file name is not valid, it does nothing
              If there is a save file with the same name, it will override it
        """
        if self.__gamegrid != None:
            all_values, cleared_values = [], []
            for row in range(9):
                for col in range(9):
                    all_values.append(self.__gamegrid.getValueAt(row, col))
            self.__gamegrid.clearGrid()
            for row in range(9):
                for col in range(9):
                    cleared_values.append(self.__gamegrid.getValueAt(row, col))
                    if all_values[row * 9 + col] != cleared_values[row * 9 + col]:
                        self.__gamegrid.setValueAt(row, col, all_values[row * 9 + col])
            bi_log, chr_log = "", ""
            for bi in (bin(n)[2:] for n in all_values):
                bi_log += "0" * (4 - len(bi)) + bi
            for is_original in (int(x != 0 and x == y) for x, y in zip(all_values, cleared_values)):
                bi_log += str(is_original)
            for r in (randint(0, 1) for left_over_spaces in range(len(bi_log) % 8)):
                bi_log += str(r)
            for byte in (bi_log[8 * l:8 * (l + 1)] for l in range(len(bi_log) // 8)):
                chr_log += chr(int(byte, 2))
            if not os.path.exists(self.__savePath):
                os.mkdir(self.__savePath)
            if len(save_name) >= 1:
                if all(letter not in '\\/:*?"<>|' for letter in str(save_name[0])):
                    with open(self.__savePath + str(save_name[0]) + ".ssv", mode="w", encoding="utf8") as save:
                        save.write(chr_log)
            else:
                with open(self.__savePath + "autosave.asv", mode="w", encoding="utf8") as save:
                    save.write(chr_log)

    def getSaves(self):
        """
        Returns a tuple containing the names of save files without file extensions
        If there is no save file or save directory, returns None
        """
        if os.path.exists(self.__savePath) and tuple(save for save in os.scandir(path=self.__savePath) if save.name.endswith(".ssv")) != ():
            saves = tuple(save.name.replace(".ssv", "") for save in os.scandir(path=self.__savePath) if save.name.endswith(".ssv"))
        else:
            saves = None
        return saves

    def loadSave(self, *save_name, original_cells_only=False):
        """
        Reads a save file and initiates a Grid object according to the information in the save file
        If no save_name is given, reads 'autosave.asv'
        If original_cells_only is True, sets the value of the cells that are not changed during the game
        Otherwise, brings all the values

        If the save file does not exist or is written in a wrong format, set the current grid to None
        """
        if len(save_name) >= 1:
            save_name = str(save_name[0]) + ".ssv"
        else:
            save_name = "autosave.asv"
        if os.path.exists(self.__savePath + save_name) and self.__checkSaveFormat(save_name):
            with open(f"{save_name}.ssv", mode="r", encoding="utf8") as sf:
                chr_log = sf.read(100)
            bi_log, values = "", ""
            for character in chr_log[:52]:
                bi_log += bin(ord(character))[2:]
            for half_byte in (bi_log[4 * n: 4 * (n + 1)] for n in range(81)):
                values += str(int(half_byte, 2))
            editable_states = bi_log[4 * 81 + 1:4 * 81 + 82]
            self.__gamegrid = Grid(3, 3)
            self.__gamegrid.toggleBuildMode()
            for row in range(9):
                for col in range(9):
                    self.__gamegrid.setValueAt(row, col, int(values[9 * row + col]) * int(editable_states[9 * row + col]))
            self.__gamegrid.toggleBuildMode()
            if original_cells_only is False:
                for row in range(9):
                    for col in range(9):
                        self.__gamegrid.setValueAt(row, col, int(values[9 * row + col]))
        else:
            self.__gamegrid = None

    def __checkSaveFormat(self, save_name):
        """
        Internal function that checks if the save file is written in a correct format
        """
        valid = True
        with open(self.__savePath + save_name + ".ssv", encoding="utf8") as save:
            raw = save.read(100)
        if len(raw) != 51:
            valid = False
        else:
            bi = "".join("0" * (8 - len(str(bin(ord(raw_chr))[2:]))) + str(bin(ord(raw_chr))[2:]) for raw_chr in raw)
            vals = tuple(int(bi[n * 4:(n + 1) * 4], 2) for n in range(81))
            if any(num < 0 or num > 9 for num in vals):
                valid = False
        return valid
        