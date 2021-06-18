import os
import sys
import datetime
import ctypes
import ctypes.wintypes

from typing import (Any, Callable, Dict, List, Iterable, Tuple)  # need 'pip install typing' for Python3.4 or lower


_StdOutputHandle = -11
_ConsoleOutputHandle = ctypes.c_void_p(0)
_DefaultConsoleColor = None

class ConsoleColor:
    """ConsoleColor from Win32."""
    Default = -1
    Black = 0
    DarkBlue = 1
    DarkGreen = 2
    DarkCyan = 3
    DarkRed = 4
    DarkMagenta = 5
    DarkYellow = 6
    Gray = 7
    DarkGray = 8
    Blue = 9
    Green = 10
    Cyan = 11
    Red = 12
    Magenta = 13
    Yellow = 14
    White = 15

class ConsoleScreenBufferInfo(ctypes.Structure):
    _fields_ = [
        ('dwSize', ctypes.wintypes._COORD),
        ('dwCursorPosition', ctypes.wintypes._COORD),
        ('wAttributes', ctypes.c_uint),
        ('srWindow', ctypes.wintypes.SMALL_RECT),
        ('dwMaximumWindowSize', ctypes.wintypes._COORD),
    ]

def SetConsoleColor(color: int) -> bool:
    """
    Change the text color on console window.
    color: int, a value in class `ConsoleColor`.
    Return bool, True if succeed otherwise False.
    """
    global _ConsoleOutputHandle
    global _DefaultConsoleColor
    if not _DefaultConsoleColor:
        if not _ConsoleOutputHandle:
            _ConsoleOutputHandle = ctypes.c_void_p(ctypes.windll.kernel32.GetStdHandle(_StdOutputHandle))
        bufferInfo = ConsoleScreenBufferInfo()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(_ConsoleOutputHandle, ctypes.byref(bufferInfo))
        _DefaultConsoleColor = int(bufferInfo.wAttributes & 0xFF)
    if sys.stdout:
        sys.stdout.flush()
    return bool(ctypes.windll.kernel32.SetConsoleTextAttribute(_ConsoleOutputHandle, ctypes.c_ushort(color)))

def ResetConsoleColor() -> bool:
    """
    Reset to the default text color on console window.
    Return bool, True if succeed otherwise False.
    """
    if sys.stdout:
        sys.stdout.flush()
    return bool(ctypes.windll.kernel32.SetConsoleTextAttribute(_ConsoleOutputHandle, ctypes.c_ushort(_DefaultConsoleColor)))

################################################################################

