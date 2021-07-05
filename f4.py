from typing import Any  # need 'pip install typing' for Python3.4 or lower
from typing import Callable, Dict, Iterable, List, Literal, Tuple
import BenchmarkAutomation as ba


def m():
    steamDir = "F:\\SteamLibrary\\steamapps\\common"
    docDir = "C:\\Users\\Navi\\Documents"

    app = ba.BenchmarkAutomation(steamDir, docDir)
    f4 = ba.Game('Fallout 4', steamDirectory=steamDir,
                 documentDirectory=docDir, exe="Fallout4Launcher.exe")

    app.addGameList('Fallout 4', f4)

    f4.setExecutorPath("s/Fallout 4")
    f4.setLauncherMode(1)
    f4.setLauncher(waitTime=5,
                   uiAppControlType="WindowControl", uiAppName='Fallout 4',
                   uiStartControlType="ImageControl", uiStartIndex=4, uiStartName='')

    checkCode = f4.checkStart()
    if checkCode:
        startCode = f4.start(GameWaitTime=30)
    else:
        return 0

    if startCode:
        inGameCode = f4.Actions([["w", "wait", 10],
                                ["s", "key_alt_tab", 0.6],
                                ["w", "wait", 20],
                                ["cl", (960, 540), 1],
                                ["cl", (960, 540), 1],
                                ["cl", (960, 540), 1],
                                ["cl", (960, 540), 1],
                                ["w", "wait", 5],
                                ["t", "tinytask/enter.exe", 1],
                                ["t", "tinytask/enter.exe", 1],
                                ["w", "wait", 20]])
    else:
        return 0

    if inGameCode:
        f4.setBenchmarkingMode(2)
        startBenchmark = f4.startBenchMarking(30)
    else:
        return 0

    quitGameCode = 0
    if startBenchmark:
        quitGameCode = f4.Actions([["s", "key_alt_f4", 0.6]])
    return quitGameCode

try:
    exitCode = 0
    exitCode = m()
except Exception as e:
    print(e)
else:
    exit(exitCode)