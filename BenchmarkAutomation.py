import Game

class BenchmarkAutomation:
    '''
    '''

    def __init__(self, steamDirectory="", documentDirectory="") -> None:
        '''
        '''
        pass

    def addGame(self, exe="", relativePath="", absolutePath=""):
        '''
        '''
        return Game(self.getSteamDirectory, self.getDocumentDirectory(), \
            exe, relativePath, absolutePath)


    ############################################################################
    def addSteamDirectory(self, dir):
        self.steamDirectory = dir

    def changeSteamDirectory(self, dir):
        self.addSteamDirectory(dir)

    def getSteamDirectory(self):
        return self.steamDirectory

    def addDocumentDirectory(self, dir):
        self.documentDirectory = dir

    def changeDocumentDirectory(self, dir):
        self.addSteamDirectory(dir)

    def getDocumentDirectory(self):
        return self.documentDirectory


    ############################################################################