class Logger:
    """
    Logger for print and log. Support for printing log with different colors on console.
    """
    FileName = '@AutomationLog.txt'
    _SelfFileName = os.path.split(__file__)[1]
    ColorNames = {
        "Black": ConsoleColor.Black,
        "DarkBlue": ConsoleColor.DarkBlue,
        "DarkGreen": ConsoleColor.DarkGreen,
        "DarkCyan": ConsoleColor.DarkCyan,
        "DarkRed": ConsoleColor.DarkRed,
        "DarkMagenta": ConsoleColor.DarkMagenta,
        "DarkYellow": ConsoleColor.DarkYellow,
        "Gray": ConsoleColor.Gray,
        "DarkGray": ConsoleColor.DarkGray,
        "Blue": ConsoleColor.Blue,
        "Green": ConsoleColor.Green,
        "Cyan": ConsoleColor.Cyan,
        "Red": ConsoleColor.Red,
        "Magenta": ConsoleColor.Magenta,
        "Yellow": ConsoleColor.Yellow,
        "White": ConsoleColor.White,
    }

    @staticmethod
    def SetLogFile(path: str) -> None:
        Logger.FileName = path

    @staticmethod
    def Write(log: Any, consoleColor: int = ConsoleColor.Default, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None, printTruncateLen: int = 0) -> None:
        """
        log: any type.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.
        printTruncateLen: int, if <= 0, log is not truncated when print.
        """
        if not isinstance(log, str):
            log = str(log)
        if printToStdout and sys.stdout:
            isValidColor = (consoleColor >= ConsoleColor.Black and consoleColor <= ConsoleColor.White)
            if isValidColor:
                SetConsoleColor(consoleColor)
            try:
                if printTruncateLen > 0 and len(log) > printTruncateLen:
                    sys.stdout.write(log[:printTruncateLen] + '...')
                else:
                    sys.stdout.write(log)
            except Exception as ex:
                SetConsoleColor(ConsoleColor.Red)
                isValidColor = True
                sys.stdout.write(ex.__class__.__name__ + ': can\'t print the log!')
                if log.endswith('\n'):
                    sys.stdout.write('\n')
            if isValidColor:
                ResetConsoleColor()
            sys.stdout.flush()
        if not writeToFile:
            return
        fileName = logFile if logFile else Logger.FileName
        fout = None
        try:
            fout = open(fileName, 'a+', encoding='utf-8')
            fout.write(log)
        except Exception as ex:
            if sys.stdout:
                sys.stdout.write(ex.__class__.__name__ + ': can\'t write the log!')
        finally:
            if fout:
                fout.close()

    @staticmethod
    def WriteLine(log: Any, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: any type.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.
        """
        Logger.Write('{}\n'.format(log), consoleColor, writeToFile, printToStdout, logFile)

    @staticmethod
    def ColorfullyWrite(log: str, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: str.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.
        ColorfullyWrite('Hello <Color=Green>Green</Color> !!!'), color name must be in Logger.ColorNames.
        """
        text = []
        start = 0
        while True:
            index1 = log.find('<Color=', start)
            if index1 >= 0:
                if index1 > start:
                    text.append((log[start:index1], consoleColor))
                index2 = log.find('>', index1)
                colorName = log[index1+7:index2]
                index3 = log.find('</Color>', index2 + 1)
                text.append((log[index2 + 1:index3], Logger.ColorNames[colorName]))
                start = index3 + 8
            else:
                if start < len(log):
                    text.append((log[start:], consoleColor))
                break
        for t, c in text:
            Logger.Write(t, c, writeToFile, printToStdout, logFile)

    @staticmethod
    def ColorfullyWriteLine(log: str, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: str.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.

        ColorfullyWriteLine('Hello <Color=Green>Green</Color> !!!'), color name must be in Logger.ColorNames.
        """
        Logger.ColorfullyWrite(log + '\n', consoleColor, writeToFile, printToStdout, logFile)

    @staticmethod
    def Log(log: Any = '', consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: any type.
        consoleColor: int, a value in class `ConsoleColor`, such as `ConsoleColor.DarkGreen`.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.
        """
        frameCount = 1
        while True:
            frame = sys._getframe(frameCount)
            _, scriptFileName = os.path.split(frame.f_code.co_filename)
            if scriptFileName != Logger._SelfFileName:
                break
            frameCount += 1

        t = datetime.datetime.now()
        log = '{}-{:02}-{:02} {:02}:{:02}:{:02}.{:03} {}[{}] {} -> {}\n'.format(t.year, t.month, t.day,
            t.hour, t.minute, t.second, t.microsecond // 1000, scriptFileName, frame.f_lineno, frame.f_code.co_name, log)
        Logger.Write(log, consoleColor, writeToFile, printToStdout, logFile)

    @staticmethod
    def ColorfullyLog(log: str = '', consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        log: any type.
        consoleColor: int, a value in class ConsoleColor, such as ConsoleColor.DarkGreen.
        writeToFile: bool.
        printToStdout: bool.
        logFile: str, log file path.

        ColorfullyLog('Hello <Color=Green>Green</Color> !!!'), color name must be in Logger.ColorNames
        """
        frameCount = 1
        while True:
            frame = sys._getframe(frameCount)
            _, scriptFileName = os.path.split(frame.f_code.co_filename)
            if scriptFileName != Logger._SelfFileName:
                break
            frameCount += 1

        t = datetime.datetime.now()
        log = '{}-{:02}-{:02} {:02}:{:02}:{:02}.{:03} {}[{}] {} -> {}\n'.format(t.year, t.month, t.day,
            t.hour, t.minute, t.second, t.microsecond // 1000, scriptFileName, frame.f_lineno, frame.f_code.co_name, log)
        Logger.ColorfullyWrite(log, consoleColor, writeToFile, printToStdout, logFile)

    @staticmethod
    def DeleteLog() -> None:
        """Delete log file."""
        if os.path.exists(Logger.FileName):
            os.remove(Logger.FileName)


################################################################################