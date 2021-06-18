import os
from typing import Any

import Logger
from Logger import ConsoleColor
from Logger import Logger

class Game:
    '''
    '''

    def __init__(self, gameName: str = "", \
        steamDirectory: str = "", documentDirectory: str = "", benchDirectory: str = "",\
        exe: str = "", relativePath: str = "", absolutePath: str = "", \
        loopTimes: int = 1, stressTest: bool = False, mode: int = 0) -> None:
        '''
        '''
        self.gameName = gameName

        if steamDirectory != None and not os.path.isdir(steamDirectory):
            self.steamDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid steamDirectory.', ConsoleColor.Yellow)
        else:
            self.steamDirectory = steamDirectory

        if documentDirectory != None and not os.path.isdir(documentDirectory):
            self.documentDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid documentDirectory.', ConsoleColor.Yellow)
        else:
            self.documentDirectory = documentDirectory

        if benchDirectory != None and not os.path.isdir(benchDirectory):
            self.benchDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid benchDirectory.', ConsoleColor.Yellow)
        else:
            self.benchDirectory = benchDirectory

        self.exe = exe

        if relativePath != None and not os.path.isdir(relativePath):
            self.relativePath = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid relativePath.', ConsoleColor.Yellow)
        else:
            self.relativePath = relativePath

        if absolutePath != None and not os.path.isdir(absolutePath) and not os.path.isabs(absolutePath):
            self.absolutePath = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid absolutePath.', ConsoleColor.Yellow)
        else:
            self.absolutePath = absolutePath

        self.loopTimes = loopTimes
        self.stressTest = stressTest

        if mode >= 0 and mode <=3:
            self.mode = mode
        else:
            Logger.WriteLine('BenchmarkAutomationGame does not initialized with a valid mode.', ConsoleColor.Yellow)

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

    def setBenchDirectory(self, dir: str) -> Any:
        '''
        '''
        self.benchDirectory = dir

    def getBenchDirectory(self) -> str:
        '''
        '''
        return self.benchDirectory

    def setRelativePath(self, dir: str) -> Any:
        '''
        '''
        self.relativePath = dir

    def getRelativePath(self) -> str:
        '''
        '''
        return self.relativePath

    def setAbsolutePath(self, dir: str) -> Any:
        '''
        '''
        self.absolutePath = dir

    def getAbsolutePath(self) -> str:
        '''
        '''
        return self.absolutePath

    ############################################################################
