import BenchmarkAutomation as ba
import os

steamDir = "F:\\SteamLibrary\\steamapps\\common"
docDir = "C:\\Users\\Navi\\Documents"

app = ba.BenchmarkAutomation(steamDir, docDir)
f4 = ba.Game('Fallout 4', steamDirectory=steamDir, documentDirectory=docDir, exe="Fallout4Launcher.exe")

app.addGameList('Fallout 4', f4)

f4.setExecutorPath("s/Fallout 4")
f4.setLauncherMode(1)
f4.setLauncher(uiAppControlType="WindowControl", uiAppName='Fallout 4', \
    uiStartControlType="ImageControl", uiStartIndex=4, uiStartName='')

checkCode = f4.checkStart()
startCode = f4.start()
print(checkCode, startCode)