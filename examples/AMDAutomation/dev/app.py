import sys
import json

################################################################################
def read_json(file):
    '''
    Read a .json file and return a json type.

    @param:
        - file - a filename to be read as .json data.

    @RETURN:
        - A Python's Data Object representing the data in the .json file.
        - None - EXCEPTION occurred.
    '''
    try:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data == None:
            data = dict()
        return data
    except Exception:
        return None


config = read_json("config.json")
RunList = config["RunList"]


################################################################################
# To Install BMAutomation, use the following Command in Windows CMD:
# Released Package:
# py -m pip install bmautomation
# Test Package:
# py -m pip install --index-url https://test.pypi.org/simple/ bmautomation
import bmautomation as ba


# Directories
steamDir: str = "F:\\SteamLibrary\\steamapps\\common"
docDir: str = "C:\\Users\\Navi\\Documents"

SniperEliteV2Dir: str = "C:\\Program Files (x86)\\Rebellion\\SniperEliteV2 Benchmark\\bin"
AvPDir: str = "C:\\Program Files (x86)\\Rebellion\\AvP D3D11 Benchmark"
UnigineHeavenDir: str = "C:\\Program Files (x86)\\Unigine\\Heaven Benchmark 4.0\\bin"
UnigineHeavenArgs: str = "-project_name Heaven -data_path ../ -engine_config ../data/heaven_4.0.cfg -system_script heaven/unigine.cpp -extern_define RELEASE -video_fullscreen"
UnigineSanctuaryDir: str = "C:\\Program Files (x86)\\Unigine\\Sanctuary"
UnigineSanctuaryArgs: str = "-video_app direct3d11 -video_mode -1 -video_width 1920 -video_height 1080 -data_path ./ -engine_config data/unigine.cfg -system_script sanctuary/unigine.cpp"
DOOMEternalDir: str = "G:\\DOOMEternal"
DOOMEternalArgs: str = "+com_skipKeyPressOnLoadScreens 1 +LoadDevMenuOption devmenuoption/sp 5 0 +g_runCmdOnMapGameplay God +g_runCmdOnMapGameplay `'chainBookmarks -t 0 -i 10`'"
SidMeiersCivilizationVIDir: str = "G:\\SidMeiersCivilizationVI\\Base\\Binaries\\Win64EOS"
SidMeiersCivilizationVIArgs: str = "-benchmark"
Rainbow6Dir: str = "G:\\Rainbow6"
Rainbow6Args: str = "/test:GameTestEngineTest_PerfTest"
Borderlands3Dir: str = "G:\\CatnipStaging2\\OakGame\\Binaries\\Win64"
Borderlands3Args: str = "-nomcp -dx12 -GbxBenchmarkMap -GbxBenchmarkIterations=10"

FFXIV_ARR_BenchDir: str = "G:\\FFXIV-ARR-Bench-Character"
FFXIVBenchmarkDir: str = "G:\\FFXIVBenchmark"
FFXIV_Endwalker_benchDir: str = "G:\\ffxiv-endwalker-bench"
FFXIV_Heavensward_BenchDir: str = "G:\\ffxiv-heavensward-bench"
FFXIV_Shadowbringers_BenchDir: str = "G:\\ffxiv-shadowbringers-bench"
FFXIV_Stormblood_BenchDir: str = "G:\\ffxiv-stormblood-bench"

GenshinImpactDir: str = "G:\\Genshin Impact"


# Init BMAutomation
app: ba.BMAutomation = ba.BMAutomation(steamDir, docDir)
# app.setDealCrashDump(True, "C:\\WinDumps")

app.setOverallLoopTimes(999)
app.setBenchmarkTime(300)


