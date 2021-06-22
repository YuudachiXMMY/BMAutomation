import os
import time
import random
from typing import Any

import win32api, win32con
import pyautogui as pag

import win32api
import uiautomation as auto

import Logger
from Logger import ConsoleColor
from Logger import Logger

## Local variable
## BM stands for BenchMarking
ROTATE_ANGLE = [0, 90, 180, 270]

BM_WAIT_TIME_MIN = 0
BM_WAIT_TIME_MAX = 15

KEY_PRESS_WAIT_TIME_MIN = 0
KEY_PRESS_WAIT_TIME_MAX = 3

RANDOM_KEY_LIST = [
    "w",
    "a",
    "s",
    "d",
    "e",
    "space",
    "left_click",
    "right_click"
]
    # "spacebar",

MOUSE_LIST = [
    "left_click",
    "right_click"
]
    # "view_upward",
    # "view_downward",
    # "view_leftward",
    # "view_rightward"

def mouseCharacterControl(action, keyTime):
    '''
    A method called by randomCharacterControl() to perform mouse control for characters.

    @param:
        - action: action to perform
        - keyTime: duration to perform the key time
    '''
    res = keyTime
    if action == "view_upward":
        callTinyTask("mouse/moveUpWard")
        # utils.input.moveTo(960, 1000, keyTime)
    if action == "view_downward":
        callTinyTask("mouse/moveDownWard")
        # utils.input.moveTo(960, 80, keyTime)
    if action == "view_leftward":
        callTinyTask("mouse/moveLeftWard")
        # utils.input.moveTo(1800, 540), keyTime
    if action == "view_rightward":
        callTinyTask("mouse/moveRightWard")
        # utils.input.moveTo(120, 540, keyTime)
    if action == "left_click":
        clickLeft(None, None, keyTime)
    if action == "right_click":
        clickRight(None, None, keyTime)
    return res

def keyCharacterControl(action, keyTime):
    '''
    A method called by randomCharacterControl() to perform keyboard control for characters.

    @param:
        - action: action to perform
        - keyTime: duration to perform the key time
    '''
    # utils.input.key_input(action, keyTime)
    callTinyTask(action)
    time.sleep(keyTime)
    return keyTime

def changeDisplayDirection(deviceIndex, angle):
    '''
    Rotate the Display Screen's Direction

    @param:
        - deviceIndex - display device index
        - angle - angle to be rotated

    @RETURN:
        - True - succeed in rotating the screen.
        - False - failed to rotate the screen.
    '''
    # if not hasDisplayDevice(deviceIndex):
    #     return
    try:
        device = win32api.EnumDisplayDevices(None, deviceIndex)
        dm = win32api.EnumDisplaySettings(device.DeviceName,win32con.ENUM_CURRENT_SETTINGS)
        if angle == 90:
            dm.DisplayOrientation = win32con.DMDO_90 #待改变的值
            #以下的720或者1280 代表我的屏幕的长宽
            #在应用项目的时候,建议使用GetSystemMetrics 动态获取长宽
            #在每次改变方向的时候,都要判断是否需要交换屏幕的长宽
            if win32api.GetSystemMetrics(win32con.SM_CXSCREEN) != 720:
                dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth

        elif angle == 180:
            dm.DisplayOrientation = win32con.DMDO_180
            if win32api.GetSystemMetrics(win32con.SM_CXSCREEN) != 1280:
                dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth

        elif angle == 270:
            dm.DisplayOrientation = win32con.DMDO_270
            if win32api.GetSystemMetrics(win32con.SM_CXSCREEN) != 720:
                dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth

        elif angle == 0:
            dm.DisplayOrientation = win32con.DMDO_DEFAULT
            if win32api.GetSystemMetrics(win32con.SM_CXSCREEN) != 1280:
                dm.PelsWidth, dm.PelsHeight = dm.PelsHeight, dm.PelsWidth

        win32api.ChangeDisplaySettingsEx(device.DeviceName,dm)

        return True

    except Exception:
        return False

