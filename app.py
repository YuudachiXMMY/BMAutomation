import sys

# To Install BMAutomation, use the following Command in Windows CMD:
# py -m pip install --index-url https://test.pypi.org/simple/ BMAutomation
import BMAutomation as ba

steamDir = "F:\\SteamLibrary\\steamapps\\common"
docDir = "C:\\Users\\Navi\\Documents"

app = ba.BMAutomation(steamDir, docDir)

def Fallout4():
    try:
        f4 = ba.Game('Fallout 4', steamDirectory=app.getSteamDirectory(),
                     documentDirectory=app.getDocumentDirectory(), exe="Fallout4Launcher.exe")

        f4.setExecutorPath("s/Fallout 4")
        f4.setLauncherMode(1)
        f4.setLauncher(waitTime=5,
                       uiAppControlType="WindowControl", uiAppName='Fallout 4',
                       uiStartControlType="ImageControl", uiStartIndex=4, uiStartName='')

        f4.setStartActions([
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
        f4.setQuitActions([
            ["s", "key_alt_f4", 0.6]
        ])
        f4.setBenchmarkingMode(2)

        checkCode = f4.check()
        if checkCode:
            app.addGameList('Fallout 4', f4)
        return checkCode

    except Exception as e:
        sys.stdout.write(e.__class__.__name__ + ': Fallout4 caused an Error.')
        return False


def main():
    checkCode = Fallout4()

    if not checkCode:
        return checkCode

    codes = app.start()
    return codes


if __name__ == "__main__":
    try:
        exit(main())

    except KeyboardInterrupt:
        ba.Logger.WriteLine(
            "\n"+"*"*10+' Ctrl+C key input detected. Program Stopped! '+"*"*10)
        exit(1)
    except Exception as e:
        ba.Logger.WriteLine("%s: Exception Detected!" % e)
        exit(0)