################################################################################
def SniperEliteV2():
    try:
        game_name: str = "SniperEliteV2"
        game: ba.Game = ba.Game(game_name, benchDirectory=SniperEliteV2Dir,
                                exe="SniperEliteV2.exe")

        game.setBenchmarkTime(60)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([])
        game.setQuitActions([
            ["k", "esc", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(1)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def AvP():
    try:
        game_name: str = "SniperEliteV2"
        game: ba.Game = ba.Game(game_name, benchDirectory=AvPDir,
                                exe="AvP_D3D11_Benchmark.exe")

        game.setBenchmarkTime(60)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([])
        game.setQuitActions([
            ["k", "esc", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(1)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def UnigineHeaven():
    try:
        game_name: str = "UnigineHeaven"
        game: ba.Game = ba.Game(game_name, benchDirectory=UnigineHeavenDir,
                                exe="Heaven.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setLaunchParam(UnigineHeavenArgs)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([])
        game.setQuitActions([
            ["s", "key_alt_f4", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)


def UnigineSanctuary():
    try:
        game_name: str = "UnigineSanctuary"
        game: ba.Game = ba.Game(game_name, benchDirectory=UnigineSanctuaryDir,
                                exe="Sanctuary.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setLaunchParam(UnigineSanctuaryArgs)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([])
        game.setQuitActions([
            ["s", "key_alt_f4", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)


def DOOMEternal():
    try:
        game_name: str = "DOOMEternal"
        game: ba.Game = ba.Game(game_name, benchDirectory=DOOMEternalDir,
                                exe="DOOMEternalx64vk.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setLaunchParam(DOOMEternalArgs)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([
            ["s", "key_alt_tab", 1.0]
        ])
        game.setQuitActions([
            ["s", "key_alt_f4", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)


def SidMeiersCivilizationVI():
    try:
        game_name: str = "SidMeiersCivilizationVI"
        game: ba.Game = ba.Game(game_name, benchDirectory=SidMeiersCivilizationVIDir,
                                exe="CivilizationVI_DX12.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setLaunchParam(SidMeiersCivilizationVIArgs)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([
            ["s", "key_alt_tab", 1.0]
        ])
        game.setQuitActions([
            ["s", "key_alt_f4", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)


def Rainbow6():
    try:
        game_name: str = "Rainbow6"
        game: ba.Game = ba.Game(game_name, benchDirectory=Rainbow6Dir,
                                exe="RainbowSix.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setLaunchParam(Rainbow6Args)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([
            ["s", "key_alt_tab", 1.0]
        ])
        game.setQuitActions([
            ["s", "key_alt_f4", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)


def Borderlands3():
    try:
        game_name: str = "Borderlands3"
        game: ba.Game = ba.Game(game_name, benchDirectory=Borderlands3Dir,
                                exe="OakGame-Win64-Test.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setLaunchParam(Borderlands3Args)

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([
            ["s", "key_alt_tab", 1.0]
        ])
        game.setQuitActions([
            ["s", "key_alt_f4", 0.6],
            ["w", "wait", 30]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)

def FFXIV_ARR_Bench():
    try:
        game_name: str = "FFXIV_ARR_Bench"
        game: ba.Game = ba.Game(game_name, benchDirectory=FFXIV_ARR_BenchDir,
                                exe="ffxiv-arr-bench-character.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("b/")
        game.setLauncherMode(1)
        game.setLauncher(waitTime=5,
                         uiAppControlType="PaneControl", uiAppName='FINAL FANTASY XIV: A Realm Reborn Official Benchmark (Character Creation)',
                         uiStartControlType="ButtonControl", uiStartIndex=11, uiStartName='')

        game.setStartActions([])
        game.setQuitActions([
            ["k", "esc", 0.6],
            ["w", "wait", 30],
            ["k", "esc", 0.6]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def FFXIVBenchmark():
    try:
        game_name: str = "FFXIVBenchmark"
        game: ba.Game = ba.Game(game_name, benchDirectory=FFXIVBenchmarkDir,
                                exe="FFXIVBenchmark.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("b/")
        game.setLauncherMode(0)

        game.setStartActions([
            ["k", "right_arrow", 0.6],
            ["k", "enter", 0.6],
            ["k", "enter", 0.6],
            ["w", "wait", 20]
        ])
        game.setQuitActions([
            ["k", "esc", 0.6]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def FFXIV_Endwalker_Bench():
    try:
        game_name: str = "FFXIV_Endwalker_bench"
        game: ba.Game = ba.Game(game_name, benchDirectory=FFXIV_Endwalker_benchDir,
                                exe="ffxiv-endwalker-bench.exe")

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
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def FFXIV_Heavensward_Bench():
    try:
        game_name: str = "FFXIV_Heavensward_Bench"
        game: ba.Game = ba.Game(game_name, benchDirectory=FFXIV_Heavensward_BenchDir,
                                exe="ffxiv-heavensward-bench.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("b/")
        game.setLauncherMode(1)
        game.setLauncher(waitTime=5,
                         uiAppControlType="PaneControl", uiAppName='FINAL FANTASY XIV: Heavensward Benchmark',
                         uiStartControlType="ButtonControl", uiStartIndex=16, uiStartName='')

        game.setStartActions([])
        game.setQuitActions([
            ["k", "esc", 0.6],
            ["w", "wait", 30],
            ["k", "esc", 1.0],
            ["k", "enter", 0.6]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def FFXIV_Shadowbringers_Bench():
    try:
        game_name: str = "FFXIV_Shadowbringers_Bench"
        game: ba.Game = ba.Game(game_name, benchDirectory=FFXIV_Shadowbringers_BenchDir,
                                exe="ffxiv-shadowbringers-bench.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("b/")
        game.setLauncherMode(1)
        game.setLauncher(waitTime=5,
                         uiAppControlType="WindowControl", uiAppName='FINAL FANTASY XIV: Shadowbringers Benchmark',
                         uiStartControlType="CustomControl", uiStartIndex=20, uiStartName='')

        game.setStartActions([])
        game.setQuitActions([
            ["k", "esc", 0.6],
            ["w", "wait", 30],
            ["s", "key_alt_f4", 0.6]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def FFXIV_Stormblood_Bench():
    try:
        game_name: str = "FFXIV_Stormblood_Bench"
        game: ba.Game = ba.Game(game_name, benchDirectory=FFXIV_Stormblood_BenchDir,
                                exe="ffxiv-stormblood-bench.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("b/")
        game.setLauncherMode(1)
        game.setLauncher(waitTime=5,
                         uiAppControlType="PaneControl", uiAppName='FINAL FANTASY XIV: Stormblood Benchmark',
                         uiStartControlType="ButtonControl", uiStartIndex=16, uiStartName='')

        game.setStartActions([])
        game.setQuitActions([
            ["k", "esc", 0.6],
            ["w", "wait", 30],
            ["k", "esc", 1.0],
            ["k", "enter", 0.6]
        ])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)


def GenshinImpact():
    # TODO
    try:
        game_name: str = "GenshinImpact"
        game: ba.Game = ba.Game(game_name, benchDirectory=GenshinImpactDir,
                                exe="launcher.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("b/")
        game.setLauncherMode(2)

        game.setStartActions([])
        game.setQuitActions([])
        game.setBenchmarkingMode(0)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)


def Fallout4():
    try:
        game_name: str = "Fallout 4"
        game: ba.Game = ba.Game(game_name, steamDirectory=app.getSteamDirectory(),
                                exe="Fallout4Launcher.exe")

        game.setBenchmarkTime(app.getBenchmarkTime())

        game.setExecutorPath("s/Fallout 4")
        game.setLauncherMode(1)
        game.setLauncher(waitTime=5,
                         uiAppControlType="WindowControl", uiAppName='Fallout 4',
                         uiStartControlType="ImageControl", uiStartIndex=4, uiStartName='')

        game.setStartActions([
            ["w", "wait", 20],
            ["cl", (960, 540), 1],
            ["cl", (960, 540), 1],
            ["cl", (960, 540), 1],
            ["cl", (960, 540), 1],
            ["w", "wait", 5],
            ["t", "tinytask//enter.exe", 1],
            ["t", "tinytask//enter.exe", 1],
            ["w", "wait", 30]
        ])
        game.setQuitActions([
            ["s", "key_alt_f4", 0.6]
        ])
        game.setBenchmarkingMode(2)

        checkCode = game.check()
        if checkCode:
            app.addGameList(game_name, game)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ +
                         ': %s caused an Error.' % game_name)
        return False


def main():
    checkCode = 1

    if "Fallout4":
        Fallout4()
    if "GenshinImpact":
        GenshinImpact()
    if "DOOMEternal":
        DOOMEternal()
    if "SidMeiersCivilizationVI":
        SidMeiersCivilizationVI()
    if "Rainbow6":
        Rainbow6()
    if "Borderlands3":
        Borderlands3()
    if "UnigineHeaven":
        UnigineHeaven()
    if "UnigineSanctuary":
        UnigineSanctuary()
    if "FFXIV_ARR_Bench":
        FFXIV_ARR_Bench()
    if "FFXIVBenchmark":
        FFXIVBenchmark()
    if "FFXIV_Endwalker_Bench":
        FFXIV_Endwalker_Bench()
    if "FFXIV_Shadowbringers_Bench":
        FFXIV_Shadowbringers_Bench()
    if "FFXIV_Stormblood_Bench":
        FFXIV_Stormblood_Bench()
    if "SniperEliteV2":
        SniperEliteV2()
    if "AvP":
        AvP()

    if not checkCode:
        return checkCode

    codes = app.start()
    return codes


if __name__ == "__main__":
    try:
        code = main()
        input("Press ENTER to quit:")

    except KeyboardInterrupt:
        ba.Logger.WriteLine(
            "\n"+"*"*10+' Ctrl+C key input detected. Program Stopped! '+"*"*10)
        input("Press ENTER to quit:")
    except Exception as e:
        ba.Logger.WriteLine("%s: Exception Detected!" % e)
        input("Press ENTER to quit:")
