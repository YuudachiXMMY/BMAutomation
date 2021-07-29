# Dev for AMDAutomation

AMDAutomation utilizes another API/Library: [BMAutomation]((https://pypi.org/project/bmautomation/)), which is published on PyPI.

Therefore, you should **install and import** this library.

To install the library, utilize this code for Windows:

``` CMD
pip install bmautomation
```

To import the library:

``` Python
import bmautomation as bm
```

## Initialization

### Utils

#### `bmautomation.read_json()`

It is recommened to utilize the `bmautomation.read_json()` function to help developing. So far, the `app.py` uses a `config.json` to make the development easlier.

In the `config.json`, you can define the machine name (which can be used for later development of analyzing) and a game run list (where you can add or remove those unnecessary games. Some may not be ready to do the automation, some may be new game.)

##### Related variables

- `config` : Read the `config.json` and save in `config`.
- `RunList` : A game run list

### Initialize `bmautomation.BMAutomation()`

First, it is recommend to init the local steam directories. Here, I define the steam directory to be:

``` Python
steamDir: str = "F:\\SteamLibrary\\steamapps\\common"
```

Once you finish defining a steam directory, you can easily initialize the app by doing so:

``` Python
app: ba.BMAutomation = ba.BMAutomation(steamDir)
```

It is also recommend to set the **overall loop times** and **benchmark time** for each game. The value depend on your automation cycle:

``` Python
app.setOverallLoopTimes(999)
app.setBenchmarkTime(300)
```

There is a list that you can play with [BMAutomation]((https://pypi.org/project/bmautomation/)):

- `bmautomation.BMAutomation().setSteamDirectory()` : Set the Steam directory.
- `bmautomation.BMAutomation().setBenchmarkTime()` : Set Benchmarking Time.
- `bmautomation.BMAutomation().setDocumentDirectory()` : Set the Document directory.
- `bmautomation.BMAutomation().setOverallLoopTimes()` : Set the BMAutomation Loop Times.
- `bmautomation.BMAutomation().setGameLoopTimes()` : Set each game Loop Times.
- `bmautomation.setDealCrashDump()` : Set to deal crash dump.

## To add a new game

### Initializing `bmautomation.Game()`

First, it is recommend to init a name for the game. **For example**, here, I define the game name to be:

``` Python
game_name: str = "FFXIV_Endwalker_bench"
```

Also, I will define the game directory:

``` Python
FFXIV_Endwalker_benchDir: str = "G:\\ffxiv-endwalker-bench"
```

Now, I am ready to initialize the `bmautomation.Game()` object:

``` Python
## Here I set the executor name while initializing the object. However, it is
## not required to do so. You can always do this by using other functions.
game: ba.Game = ba.Game(game_name, benchDirectory = FFXIV_Endwalker_benchDir,
                        exe = "ffxiv-endwalker-bench.exe")
```

To finish the initialization of `bmautomation.Game()` object, here's a **TODO** list:

- [ ] `bmautomation.Game().setExecutorPath()` : Set the Executor Path.
- [ ] `bmautomation.Game().setLauncherMode()` : Set the Launcher Operation Mode.
- [ ] `bmautomation.Game().setLauncher()` : Set the Launcher Operation _(Must do this if not game.setLauncherMode(0))_.
- [ ] `bmautomation.Game().setStartActions()` : Set the start-up actions after game is launched.
- [ ] `bmautomation.Game().setQuitActions()` : Set the quit actions after game is launched.
- [ ] `bmautomation.Game().setBenchmarkingMode()` : Set the Benchmarking Mode.

There is a full list of all config settings for the `bmautomation.Game()` object:

- `bmautomation.Game().setGameName()` : Set the Game Name.
- `bmautomation.Game().setBenchmarkTime()` : Set Benchmarking Time.
- `bmautomation.Game().setSteamDirectory()` : Set the Steam directory.
- `bmautomation.Game().setDocumentDirectory()` : Set the Document directory.
- `bmautomation.Game().setBenchDirectory()` : Set the Benchmark directory.
- `bmautomation.Game().setRelativePath()` : Set the Relative Path represent the game folder name under the Steam directory.
- `bmautomation.Game().setAbsolutePath()` : Set the Absolute Path used for independent games.
- `bmautomation.Game().setLoopTimes()` : Set the Loop Times.
- `bmautomation.Game().getLoopTimes()` : Get the Loop Times.
- `bmautomation.Game().setExecutor()` : Set the Executor.
- `bmautomation.Game().setExecutorPath()` : Set the Executor Path.
- `bmautomation.Game().setLauncherMode()` : Set the Launcher Operation Mode.
- `bmautomation.Game().setLauncher()` : Set the Launcher Operation.
- `bmautomation.Game().setLaunchParam()` : Set the Launching Parameter for the Game that can be recognized by Command Line.
- `bmautomation.Game().setStartActions()` : Set the start-up actions after game is launched.
- `bmautomation.Game().setQuitActions()` : Set the quit actions after game is launched.
- `bmautomation.Game().setBenchmarkingMode()` : Set the Benchmarking Mode.

Last but not least, before you add it to the `app` run list, you should always use **check** function to check whether it is well-setted to do the automation:

``` Python
checkCode = game.check() # Return True if it is ready to be added to the game list.
if checkCode:
    app.addGameList(game_name, game)
```

#### For developing purpose

You can also utilize other check functions to see each status of config settings for debugging ('cause `bmautomation.Game().check()` utilizes these check functions to do an overall check):

- `bmautomation.Game().checkStartActions()` : Check whether this Game start-up operation is setted successfully.
- `bmautomation.Game().checkQuitActions()` : Check whether this Game quit operation is setted successfully.
- `bmautomation.Game().checkLaunch()` : Check whether the launcher start-up operation is setted successfully.

### Demo codes

#### FFXIV Endwalker Bench

``` Python
# Importing BMAutomation
import bmautomation as ba

# Directories
steamDir: str = "F:\\SteamLibrary\\steamapps\\common"       # Steam Directory

FFXIV_Endwalker_benchDir: str = "G:\\ffxiv-endwalker-bench" # Game Directory

# Init `bmautomation.BMAutomation`
app: ba.BMAutomation = ba.BMAutomation(steamDir)

# Set `bmautomation.BMAutomation` overall loop times and benchmark time (scale: seconds).
app.setOverallLoopTimes(999)
app.setBenchmarkTime(300)

# I would like to write the Script of each game in a function, and call the
# function if needed:)
def FFXIV_Endwalker_Bench():
    # It is always wise to use `try` & `except` pair to track errors.
    try:
        game_name: str = "FFXIV_Endwalker_bench"
        # Initialize `bmautomation.Game()`
        game: ba.Game = ba.Game(game_name, benchDirectory=FFXIV_Endwalker_benchDir,
                                exe="ffxiv-endwalker-bench.exe")

        # Set benchmark time to app's benchmark time (which is setted to 300 seconds; default: 600)
        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("b/")
        game.setLauncherMode(1)
        game.setLauncher(waitTime=5,
                         uiAppControlType="WindowControl", uiAppName='FINAL FANTASY XIV: Endwalker Benchmark',
                         uiStartControlType="CustomControl", uiStartIndex=20, uiStartName='')

        game.setStartActions([])
        game.setQuitActions([
            ["k", "esc", 0.6],
            ["w", "wait", 30],
            ["s", "key_alt_f4", 1.0]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        print(e.__class__.__name__ +
              ': %s caused an Error.' % game_name)
        return False

# Main function of the Script
def main():
    checkFFXIV = FFXIV_Endwalker_Bench()

    # This if-statement is not necessary. 'cause we've already done a check
    # by `bmautomation.Game().check()`
    if checkFFXIV:
        app.start()

main()
```
