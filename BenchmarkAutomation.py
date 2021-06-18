import Game
from typing import Any

class BenchmarkAutomation:
    '''
    '''

    def __init__(self, steamDirectory: str = "", documentDirectory: str = "") -> None:
        '''
        '''
        pass

    def addGame(self, exe: str = "", relativePath: str = "", absolutePath: str = "") -> Any:
        '''
        '''
        return Game(self.getSteamDirectory, self.getDocumentDirectory(), \
            exe, relativePath, absolutePath)


    ############################################################################
    def setSteamDirectory(self, dir: str) -> Any:
        '''
        '''
        self.steamDirectory = dir

    def getSteamDirectory(self) -> str:
        '''
        '''
        return self.steamDirectory

    def setDocumentDirectory(self, dir: str) -> Any:
        '''
        '''
        self.documentDirectory = dir

    def getDocumentDirectory(self) -> str:
        '''
        '''
        return self.documentDirectory


    ############################################################################