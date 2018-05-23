"""
This module contains Cell class
"""
class Cell:
    """
    The building block of the entire sudoku puzzle structure
    Contains minimum and maximum value, current value, string of possible values,
     and editable state
    """
    def __init__(self, minVal=0, maxVal=9):
        if minVal > maxVal:
            raise ValueError
        elif not isinstance(minVal, int) or not isinstance(maxVal, int):
            raise TypeError
        self.__minVal = minVal
        self.__maxVal = maxVal
        self.__value = 0
        self.__possibles = ""
        self.__editable = True

        self.__initPossibles()

    def __initPossibles(self):
        possibles = ""
        for num in range(self.__minVal, self.__maxVal + 1):
            possibles += f"#{num}"
        self.setPossibles(possibles)

    def setValue(self, num):
        """
        Sets the value of the cell
        The value must be between the minimum value and maximum value, including both ends
        If the cell's editable state is False, or the argument is not an integer, does nothing
        """
        if (self.__editable is True) and isinstance(num, int) and (self.__minVal <= num <= self.__maxVal):
            self.__value = num
        else:
            pass

    def getValue(self):
        """
        Returns the value of the cell
        """
        return self.__value

    def setPossibles(self, possibles):
        """
        Takes a string as the argument
        According to the string, sets the 'possibles' string
        """
        # Make sure it is in a string form
        possibles = str(possibles)
        # If '#' is not in the string and the string consists of only digits,
        # it assumes that the values are all 1-digit length
        if "#" not in possibles and possibles.isdigit():
            # Making sure no number is repeating,
            # then sorting in order, then put "#"s between digits... ----------(1)
            self.__possibles = "#" + "#".join(str(num) for num in sorted(int(string) for string in set(possibles)))
        # If the string has nothing or nothing except '#'s or empty spaces,
        # then the possibles are nothing
        elif possibles.replace(" ", "").replace("#", "") == "":
            self.__possibles = ""
        # In cases where there are "#"s separating numbers (However many #s are separating numbers!)
        elif ("#" in possibles) and "".join(possibles.split("#")).isdigit():
            # Make sure there is no #s next to each other before being processed
            while possibles.count("##") != 0:
                possibles = possibles.replace("##", "#")
            # If the string does not start with #,
            # it will count all each digit before # as a single number
            if possibles[0] != "#":
                # Basically a more complex version of (1) few lines above
                self.__possibles = "#" + "#".join(str(num) for num in sorted(int(string) for string in set(possibles.split("#")[0]).union(set(possibles.split("#")[1:]))))
            else:
                # Similar
                self.__possibles = "#" + "#".join(str(num) for num in sorted(int(string) for string in set(possibles.split("#")[1:])))
        else:  # Otherwise, it will not take the input
            pass

    def getPossibles(self):
        """
        Returns 'possibles' string
        """
        return self.__possibles

    def setEditable(self, tf):
        """
        Takes boolean
        Sets the editable state of the cell
        """
        self.__editable = bool(tf)

    def isEditable(self):
        """
        Returns the cell's editable state
        """
        return self.__editable
