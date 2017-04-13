import os
'''
Name: FileHander:
Description: Controls reading/writing to files and
determines if a file has updated
@param player : a character representing the player
'''
class FileHandler:
    def __init__(self,player):
        if player == "X":
            self.__player = player
            self.__opponent ="Y"
        else:
            self.__player = player
            self.__opponent = "X"
        file = "log_"+self.__opponent+".txt"
        self.__opponentStamp = os.stat(file).st_mtime
    '''
    Method: write()
    description: This method records a move given by the player

    parameter:
    turn - an integer representing game's current turn
    piece - A string representing a chess piece
    move - a 2 character string that represents a chess square
    ex) a2



    Known Issues:
    1. Method does not check for file existance
    2. Method does not check if string is in proper format
    '''
    def write(self,turn,piece,move,timeExpired):
        file = "log_"+self.__player+".txt"
        log = str(turn) + " " + self.__player+":"+piece+":"+move+"\n"
        previous = self.getPreviousMove()

        if previous:#in middle of game
            f = open(file,"a")
            if (not timeExpired):
                f.write(previous)
            f.write(log)
            f.close()
        else: #if opponent file is empty, start of new game
            f = open(file,"w")
            f.write(log)
            f.close()
    '''
    Method: waitOpponent()
    description: boolean function to determine if the opposing player has made a move
    Return Values:
    True : If file has been modified
    False: File has not been modified from the last recorded time

    '''
    def waitOpponent(self):
        file = "log_"+self.__opponent+".txt" 
        modif = os.stat(file).st_mtime
        if modif != self.__opponentStamp:
            self.__opponentStamp = modif
            return False
        else:
            return True
    '''
    Method: getPreviousMove()
    description: returns a string containing the last line of the opponent file

    Return Values:
    None: Empty String if the file is initially empty
    String in the format of [n X:P:MM]

    Known Issues: Does not check for file existance
    '''
    def getPreviousMove(self):
        file = "log_"+self.__opponent+".txt"
        f = open(file,"r")
        last = None
        for line in f:    
            last = line
        f.close()
        return last
    '''
    Method: loadAll()
    description: this method returns a list with indices containing a file from
    the file

    return: list of all items in the file

    known Issues: does not check for file existance
    '''
    def loadAll(self):
        file = "log_"+self.__player+".txt"
        f = open (file,"r")
        lines = f.readlines()
        f.close()
        return lines
'''
player = "X"
player1 = FileHandler(player)
turn = 0
piece = "K"
move = "e1"
if player == "X":
    player1.write(turn,piece,move)
else:
    turn = 1
    pass
while(turn < 10):
    while(True):
        wait = player1.waitOpponent()
        if wait:
            pass
        else:
            break
    player1.write(turn,piece,move)
    turn = turn + 2
print("X Finished")
'''