############################################################################
################################## VK_Code #################################
############################################################################
class VK_CODE():
    '''
    VK_CODE is a class having two dictionaries to represent VK_CODE
    '''

    def __init__(self):
        '''
        Construct VK_CODE with two representations of VK_CODE
        '''
        self._VK_CODE1 = {
            'backspace':0x08,
            'tab':0x09,
            'clear':0x0C,
            'enter':0x0D,
            'shift':0x10,
            'ctrl':0x11,
            'alt':0x12,
            'pause':0x13,
            'caps_lock':0x14,
            'esc':0x1B,
            'spacebar':0x20,
            'page_up':0x21,
            'page_down':0x22,
            'end':0x23,
            'home':0x24,
            'left_arrow':0x25,
            'up_arrow':0x26,
            'right_arrow':0x27,
            'down_arrow':0x28,
            'select':0x29,
            'print':0x2A,
            'execute':0x2B,
            'print_screen':0x2C,
            'ins':0x2D,
            'del':0x2E,
            'help':0x2F,
            '0':0x30,
            '1':0x31,
            '2':0x32,
            '3':0x33,
            '4':0x34,
            '5':0x35,
            '6':0x36,
            '7':0x37,
            '8':0x38,
            '9':0x39,
            'a':0x41,
            'b':0x42,
            'c':0x43,
            'd':0x44,
            'e':0x45,
            'f':0x46,
            'g':0x47,
            'h':0x48,
            'i':0x49,
            'j':0x4A,
            'k':0x4B,
            'l':0x4C,
            'm':0x4D,
            'n':0x4E,
            'o':0x4F,
            'p':0x50,
            'q':0x51,
            'r':0x52,
            's':0x53,
            't':0x54,
            'u':0x55,
            'v':0x56,
            'w':0x57,
            'x':0x58,
            'y':0x59,
            'z':0x5A,
            'numpad_0':0x60,
            'numpad_1':0x61,
            'numpad_2':0x62,
            'numpad_3':0x63,
            'numpad_4':0x64,
            'numpad_5':0x65,
            'numpad_6':0x66,
            'numpad_7':0x67,
            'numpad_8':0x68,
            'numpad_9':0x69,
            'multiply_key':0x6A,
            'add_key':0x6B,
            'separator_key':0x6C,
            'subtract_key':0x6D,
            'decimal_key':0x6E,
            'divide_key':0x6F,
            'F1':0x70,
            'F2':0x71,
            'F3':0x72,
            'F4':0x73,
            'F5':0x74,
            'F6':0x75,
            'F7':0x76,
            'F8':0x77,
            'F9':0x78,
            'F10':0x79,
            'F11':0x7A,
            'F12':0x7B,
            'F13':0x7C,
            'F14':0x7D,
            'F15':0x7E,
            'F16':0x7F,
            'F17':0x80,
            'F18':0x81,
            'F19':0x82,
            'F20':0x83,
            'F21':0x84,
            'F22':0x85,
            'F23':0x86,
            'F24':0x87,
            'num_lock':0x90,
            'scroll_lock':0x91,
            'left_shift':0xA0,
            'right_shift ':0xA1,
            'left_control':0xA2,
            'right_control':0xA3,
            'left_menu':0xA4,
            'right_menu':0xA5,
            'browser_back':0xA6,
            'browser_forward':0xA7,
            'browser_refresh':0xA8,
            'browser_stop':0xA9,
            'browser_search':0xAA,
            'browser_favorites':0xAB,
            'browser_start_and_home':0xAC,
            'volume_mute':0xAD,
            'volume_Down':0xAE,
            'volume_up':0xAF,
            'next_track':0xB0,
            'previous_track':0xB1,
            'stop_media':0xB2,
            'play/pause_media':0xB3,
            'start_mail':0xB4,
            'select_media':0xB5,
            'start_application_1':0xB6,
            'start_application_2':0xB7,
            'attn_key':0xF6,
            'crsel_key':0xF7,
            'exsel_key':0xF8,
            'play_key':0xFA,
            'zoom_key':0xFB,
            'clear_key':0xFE,
            '+':0xBB,
            ',':0xBC,
            '-':0xBD,
            '.':0xBE,
            '/':0xBF,
            '`':0xC0,
            ';':0xBA,
            '[':0xDB,
            '\\':0xDC,
            ']':0xDD,
            "'":0xDE
        }
        self._VK_CODE2 = {
            'A':'a',
            'B':'b',
            'C':'c',
            'D':'d',
            'E':'e',
            'F':'f',
            'G':'g',
            'H':'h',
            'I':'i',
            'J':'j',
            'K':'k',
            'L':'l',
            'M':'m',
            'N':'n',
            'O':'o',
            'P':'p',
            'Q':'q',
            'R':'r',
            'S':'s',
            'T':'t',
            'U':'u',
            'V':'v',
            'W':'w',
            'X':'x',
            'Y':'y',
            'Z':'z',
            ')':'0',
            '!':'1',
            '@':'2',
            '#':'3',
            '$':'4',
            '%':'5',
            '^':'6',
            '&':'7',
            '*':'8',
            '(':'9',
            '=':'+',
            '<':',',
            '_':'-',
            '>':'.',
            '?':'/',
            '~':'`',
            ':':';',
            '{':'[',
            '|':'\\',
            '}':']',
            '"':"'"
        }

    def getVK_CODE1(self):
        '''
        Return the first type of representation of VK_CODE

        @RETURN: The first type of representation of VK_CODE
        '''
        return dict(self._VK_CODE1)

    def getVK_CODE2(self):
        '''
        Return the second type of representation of VK_CODE

        @RETURN: The second type of representation of VK_CODE
        '''
        return dict(self._VK_CODE2)

