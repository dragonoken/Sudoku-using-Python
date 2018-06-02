from time import sleep
from random import randrange
from os import system
from gameobjects.game import Game

class Sudoku:
    """
    Text-Based Sudoku Puzzle Game Program! (User Interface part)
    """
    def __init__(self):
        #Shapes and some other stuff for text-based-art
        self.__shapes = {0:" ", "V":chr(5), "H":chr(6), 1:chr(3), 2:chr(4), 3:chr(2), 4:chr(1), 5:chr(25), 6:chr(21), 7:chr(23), 8:chr(22), 9:chr(16)}

        #The actual CORE of this program
        self.__game = Game()

        #Recommanded window size
        self.__changeScreen()
        input("Make sure\nyour console size\nis\nat least\n86 character wide\nand\n28 character tall\n\n\nPress Enter to Continue >>> ")

        #Go to the main menu (Actual start)
        self.__mainMenu()


    def __mainMenu(self):
        """
        mainMenu()

        Displays main menu options and takes an input, then it sends the user to a corresponding menu
        """
        #Dictionary of selectable main options
        menu = {"0":self.__quit, "1":self.__playOption, "2":self.__showRules}
        quitting = False

        while quitting is False:
            self.__changeScreen()
            self.__displayMain()

            choice = self.__optionChoice()
            while not self.__validOptChoice(choice, 0, 2):
                self.__changeScreen()
                self.__displayMain()
                choice = self.__optionChoice()

            chosen = menu[choice]

            if chosen == self.__quit:
                quitting = chosen()
            else:
                chosen()
        self.__exit()


    def __playOption(self):
        """
        playOption()

        Displays play options and takes an input, then it sends the user to a corresponding menu
        """
        back = False
        menu = {"0":"Back", "1":self.__newGame, "2":self.__loadSave, "3":self.__buildChoice, "c":self.__continue}

        while back is False:
            self.__changeScreen()
            self.__displayPlayOpt()

            choice = self.__optionChoice()
            while (choice != "c" and not self.__validOptChoice(choice, 0, 3)) or (choice == "c" and not self.__game.lastGameExists()):
                self.__changeScreen()
                self.__displayPlayOpt()
                choice = self.__optionChoice()

            chosen = menu[choice]

            if chosen == "Back":
                back = True
            else:
                chosen()


    def __continue(self):
        """
        continue()

        Loads the last game save file and starts the game
        """
        self.__game.loadSave()
        self.__play()


    def __newGame(self):
        """
        newGame()

        Loads a puzzle file and start a new game
        """
        self.__changeScreen()
        self.__showPuzzles()
        if self.__game.getPuzzles() is None:
            input("\n\n\nPress Enter to go back to the play menu >>>")
        else:
            puzzleChoice = input("\n(Press Enter to go back to the play menu)\nSelect a puzzle file number :").strip()
            while puzzleChoice != "" and (not puzzleChoice.isdigit() or (len(puzzleChoice) > 1 and puzzleChoice[0] == "0") or int(puzzleChoice) == 0 or int(puzzleChoice) > len(self.__game.getPuzzles())):
                self.__changeScreen()
                self.__showPuzzles()
                puzzleChoice = input("\n(Press Enter to go back to the play menu)\nSelect a puzzle file number :").strip()
            if puzzleChoice != "":
                self.__game.loadPuzzle(self.__game.getPuzzles()[int(puzzleChoice) - 1])
                self.__play()


    def __loadSave(self):
        """
        loadSave()

        Loads a saved game and continue
        """
        self.__changeScreen()
        self.__showSaves()
        if self.__game.getSaves() is None:
            input("\n\n\nPress Enter to go back to the play menu >>>")
        else:
            saveChoice = input("\n(Press Enter to go back to the play menu)\nSelect a save file number :").strip()
            while saveChoice != "" and (not saveChoice.isdigit() or (len(saveChoice) > 1 and saveChoice[0] == "0") or int(saveChoice) == 0 or int(saveChoice) > len(self.__game.getPuzzles())):
                self.__changeScreen()
                self.__showSaves()
                saveChoice = input("\n(Press Enter to go back to the play menu)\nSelect a save file number :").strip()
            if saveChoice != "":
                self.__game.loadSave(self.__game.getSaves()[int(saveChoice) - 1])
                self.__play(save=self.__game.getSaves()[int(saveChoice) - 1])


    def __buildChoice(self):
        """
        buildChoice()

        Loads an existing puzzle or make a new one
        """
        self.__changeScreen()
        self.__showPuzzles()
        print("\n\n(Press Enter to go back to the play menu)")
        if self.__game.getSaves is not None:
            print("Select a puzzle file number or ", end="")
        buildChoice = input("'N' to create a new puzzle :").strip().lower()
        while buildChoice != "" and buildChoice != "n" and (not buildChoice.isdigit() or (len(buildChoice) > 1 and buildChoice[0] == "0")
                                                            or int(buildChoice) == 0 or int(buildChoice) > len(self.__game.getPuzzles())):
            self.__changeScreen()
            self.__showPuzzles()
            print("\n\n(Press Enter to go back to the play menu)")
            if self.__game.getSaves is not None:
                print("Select a puzzle file number or ", end="")
            buildChoice = input("'N' to create a new puzzle :").strip().lower()
        if buildChoice != "":
            if buildChoice == "n":
                self.__game.newGrid(build=True)
                self.__buildEdit()
            else:
                puzzle = self.__game.getPuzzles()[int(buildChoice) - 1]
                self.__game.loadPuzzle(puzzle, editing=True)
                self.__buildEdit(puzzle=puzzle)


    def __play(self, save=None):
        """
        play([, save=str])  save : save file name without extension

        Play the current game
        If save file name is given, 'save to {save_name}' will be available
        """
        if not self.__game.currentGameExists():
            print("   *Failed to load the file*\n\n\n")
            input("Press Enter to go back to the play menu >>>")

        elif self.__game.isImpossible():
            self.__changeScreen()
            self.__visualizeGrid()
            print()
            print("   *This puzzle has no solution!*")
            print()
            input("Press Enter to go back to the play menu >>>")
        else:
            quitting = False
            rCursor = 0
            cCursor = 0
            solved = self.__game.isSolved()
            magic = 3
            while quitting is False and solved is False:
                self.__changeScreen()
                self.__visualizeGrid(cursor=(True, rCursor, cCursor))
                print()
                print("   W A S D : Move the cursor UP/LEFT/DOWN/RIGHT (combinations allowed)")
                print("    0 - 9  : Set the value of the cell (0 to empty the cell)")
                if self.__game.undoable():
                    print("      Z    : Undo")
                if self.__game.redoable():
                    print("      R    : Redo")
                print("      V    : Save the current game")
                print("      Q    : Quit the game and go back to the play menu")
                print()
                playerAction = input("Action :").replace(" ", "").lower()
                if len(playerAction) == 1 and playerAction not in "wasd":
                    if playerAction in "0123456789":
                        self.__game.setValueAt(rCursor, cCursor, int(playerAction))
                        solved = self.__game.isSolved()
                        if not solved:
                            self.__game.saveGame()
                    elif self.__game.undoable() and playerAction == "z":
                        self.__game.undo()
                        self.__game.saveGame()
                    elif self.__game.redoable() and playerAction == "r":
                        self.__game.redo()
                        self.__game.saveGame()
                    elif playerAction == "v":
                        save = self.__saving(puzzle=False, file=save)
                    elif playerAction == "q":
                        if self.__game.isSaved():
                            quitting = True
                        else:
                            self.__changeScreen()
                            print("   1 : Save and Quit")
                            print("   2 : Quit without Saving")
                            print("   0 : Back")
                            print("\n\n")
                            saveChoice = self.__optionChoice()
                            while not self.__validOptChoice(saveChoice, 0, 2):
                                self.__changeScreen()
                                print("   1 : Save and Quit")
                                print("   2 : Quit without Saving")
                                print("   0 : Back")
                                print("\n\n")
                                saveChoice = self.__optionChoice()
                            if saveChoice == "1":
                                save = self.__saving(puzzle=False, file=save)
                            elif saveChoice == "2":
                                quitting = True
                    magic = 3
                elif all(c in "wasd" for c in playerAction):
                    rCursor += playerAction.count("s") - playerAction.count("w")
                    cCursor += playerAction.count("d") - playerAction.count("a")
                    rCursor %= 9
                    cCursor %= 9
                    magic = 3
                elif playerAction in ("brute", "force", "incoming"):
                    if playerAction == "brute":
                        magic = 2
                    elif magic == 2 and playerAction == "force":
                        magic = 1
                    elif magic == 1 and playerAction == "incoming":
                        magic = 3
                        print("BRUTE FORCE SEARCH IN PROCESS... (This might take a while)")
                        self.__game.solve()
                        solved = self.__game.isSolved()
                    else:
                        magic = 3
                else:
                    magic = 3
            if solved is True:
                self.__changeScreen()
                self.__visualizeGrid()
                print("\n\n   *** Congratulations! ***")
                print("    You Solved The Puzzle!")
                input("\n\nPress enter to go back to the play menu >>>")
        self.__game.exitGrid()


    def __buildEdit(self, puzzle=None):
        """
        buildEdit()

        Build a new puzzle or edit an existing puzzle
        """
        if not self.__game.currentGameExists():
            print("   *Failed to load the file*\n\n\n")
            input("Press Enter to go back to the play menu >>>")
        else:
            quitting = False
            rCursor = 0
            cCursor = 0
            while quitting is False:
                self.__changeScreen()
                self.__visualizeGrid(cursor=(True, rCursor, cCursor))
                print()
                print("   W A S D : Move the cursor UP/LEFT/DOWN/RIGHT (combinations allowed)")
                print("    0 - 9  : Set the value of the cell (0 to empty the cell)")
                if self.__game.undoable():
                    print("      Z    : Undo")
                if self.__game.redoable():
                    print("      R    : Redo")
                print("      V    : Save the current puzzle")
                print("      Q    : Quit the game and go back to the play menu")
                print()
                if not self.__game.isSolvable():
                    print("!!! This Puzzle Has No Solution !!!")
                print()
                playerAction = input("Action :").replace(" ", "").lower()
                if len(playerAction) == 1 and playerAction not in "wasd":
                    if playerAction in "0123456789":
                        self.__game.setValueAt(rCursor, cCursor, int(playerAction))
                    elif self.__game.undoable() and playerAction == "z":
                        self.__game.undo()
                    elif self.__game.redoable() and playerAction == "r":
                        self.__game.redo()
                    elif playerAction == "v":
                        puzzle = self.__saving(puzzle=True, file=puzzle)
                    elif playerAction == "q":
                        if self.__game.isSaved():
                            quitting = True
                        else:
                            self.__changeScreen()
                            print("   1 : Save and Quit")
                            print("   2 : Quit without Saving")
                            print("   0 : Back")
                            print("\n\n")
                            saveChoice = self.__optionChoice()
                            while not self.__validOptChoice(saveChoice, 0, 2):
                                self.__changeScreen()
                                print("   1 : Save and Quit")
                                print("   2 : Quit without Saving")
                                print("   0 : Back")
                                print("\n\n")
                                saveChoice = self.__optionChoice()
                            if saveChoice == "1":
                                puzzle = self.__saving(puzzle=True, file=puzzle)
                            elif saveChoice == "2":
                                quitting = True
                elif all(c in "wasd" for c in playerAction):
                    rCursor += playerAction.count("s") - playerAction.count("w")
                    cCursor += playerAction.count("d") - playerAction.count("a")
                    rCursor %= 9
                    cCursor %= 9
            self.__game.exitGrid()


    def __saving(self, puzzle=False, file=None):
        """
        saving(puzzle=bool, file=str)

        A set of saving processes
        If puzzle is True, save as a puzzle file
        If puzzle is False, save as a saved game file

        If file name is given, saving to that file is available
        """
        yes = ("y", "yes", "yeah", "yep")
        no = ("n", "no", "nah", "nope")
        if puzzle is False:
            files = self.__game.getSaves()
        else:
            files = self.__game.getPuzzles()
        self.__changeScreen()
        print("   1 : Save As ...")
        if files is not None:
            print("   2 : Save to a file")
        if file is not None:
            print(f"   3 : Save to ' {file} '")
        print("   0 : Back")
        print("\n\n")
        choice = self.__optionChoice().replace(" ", "")
        while not self.__validOptChoice(choice, 0, 3) or (files is None and choice == "2") or (file is None and choice == "3"):
            self.__changeScreen()
            print("   1 : Save As ...")
            if puzzle is False:
                files = self.__game.getSaves()
            else:
                files = self.__game.getPuzzles()
            if files is not None:
                print("   2 : Save to a file")
            if file is not None:
                print(f"   3 : Save to ' {file} '")
            print("   0 : Back")
            print("\n\n")
            choice = self.__optionChoice().strip()
        if choice == "1":
            self.__changeScreen()
            if puzzle is False:
                self.__showSaves()
            else:
                self.__showPuzzles()
            name = input("\n\n(Press Enter to go back)\nSave as (name) :").strip()
            while any(letter in "\\/:*?\"<>|" for letter in name):
                self.__changeScreen()
                if puzzle is False:
                    self.__showSaves()
                else:
                    self.__showPuzzles()
                name = input("\nSave name cannot contain following characters : \\/:*?\"<>|\n(Press Enter to go back)\nSave as (name) :").strip()
            if name != "":
                if puzzle is False:
                    files = self.__game.getSaves()
                else:
                    files = self.__game.getPuzzles()
                if files is None or name not in files:
                    if puzzle is False:
                        self.__game.saveGame(name)
                        file = name
                    else:
                        self.__game.savePuzzle(name)
                        file = name
                else:
                    self.__changeScreen()
                    override = input(f"   Save file ' {name} ' already exists\n\n\nOverride the exiting save file? (Y/N) :").strip().lower()
                    while override not in yes and override not in no:
                        self.__changeScreen()
                        override = input(f"   Save file ' {name} ' already exists\n\n\nOverride the exiting save file? (Y/N) :").strip().lower()
                    if override in yes:
                        if puzzle is False:
                            self.__game.saveGame(name)
                            file = name
                        else:
                            self.__game.savePuzzle(name)
                            file = name
        elif choice == "2":
            self.__changeScreen()
            if puzzle is False:
                self.__showSaves()
                files = self.__game.getSaves()
            else:
                self.__showPuzzles()
                files = self.__game.getPuzzles()
            file = input("\n\n(Press Enter to go back)\nSelect a file number :").strip()
            while file != "" and (not file.isdigit() or (len(file) > 1 and file[0] == "0") or (file.isdigit() and (int(file) == 0 or int(file) > len(files)))):
                self.__changeScreen()
                if puzzle is False:
                    self.__showSaves()
                    files = self.__game.getSaves()
                else:
                    self.__showPuzzles()
                    files = self.__game.getPuzzles()
                file = input("\n\n(Press Enter to go back)\nSelect a file number :").strip()
            if file != "":
                chosenFile = files[int(file)-1]
                self.__changeScreen()
                override = input(f"Override ' {chosenFile} '? (Y/N) :").strip().lower()
                while override not in yes and override not in no:
                    self.__changeScreen()
                    override = input(f"Override ' {chosenFile} '? (Y/N) :").strip().lower()
                if override in yes:
                    if puzzle is False:
                        self.__game.saveGame(chosenFile)
                        file = chosenFile
                    else:
                        self.__game.savePuzzle(chosenFile)
                        file = chosenFile
        elif choice == "3":
            if puzzle is False:
                self.__game.saveGame(file)
            else:
                self.__game.savePuzzle(file)
        return file


    def __showRules(self):
        """
        showRules()

        Displays the rules of sudoku
        """
        self.__changeScreen()

        print("   @@@@@@@@@@@@@@@@@", sep="")
        print("       R u l e s    ", sep="")
        print("   @@@@@@@@@@@@@@@@@", sep="")
        print()
        print("   # Each puzzle consists of a 9x9 grid (with nine 3x3 boxes)", sep="")
        print("     containing given clues in various places.", sep="")
        print()
        print("   # Each of the nine 3x3 boxes has to contain all the numbers 1-9 within its squares.", sep="")
        print()
        print("   # Each number can only appear once in a row, column or box.\n", sep="")

        H, V = "H", "V" #Horizontal line, Vertical line
        N = "N" #Number
        nums=[1,2,3,4,5,6,7,8,9]
        aBox =(
                (4,H,H,H,8,H,H,H,8,H,H,H,3),
                (V,0,N,0,V,0,N,0,V,0,N,0,V),
                (5,H,H,H,9,H,H,H,9,H,H,H,7),
                (V,0,N,0,V,0,N,0,V,0,N,0,V),
                (5,H,H,H,9,H,H,H,9,H,H,H,7),
                (V,0,N,0,V,0,N,0,V,0,N,0,V),
                (1,H,H,H,6,H,H,H,6,H,H,H,2)
              )
        box = "There are 9 boxes like this --->   "
        for rowNum in range(len(aBox)):
            if rowNum == 3:
                print("   ", box, sep="", end="")
            else:
                print("   ", " "*len(box), sep="", end="")
            for letter in aBox[rowNum]:
                if letter == "N":
                    print(nums.pop(randrange(len(nums))), end="")
                else:
                    print(self.__shapes[letter], end="")
            print()
        nums=[1,2,3,4,5,6,7,8,9]
        aRow =(
                (4,H,H,H,8,H,H,H,8,H,H,H,3,0,4,H,H,H,8,H,H,H,8,H,H,H,3,0,4,H,H,H,8,H,H,H,8,H,H,H,3),
                (V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,N,0,V,0,N,0,V,0,N,0,V),
                (1,H,H,H,6,H,H,H,6,H,H,H,2,0,1,H,H,H,6,H,H,H,6,H,H,H,2,0,1,H,H,H,6,H,H,H,6,H,H,H,2)
              )
        row = "A row with numbers --->   "
        for rowNum in range(len(aRow)):
            if rowNum == 1:
                print("   ", row, sep="", end="")
            else:
                print("   ", " "*len(row), sep="", end="")
            for letter in aRow[rowNum]:
                if letter == "N":
                    print(nums.pop(randrange(len(nums))), end="")
                else:
                    print(self.__shapes[letter], end="")
            print()
        print("\n\n")

        input("Press Enter to go back to the main menu >>>")


    def __displayMain(self):
        """
        displayMain()

        Displays SUDOKU art and main menu options
        """
        H, V = "H", "V" #Horizontal line, Vertical line
        N = "N" #Number
        nums = [1, 2, 3, 4, 5, 6, 7, 8, 9] #Number list
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
        print("   ", "-"*79, "\n   ", "-"*79, sep="") #Line decoration
        for row in SUDOKU:
            print("   ", end="")
            for letter in row:
                if letter == "N": #Pop and print a random number from the list 'nums'
                    print(nums.pop(randrange(len(nums))), end="")
                else: #Print the shape according to the shape dictionary
                    print(self.__shapes[letter], end="")
            print() #Next line
        print("   ", "-"*79, "\n   ", "-"*79, sep="") #Line decoration
        #SUDOKU art finished

        #Display options
        print("   1 : Play\n", sep="")
        print("   2 : Rules\n", sep="")
        print("   0 : Quit", sep="")
        print("\n\n")


    def __displayPlayOpt(self):
        """
        displayPlayOpt()

        Displays PLAY art and play options
        """
        H, V = "H", "V" #Horizontal line, Vertical line
        N, n = "N", "n" #Number1, Number2
        nums1 = [1, 2, 3, 4, 5, 6, 7, 8, 9] #Number list 1
        nums2 = [1, 2, 3, 4, 5, 6, 7, 8, 9] #Number list 2
        #PLAY art!
        PLAY =  (
                (0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,H,H,H,H,H,H,H,H,3,0,4,H,H,3,0,0,0,0,0,0,0,0,0,4,H,H,H,H,3,0,0,0,4,H,H,3,0,0,4,H,H,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0),
                (4,H,H,H,8,H,H,H,8,H,H,H,3,0,V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,4,H,2,0,0,0,0,1,H,3,0,V,0,0,V,0,0,V,0,0,V,0,4,H,H,H,8,H,H,H,8,H,H,H,3),
                (V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,0,4,H,H,3,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,4,H,H,3,0,0,V,0,V,0,0,1,3,4,2,0,0,V,0,V,0,n,0,V,0,n,0,V,0,n,0,V),
                (5,H,H,H,9,H,H,H,9,H,H,H,7,0,V,0,0,1,H,H,2,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,V,0,0,V,0,0,V,0,1,3,0,0,1,2,0,0,4,2,0,5,H,H,H,9,H,H,H,9,H,H,H,7),
                (V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,1,H,H,2,0,0,V,0,0,1,H,3,0,0,4,H,2,0,0,V,0,n,0,V,0,n,0,V,0,n,0,V),
                (5,H,H,H,9,H,H,H,9,H,H,H,7,0,V,0,0,4,H,H,H,H,H,2,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,0,0,0,0,0,0,V,0,0,0,0,V,0,0,V,0,0,0,0,5,H,H,H,9,H,H,H,9,H,H,H,7),
                (V,0,N,0,V,0,N,0,V,0,N,0,V,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,1,H,H,H,H,H,3,0,V,0,0,4,H,H,3,0,0,V,0,0,0,0,V,0,0,V,0,0,0,0,V,0,n,0,V,0,n,0,V,0,n,0,V),
                (1,H,H,H,6,H,H,H,6,H,H,H,2,0,V,0,0,V,0,0,0,0,0,0,0,V,0,0,0,0,0,0,0,0,V,0,V,0,0,V,0,0,V,0,0,V,0,0,0,0,V,0,0,V,0,0,0,0,1,H,H,H,6,H,H,H,6,H,H,H,2),
                (0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,H,H,2,0,0,0,0,0,0,0,1,H,H,H,H,H,H,H,H,2,0,1,H,H,2,0,0,1,H,H,2,0,0,0,0,1,H,H,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)
                )
        print("   ", "-"*71, "\n   ", "-"*71, sep="") #Line decoration
        for row in PLAY:
            print("   ", end="")
            for letter in row:
                if letter == "N": #Pop and print a random number from the list 'nums1'
                    print(nums1.pop(randrange(len(nums1))), end="")
                elif letter == "n": #Pop and print a random number from the list 'nums2'
                    print(nums2.pop(randrange(len(nums2))), end="")
                else: #Print the shape according to the shape dictionary
                    print(self.__shapes[letter], end="")
            print() #Next line
        print("   ", "-"*71, "\n   ", "-"*71, sep="") #Line decoration
        #PLAY art finished

        #Display options
        if self.__game.lastGameExists():
            print("   C : Continue\n")
        print("   1 : New Game\n")
        print("   2 : Load Save\n")
        print("   3 : Build/Edit Puzzle\n")
        print()
        print("   0 : Back")
        print("\n\n")


    def __visualizeGrid(self, cursor=(False, 0, 0)):
        """
        visualizeGrid(cursor=(bool, int, int))  cursor=(show_cursor, row, col)

        Visualizes the game grid in the form of text-based graphical design

        If the first element of the tuple 'cursor' is True, it shows a cursor at the corresponding position
        """
        values = self.__game.getAllValues()
        editables = self.__game.getAllEditableStates()
        def print_top_line():
            """
            Nested function for printing upper layers of mini grids
            """
            print("   ", end="")
            for col in range(9):
                if col % 3 == 0:
                    print(chr(1), end="")
                    print(chr(6) * 3, end="")
                    print(chr(22), end="")

                elif col % 3 == 2:
                    print(chr(6) * 3, end="")
                    print(chr(2), end="")
                    if col < 8:
                        print(" ", end="")
                    else:
                        print()
                else:
                    print(chr(6) * 3, end="")
                    print(chr(22), end="")

        def print_number_line(row):
            """
            Requires an integer row value as the argument
            Nested function for printing lines with number values
            """
            print("   ", end="")
            for col in range(9):  # Lines with numbers
                val = values[9 * row + col]
                if val == 0:
                    cellStr = " "
                else:
                    cellStr = val

                if (cursor[0] is True) and (cursor[1] == row) and (cursor[2] == col):
                    if not editables[9 * row + col]:
                        print(chr(5), ">", cellStr, "<", sep="", end="")
                    else:
                        print(chr(5), "<", cellStr, ">", sep="", end="")
                else:
                    if not editables[9 * row + col]:
                        print(chr(5), "`", cellStr, "'", sep="", end="")
                    else:
                        print(chr(5), " ", cellStr, " ", sep="", end="")
                if col % 3 == 2:
                    print(chr(5), end="")
                    if col != 8:
                        print(" ", end="")
                    else:
                        print()

        def print_middle_line():
            """
            Nested function for printing layers between number lines
            """
            print("   ", end="")
            for col in range(9):
                if col % 3 == 0:
                    print(chr(25), end="")
                    print(chr(6) * 3, end="")
                    print(chr(16), end="")

                elif col % 3 == 2:
                    print(chr(6) * 3, end="")
                    print(chr(23), end="")
                    if col < 8:
                        print(" ", end="")
                    else:
                        print()
                else:
                    print(chr(6) * 3, end="")
                    print(chr(16), end="")

        def print_bottom_line():
            """
            Nested function for printing lower layers of mini grids
            """
            print("   ", end="")
            for col in range(9):
                if col % 3 == 0:
                    print(chr(3), end="")
                    print(chr(6) * 3, end="")
                    print(chr(21), end="")

                elif col % 3 == 2:
                    print(chr(6) * 3, end="")
                    print(chr(4), end="")
                    if col < 8:
                        print(" ", end="")
                    else:
                        print()
                else:
                    print(chr(6) * 3, end="")
                    print(chr(21), end="")

        for row in range(9):
            if row % 3 == 0:
                print_top_line()
            else:
                print_middle_line()
            print_number_line(row)
            if row % 3 == 2:
                print_bottom_line()


    def __showSaves(self):
        """
        showSaves()

        Displays save files
        """
        saves = self.__game.getSaves()
        if saves is None:
            print("   *No Existing Save Files*\n\n\n\n\n\n\n\n\n\n")
        else:
            for num, save in enumerate(saves, 1):
                print(f"   {num:>{len(saves)}}) {save}")
            print("\n\n")


    def __showPuzzles(self):
        """
        showPuzzles()

        Displays puzzle files
        """
        puzzles = self.__game.getPuzzles()
        if puzzles is None:
            print("   *No Existing Puzzle Files*\n\n\n\n\n\n\n\n\n\n")
        else:
            for num, puzzle in enumerate(puzzles, 1):
                print(f"   {num:>{len(puzzles)}}) {puzzle}")
            print("\n\n")


    def __changeScreen(self):
        """
        changeScreen()

        Wipes the screen
        """
        #If the game is running on a Windows Command Prompt, this will clear the screen
        system("cls")
        #Just to make sure, print next-line many times so that the old texts will definately disappear from the current screen
        print("\n"*100)


    def __optionChoice(self):
        """
        optionChoice()

        Prompts the user to input a value and then returns it
        """
        choice = input("Choose an option : ").lower() #Take input
        choice = choice.replace(" ", "") #Remove any empty space
        return choice


    def __validOptChoice(self, userInput, start, end):
        """
        validOptChoice(str, int, int[, args])

        Returns a boolean
        True if the user input is a number (integer) in [start, end]
        False otherwise
        """
        return userInput.isdigit() and not (len(userInput) > 1 and userInput[0] == "0") and int(userInput) in range(start, end+1)


    def __quit(self):
        """
        quit()

        Prompts the user to confirm quitting
        If the user confirms quitting, the program ends
        Else, it sends the user back to the main menu
        """
        self.__changeScreen()

        #Ways you can say "Yes" or "No"
        yes = ("y", "yes", "yep", "yeah", "quit")
        no = ("n", "no", "nope", "nah", "back")

        #Input is NOT case-sensitive since the upper case letters would be all converted to lower cases here
        choice = input("Quit the program? (Y or N) : ").lower()
        #The program will keep prompting until the player enters a valid input
        while choice not in yes and choice not in no:
            self.__changeScreen()
            choice = input("Quit the program? (Y or N)").lower()

        return choice in yes


    def __exit(self):
        """
        exit()

        Delays the closing of the program for a moment as it displays closing message
        """
        self.__changeScreen()
        print("Closing.")
        sleep(0.25)
        self.__changeScreen()
        print("Closing..")
        sleep(0.25)
        self.__changeScreen()
        print("Closing...")
        sleep(0.25)
        self.__changeScreen()


def programStarter(Class):
    program = Class()


if __name__ == '__main__':
    programStarter(Sudoku)