VK_CODE = VK_CODE.VK_CODE()
VK_CODE1 = VK_CODE.getVK_CODE1()
VK_CODE2 = VK_CODE.getVK_CODE2()

tmp = VK_CODE().getVK_CODE2().copy()
tmp.update(VK_CODE().getVK_CODE1())
RANDOM_WORD_LIST = list(tmp.keys())

############################################################################
################################## Input ###################################
############################################################################
def key_input(key, t=0.05):
    '''
    Perform a key pressdown and pressup.

    @param:
        - key - a key to be pressed.
        - t - time period in second between pressdown and pressup (default to 0.05).

    @RETURN:
        - 1 - succeed in performing a key pressing process.
        - 0 - failed to perform a key pressing process.
    '''
    if key in VK_CODE2:
        key = VK_CODE2[key]
    if key in VK_CODE1:
        # Pressdown
        win32api.keybd_event(VK_CODE1[key],0,0,0)
        # Duration between pressdown and pressup
        time.sleep(t)
        # Pressup
        win32api.keybd_event(VK_CODE1[key],0,win32con.KEYEVENTF_KEYUP,0)
        return 1
    return 0

def key_inputs(str_input='', t=0.05):
    '''
    Perform a serious of key pressdowns and pressups.

    @param:
        - string of keys - a string of keys to be pressed (default to '').
        - t - time period in second between each key to be pressed (default to 0.05).

    @RETURN:
        - 1 - succeed in performing a key pressing process.
        - 0 - failed to perform a key pressing process.
    '''
    for k in str_input:
        keyInputStatusCode = key_input(k)
        if not keyInputStatusCode:
            return keyInputStatusCode
        time.sleep(t)
    return keyInputStatusCode

def key_alt_tab(t=0.5):
    '''
    Perform a key action of ALT + TAB.

    @param:
        - t - time period in second between pressdown and pressup (default to 0.05).
    '''
    win32api.keybd_event(VK_CODE1["alt"],0,0,0)
    win32api.keybd_event(VK_CODE1["tab"],0,0,0)
    time.sleep(t)
    win32api.keybd_event(VK_CODE1["tab"],0,win32con.KEYEVENTF_KEYUP,0)
    win32api.keybd_event(VK_CODE1["alt"],0,win32con.KEYEVENTF_KEYUP,0)

def key_alt_f4():
    '''
    Perform a key action of ALT + F4.

    @param:
        - t - time period in second between pressdown and pressup (default to 0.05).
    '''
    win32api.keybd_event(VK_CODE1["alt"],0,0,0)
    time.sleep(0.2)
    win32api.keybd_event(VK_CODE1["F4"],0,0,0)
    time.sleep(0.2)
    win32api.keybd_event(VK_CODE1["F4"],0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(0.2)
    win32api.keybd_event(VK_CODE1["alt"],0,win32con.KEYEVENTF_KEYUP,0)

def clickLeft(x=None, y=None, duration=0):
    '''
    Perform a mouse action of left clicking on screen position at (x, y).

    @param:
        - x - horizontal position to be clicked.
        - y - vertical position to be clicked.
    '''
    if x == None and y == None:
        x, y = win32api.GetCursorPos()
    # win32api.SetCursorPos((x, y))
    # time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    time.sleep(duration)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
    return x, y

def clickRight(x=None, y=None, duration=0):
    '''
    Perform a mouse action of right clicking on screen position at (x, y).

    @param:
        - x - horizontal position to be clicked.
        - y - vertical position to be clicked.
    '''
    if x == None and y == None:
        x, y = win32api.GetCursorPos()
    # win32api.SetCursorPos((x, y))
    # time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
    time.sleep(duration)
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
    return x, y

def move(dest_x, dest_y, start_x=None, start_y=None, duration=0):
    '''
    Perform a mouse action to move the mouse
    from (start_x, start_y) to (dest_x, dest_y) in duration time.

    @param:
        - dest_x - horizontal position to end
        - dest_y - vertical position to end
        - start_x - horizontal position to start
        - start_y - vertical position to start
        - duration - action's duration in seconds
    '''
    if start_x == None:
        start_x = win32api.GetCursorPos()[0]
    if start_y == None:
        start_y = win32api.GetCursorPos()[1]
    win32api.SetCursorPos((start_x, start_y))
    pag.moveTo(dest_x, dest_y, duration=duration, tween=pag.easeInOutQuad)

def moveTo(dest_x, dest_y, duration=0):
    '''
    Perform a mouse action of clicking on screen position at (x, y).

    @param:
        - x - horizontal position to be clicked.
        - y - vertical position to be clicked.
    '''
    start_x, start_y = win32api.GetCursorPos()
    move(start_x, start_y, dest_x, dest_y, duration)

def getMouse(t=0):
    '''
    Get the mouse position and print in the console

    @param:
        - t - period to get the mouse position

    @RETURN:
        - (x, y) - a tuple which x represent the x-position of the mouse and y represent the y-position of the mouse.
    '''
    try:
        while True:
            print("Press Ctrl-C to end")
            screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
            x, y = pag.position()  # 返回鼠标的坐标
            print("Screen size: (%s %s),  Position : (%s, %s)\n" % (screenWidth, screenHeight, x, y))  # 打印坐标

            time.sleep(t)  # 每个1s中打印一次 , 并执行清屏
            os.system('cls')  # 执行系统清屏指令
    except KeyboardInterrupt:
        print('end')

def logMouse(t=0):
    '''
    Get the mouse position and print in the console only when the mouse position changes

    @param:
        - t - period to get the mouse position

    @RETURN:
        - (x, y) - a tuple which x represent the x-position of the mouse and y represent the y-position of the mouse.
    '''
    try:
        x, y = pag.position()  # 返回鼠标的坐标
        while True:
            screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
            xNew, yNew = pag.position()  # 返回鼠标的坐标
            if xNew != x and yNew != y:
                print("Screen size: (%s %s),  Position : (%s, %s)\n" % (screenWidth, screenHeight, x, y))  # 打印坐标
                x, y = (xNew, yNew)

    except KeyboardInterrupt:
        os.system('cls')  # 执行系统清屏指令
        print('end')

def callTinyTask(file):
    '''
    Calling the .exe file made by TinyTask

    @param:
        - file: a TinyTask File Name to be performed

    @RETURN:
        - 0 - failed
        - 1 - succeed
    '''
    return win32api.ShellExecute(1, 'open', file, '', '', 1)


############################################################################
################################### Game ###################################
############################################################################
class Game:
    '''
    '''

    def __init__(self, gameName: str = "", \
        steamDirectory: str = "", documentDirectory: str = "", benchDirectory: str = "",\
        exe: str = "", relativePath: str = "", absolutePath: str = "", \
        loopTimes: int = 1, stressTest: bool = False, mode: int = 0) -> None:
        '''

        mode:
            0- norm
            1- alt-tab
            2- randomControl
            3- randomInput
            4- randomRotate
        '''
        self.gameName = gameName

        if not steamDirectory is None and not os.path.isdir(steamDirectory):
            self.steamDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid steamDirectory.', ConsoleColor.Yellow)
        else:
            self.steamDirectory = steamDirectory

        if not documentDirectory is None and not os.path.isdir(documentDirectory):
            self.documentDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid documentDirectory.', ConsoleColor.Yellow)
        else:
            self.documentDirectory = documentDirectory

        if not benchDirectory is None and not os.path.isdir(benchDirectory):
            self.benchDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid benchDirectory.', ConsoleColor.Yellow)
        else:
            self.benchDirectory = benchDirectory

        self.exe = exe

        if not relativePath is None and not os.path.isdir(relativePath):
            self.relativePath = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid relativePath.', ConsoleColor.Yellow)
        else:
            self.relativePath = relativePath

        if not absolutePath is None and not os.path.isdir(absolutePath) and not os.path.isabs(absolutePath):
            self.absolutePath = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid absolutePath.', ConsoleColor.Yellow)
        else:
            self.absolutePath = absolutePath

        self.loopTimes = loopTimes
        self.stressTest = stressTest

        if mode >= 0 and mode <=4:
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

    def setExecutor(self, exe: str):
        '''
        '''
        self.exe = exe

    def getExecutor(self) -> str:
        '''
        '''
        return self.exe

    def getBenchmarkingMode(self) -> int:
        '''
        '''
        return self.mode

    ############################################################################
    def startGame(self, exePath: str, exeName: str = None, \
        hasLauncher: bool = False, launcherMode: int = None, \
        uiAppControlType: str = None, uiAppName: str = None, \
        uiButtonType: str = None, uiButtonIndex: int = None, uiButtonName: str = None,\
        clickPos: tuple = None, \
        TinyTaskName: str = None) -> int:
        '''
        S/s- Steam
        R/r- Relative
        A/a- Abolute
        Other- Directly add to full .exe path

        exe- Executor

        launcherMode:
            0 - UIAutomation
            1 - click on given position
            2 - call TinyTask
        '''
        if exeName is None:
            if self.exe is None or self.exe == "":
                Logger.WriteLine('error: Executor is None. Please use setExecutor() to initialize first.', ConsoleColor.Red)
                return 0
            exe = self.exe

        paths = str.lower(exePath).split("-")

        full_exe = ""
        for p in paths:
            if p == "s":
                full_exe = os.path.join(full_exe, self.getSteamDirectory())
            elif p == "r":
                full_exe = os.path.join(full_exe, self.getRelativePath())
            elif p == "a":
                full_exe = os.path.join(full_exe, self.getAbsolutePath())
            else:
                full_exe = os.path.join(full_exe, p)

        full_exe = os.path.join(full_exe, exe)

        if not os.path.isfile(full_exe):
            Logger.WriteLine('error: Executor\'s Full Path is not valid. Current Path: %s'%full_exe, ConsoleColor.Red)
            return 0
        startGame = win32api.ShellExecute(1, 'open', full_exe, '', '', 1)

        if hasLauncher:
            Logger.WriteLine('waiting 20 seconds for launcher to start......', ConsoleColor.Gray)
            time.sleep(20)

            ## Using UIAutomation
            if launcherMode == 0:
                if uiAppControlType is None:
                    Logger.WriteLine('error: uiAppControlType should not be None.', ConsoleColor.Red)
                    return 0
                if uiAppName is None:
                    Logger.WriteLine('error: uiAppName should not be None.', ConsoleColor.Red)
                    return 0

                if uiButtonType is None:
                    Logger.WriteLine('error: uiButtonType should not be None.', ConsoleColor.Red)
                    return 0
                if uiButtonIndex is None and uiButtonName is None:
                    Logger.WriteLine('error: uiButtonIndex or uiButtonName should not be None.', ConsoleColor.Red)
                    return 0
                if uiButtonIndex is None and not uiButtonName is None:
                    uiButtonIndex = 0


                if uiAppControlType == "PaneControl":
                    app = auto.PaneControl(searchDepth=1, Name=uiAppName)
                elif uiAppControlType == "WindowControl":
                    app = auto.WindowControl(searchDepth=1, Name=uiAppName)
                elif uiAppControlType == "ImageControl":
                    app = auto.ImageControl(searchDepth=1, Name=uiAppName)
                elif uiAppControlType == "ButtonControl":
                    app = auto.ButtonControl(searchDepth=1, Name=uiAppName)
                else:
                    Logger.WriteLine("error: %s is not recognized as a ControlType. Please check again or report this issue."%uiAppControlType, ConsoleColor.Red)
                    return 0

                ## Set the launcher window to the very top of the screen
                app.SetTopmost(True)

                ## Click on Start Button
                if uiButtonType == "PaneControl":
                    auto.PaneControl(foundIndex=uiButtonIndex, Name=uiButtonName).Click()
                elif uiButtonType == "WindowControl":
                    auto.WindowControl(foundIndex=uiButtonIndex, Name=uiButtonName).Click()
                elif uiButtonType == "ImageControl":
                    auto.ImageControl(foundIndex=uiButtonIndex, Name=uiButtonName).Click()
                elif uiButtonType == "ButtonControl":
                    auto.ButtonControl(foundIndex=uiButtonIndex, Name=uiButtonName).Click()
                else:
                    Logger.WriteLine("error: %s is not recognized as a ControlType. Please check again or report this issue."%uiButtonType, ConsoleColor.Red)
                    return 0

            ## Using win32 Mouse Click Action
            elif launcherMode == 1:
                xClickPos, yClickPos = clickPos
                clickLeft(xClickPos, yClickPos)

            ## Calling TinyTask executor
            elif launcherMode == 2:
                callTinyTask(TinyTaskName)

        return startGame

    def startBenchMarking(self, duration: int = 300):
        '''
        mode:
            0- norm
            1- alt-tab
            2- randomControl
            3- randomInput
            4- randomRotate
        '''
        ## Normal Benchmarking
        if self.getBenchmarkingMode == 0:
            time.sleep(duration)
        ## Alt-Tab Benchmarking
        elif self.getBenchmarkingMode == 1:
            waitTime = 0
            altTabTime = 0
            while(duration >= 0):
                waitTime = random.uniform(BM_WAIT_TIME_MIN, BM_WAIT_TIME_MAX)
                altTabTime = random.uniform(KEY_PRESS_WAIT_TIME_MIN, KEY_PRESS_WAIT_TIME_MAX)
                key_alt_tab()
                time.sleep(altTabTime)
                key_alt_tab()
                time.sleep(waitTime)

                duration -= 1
                duration -= waitTime
                duration -= altTabTime
        ## Random-Control Benchmarking
        elif self.getBenchmarkingMode == 2:
            waitTime = 0
            tmp = RANDOM_KEY_LIST.copy()
            tmp.extend(MOUSE_LIST)
            while(duration >= 0):
                waitTime = random.uniform(BM_WAIT_TIME_MIN, BM_WAIT_TIME_MAX)
                keyTime = random.uniform(KEY_PRESS_WAIT_TIME_MIN, KEY_PRESS_WAIT_TIME_MAX)
                action = random.choice(tmp)

                if action in MOUSE_LIST:
                    keyTime = mouseCharacterControl(action, keyTime)
                elif action in RANDOM_KEY_LIST:
                    keyTime = keyCharacterControl(action, keyTime)

                duration -= waitTime
                duration -= keyTime
                time.sleep(waitTime)
        ## Random-Input Benchmarking
        elif self.getBenchmarkingMode == 3:
            waitTime = 0
            while(duration >= 0):
                waitTime = random.uniform(BM_WAIT_TIME_MIN, BM_WAIT_TIME_MAX)
                keyTime = random.uniform(KEY_PRESS_WAIT_TIME_MIN, KEY_PRESS_WAIT_TIME_MAX)
                action = random.choice(RANDOM_WORD_LIST)

                keyTime = keyCharacterControl(action, keyTime)

                duration -= waitTime
                duration -= keyTime
                time.sleep(waitTime)
        ## Random-Rotate Benchmarking
        elif self.getBenchmarkingMode == 4:
            waitTime = 0
            altTabTime = 0
            while(duration >= 0):
                waitTime = random.uniform(5, 20)

                changeDisplayDirection(0, random.choice(ROTATE_ANGLE))

                duration -= waitTime
                time.sleep(waitTime)

            changeDisplayDirection(0, 0)
        else:
            Logger.WriteLine("error: Benchmarking Mode failed.", ConsoleColor.Red)


############################################################################
########################### BenchmarkAutomation ############################
############################################################################
class BenchmarkAutomation:
    '''
    '''

    def __init__(self, steamDirectory: str = "", documentDirectory: str = "", \
        OverallLoopTimes: int = 1, GameLoopTimes: int = -1) -> None:
        '''
        '''
        if not steamDirectory is None and not os.path.isdir(steamDirectory):
            self.steamDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid steamDirectory.', ConsoleColor.Yellow)
        else:
            self.steamDirectory = steamDirectory

        if not documentDirectory is None and not os.path.isdir(documentDirectory):
            self.documentDirectory = None
            Logger.WriteLine('warning: BenchmarkAutomationGame is not initialized with a valid documentDirectory.', ConsoleColor.Yellow)
        else:
            self.documentDirectory = documentDirectory

        self.gameList = dict()

        self.OverallLoopTimes = OverallLoopTimes
        self.GameLoopTimes = GameLoopTimes

    ############################################################################
    def addGameList(self, gameName: str, gameObj: Game = None, \
        exe: str = "", relativePath: str = "", absolutePath: str = "") -> Any:
        '''
        '''
        if not gameObj is None:
            self.gameList[gameName] = gameObj
        else:
            self.gameList[gameName] = Game( \
                self.getSteamDirectory, self.getDocumentDirectory(), \
                exe, relativePath, absolutePath)

    def getGameList(self) -> dict:
        '''
        '''
        return self.gameList

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