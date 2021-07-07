import ctypes
import ctypes.wintypes
import datetime
import json
import os
import random
import re
import subprocess
import sys
import time
from typing import Any  # need 'pip install typing' for Python3.4 or lower
from typing import Callable, Dict, Iterable, List, Literal, Tuple

import pyautogui as pag
import uiautomation as auto
import win32api
import win32con

################################################################################
################################### Console ####################################
################################################################################
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
            _ConsoleOutputHandle = ctypes.c_void_p(
                ctypes.windll.kernel32.GetStdHandle(_StdOutputHandle))
        bufferInfo = ConsoleScreenBufferInfo()
        ctypes.windll.kernel32.GetConsoleScreenBufferInfo(
            _ConsoleOutputHandle, ctypes.byref(bufferInfo))
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
#################################### Logger ####################################
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
    def WriteProgress(counts: int, total: int, log: str = "", width: int = 50, unit: str = "", consoleColor: int = ConsoleColor.Default):
        """
        Write a progress bar with the given counts of total.

        Parameters
        ----------
        counts : integer
            Current counts of a progress.
        total : int
            Total counts of a progress.
        log : string, optional.
            Log message before the progress bar (default: ""). Usually passing 'Waiting' or 'Progressing'.
        width : int, optional
            The width in letters of the progress bar (default: 50).
        unit : string, optional.
            Unit of the counts (default: ""). Ususally passing a time unit like 's' and 'min'.
            For example, by passing 's' will have an output '1 s / 10 s  10%'; otherwise, '1 / 10  10%'
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).

        Notes
        -----
        * Logger.WriteProgress should always be used with vairables updated in loops; Please check the Examples section

        Examples
        --------
        To init a new progress bar with 1 / 10, simply do this:

        >>> Logger.WriteProgress(1, 10)
        |                                                  | 1 / 10  10.00%

        Adding log message and count units:

        >>> Logger.WriteProgress(1, 10, log='Waiting', unit='s')
        Waiting|                                                  | 1 s / 10 s  10.00%

        The following code shows a small demo of having progress bar randomly increasing:

        >>> import random
        >>> counts = 0
        >>> total = 100 # Total counts will be 100
        >>> Logger.WriteProgress(counts, total) # Starting the progress bar from 0 to 100
        >>> while counts < total:
        >>>     counts += random.randint(0, 5) # Randomly increasing the progress bar.
        >>>     Logger.WriteProgress(counts, total) # Updating the progress bar on console

        """
        log = str(log) + ' '
        isValidColor = (
            consoleColor >= ConsoleColor.Black and consoleColor <= ConsoleColor.White)
        if isValidColor:
            SetConsoleColor(consoleColor)
        # sys.stdout.write(' ' * (width + 9) + '\r')
        # sys.stdout.flush()
        progress = int(width * counts / total)
        sys.stdout.write(log + '|' + '█' * progress +
                         ' ' * int(width - progress) + '|')
        if unit == "" or unit is None:
            sys.stdout.write(
                ' {0} / {1}  {2}%\r'.format(int(counts), total, ('%.2f' % (100*counts/total))))
        else:
            sys.stdout.write(' {0} {3} / {1} {3}  {2}%\r'.format(int(counts),
                             total, ('%.2f' % (100*counts/total)), unit))
        if progress == width:
            sys.stdout.write('\n')
        if isValidColor:
            ResetConsoleColor()
        sys.stdout.flush()

    @staticmethod
    def CountProgress(total: int, log: str = "Progressing", step: int = 1, width: int = 50, consoleColor: int = ConsoleColor.Default):
        """
        Write a progress bar counting down in seconds

        Parameters
        ----------
        total : int
            Total counts of a progress.
        log : string, optional.
            Log message before the progress bar (default: "Progressing"). Usually passing 'Waiting' or 'Progressing'.
        step : int, optional.
            Steps or period to update the progress bar in seconds (default: 1).
        width : int, optional
            The width in letters of the progress bar (default: 50).
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).

        Examples
        --------
        To show a progress bar uniformly progressing for 10 seconds with step 1:

        >>> Logger.WriteProgress(10, log="Progressing", step=1)
        Progressing|                                                  | 0 s / 10 s  0.00%
        Progressing|█                                                 | 1 s / 10 s  10.00%
        Progressing|██                                                | 2 s / 10 s  20.00%
        ......

        or just simply use the following code and will prodcue the same output:

        >>> Logger.WriteProgress(10)
        Progressing|                                                  | 0 s / 10 s  0.00%
        Progressing|█                                                 | 1 s / 10 s  10.00%
        Progressing|██                                                | 2 s / 10 s  20.00%
        ......

        """
        for counts in range(0, total+1, step):
            Logger.WriteProgress(counts, total, log, step,
                                 width, "s", consoleColor)
            time.sleep(step)

    @staticmethod
    def SetLogFile(path: str) -> None:
        Logger.FileName = path

    @staticmethod
    def Write(log: Any, consoleColor: int = ConsoleColor.Default, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None, printTruncateLen: int = 0) -> None:
        """
        Write logs to Console

        Parameters
        ----------
        log : Any type. A string is preferred.
            Logs text
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).
        writeToFile : bool, optional.
            True to write logs into a file (default: True).
        printToStdout : bool, optional.
            True to print to standard output (default: True).
        logFile : str, optional.
            Logs file name (default: None). None to write to default log file '@AutomationLog.txt'
        printTruncateLen : int, optional.
            If <= 0, log is not truncated when print.

        Notes
        -----
        'ConsoleColor' (or Logger.ColorNames) currently has supported the following colors:

        ============  ===========
            Color         int
        ============  ===========
        Default       -1
        Black         0
        DarkBlue      1
        DarkGreen     2
        DarkCyan      3
        DarkRed       4
        DarkMagenta   5
        DarkYellow    6
        Gray          7
        DarkGray      8
        Blue          9
        Green         10
        Cyan          11
        Red           12
        Magenta       13
        Yellow        14
        White         15
        ============  ===========

        Examples
        --------
        Logger.Write() is mainly used by other Logger Functions.

        Logger.WriteLine() utilize this function to write logs to console line, and change a new line
        for next log, by adding `\\n` in log parameter.

        >>> Logger.Write('{}\\n'.format(log), consoleColor, writeToFile, printToStdout, logFile)

        Logger.WriteFlush() utilize this function to write logs to console line, and will overwrite
        the current line with next log, by adding `\\r` in log parameter.

        >>> Logger.Write('{}\\r'.format(log), consoleColor, writeToFile, printToStdout, logFile)

        """
        if not isinstance(log, str):
            log = str(log)
        if printToStdout and sys.stdout:
            isValidColor = (
                consoleColor >= ConsoleColor.Black and consoleColor <= ConsoleColor.White)
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
                sys.stdout.write(ex.__class__.__name__ +
                                 ': can\'t print the log!')
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
                sys.stdout.write(ex.__class__.__name__ +
                                 ': can\'t write the log!')
        finally:
            if fout:
                fout.close()

    @staticmethod
    def WriteLine(log: Any, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        Write logs to Console with a new line

        Parameters
        ----------
        log : Any type. A string is preferred.
            Logs text
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).
        writeToFile : bool, optional.
            True to write logs into a file (default: True).
        printToStdout : bool, optional.
            True to print to standard output (default: True).
        logFile : str, optional.
            Logs file name (default: None). None to write to default log file '@AutomationLog.txt'
        printTruncateLen : int, optional.
            If <= 0, log is not truncated when print.

        Notes
        -----
        * This function utilize Logger.Write(), please see more details in Logger.Write().
        * Parameters of this functions must follow in Logger.Write() specification.

        Examples
        --------
        To easily utilize Logger.WriteLine() to log error or warning message for this package:

        >>> # The following line of code will log a message with Red color on console, representing an Error Message.
        >>> Logger.WriteLine('ERROR: This is an error message.'.format(log), consoleColor=ConsoleColor.Red)
        ERROR: This is an error message.

        >>> # The following line of code will log a message with Yellow color on console, representing a Warning Message.
        >>> Logger.WriteLine('Warning: This is a warning message.'.format(log), consoleColor=ConsoleColor.Red)
        Warning: This is a warning message.

        The following code by using Looger.Write() will have the same output as above:

        >>> # The following line of code will log a message with Red color on console, representing an Error Message.
        >>> Logger.Write('ERROR: This is an error message.\\n'.format(log), consoleColor=ConsoleColor.Red)
        ERROR: This is an error message.

        >>> # The following line of code will log a message with Yellow color on console, representing a Warning Message.
        >>> Logger.Write('Warning: This is a warning message.\\n'.format(log), consoleColor=ConsoleColor.Red)
        Warning: This is a warning message.

        """
        Logger.Write('{}\n'.format(log), consoleColor,
                     writeToFile, printToStdout, logFile)

    @staticmethod
    def WriteFlush(log: Any, consoleColor: int = ConsoleColor.Default, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None, printTruncateLen: int = 0) -> None:
        """
        Write logs to Console by overwriting the current line.

        Parameters
        ----------
        log : Any type. A string is preferred.
            Logs text
        consoleColor : int, optional.  A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).
        writeToFile : bool, optional.
            True to write logs into a file (default: True).
        printToStdout : bool, optional.
            True to print to standard output (default: True).
        logFile : str, optional.
            Logs file name (default: None). None to write to default log file '@AutomationLog.txt'
        printTruncateLen : int, optional.
            If <= 0, log is not truncated when print.

        Notes
        -----
        * This function utilize Logger.Write(), please see more details in Logger.Write().
        * Parameters of this functions must follow in Logger.Write() specification.

        Examples
        --------
        To easily utilize Logger.WriteFlush() to log error or warning message for this package:

        >>> # The following line of code will log a message with Red color on console, representing an Error Message.
        >>> Logger.WriteFlush('ERROR: This is an error message.'.format(log), consoleColor=ConsoleColor.Red)

        >>> # The following line of code will log a message with Yellow color on console, representing a Warning Message.
        >>> Logger.WriteFlush('Warning: This is a warning message.'.format(log), consoleColor=ConsoleColor.Red)

        The following code by using Looger.Write() will have the same output as above:

        >>> # The following line of code will log a message with Red color on console, representing an Error Message.
        >>> Logger.Write('ERROR: This is an error message.\\r'.format(log), consoleColor=ConsoleColor.Red)
        ERROR: This is an error message.

        >>> # The following line of code will log a message with Yellow color on console, representing a Warning Message.
        >>> Logger.Write('Warning: This is a warning message.\\r'.format(log), consoleColor=ConsoleColor.Red)
        Warning: This is a warning message.

        """
        Logger.Write('{}\r'.format(log), consoleColor,
                     writeToFile, printToStdout, logFile)

    @staticmethod
    def ColorfulWrite(log: str, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        Can write colorful logs to Console by using brackets.

        Parameters
        ----------
        log : Sting
            Logs text
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).
        writeToFile : bool, optional.
            True to write logs into a file (default: True).
        printToStdout : bool, optional.
            True to print to standard output (default: True).
        logFile : str, optional.
            Logs file name (default: None). None to write to default log file '@AutomationLog.txt'
        printTruncateLen : int, optional.
            If <= 0, log is not truncated when print.

        Notes
        -----
        * Parameters of this functions must follow in Logger.Write() specification.

        Examples
        --------
        Logger.ColorfulWrite() can print colorfull outputs by using brackets:

        >>> ColorfulWrite('Hello <Color=Green>Green</Color>!!')
        Hello Green!!

        where 'Hello' has default ConsoleColor (which is White), and 'Green' will be printed
        in ConsoleColor.Green (which is Green).

        The value on the right of `Color=Green` must be in Logger.ColorNames.

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
                text.append((log[index2 + 1:index3],
                            Logger.ColorNames[colorName]))
                start = index3 + 8
            else:
                if start < len(log):
                    text.append((log[start:], consoleColor))
                break
        for t, c in text:
            Logger.Write(t, c, writeToFile, printToStdout, logFile)

    @staticmethod
    def ColorfulWriteLine(log: str, consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        Can write colorful logs to Console with a new line by using brackets.

        Parameters
        ----------
        log : Sting
            Logs text
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).
        writeToFile : bool, optional.
            True to write logs into a file (default: True).
        printToStdout : bool, optional.
            True to print to standard output (default: True).
        logFile : str, optional.
            Logs file name (default: None). None to write to default log file '@AutomationLog.txt'
        printTruncateLen : int, optional.
            If <= 0, log is not truncated when print.

        Notes
        -----
        * This function utilize Logger.ColorfulWrite(), please see more details in Logger.ColorfulWrite().
        * Parameters of this functions must follow in Logger.Write() specification.

        Examples
        --------
        Logger.ColorfulWriteLine() can print colorfull outputs with a new line by using brackets:

        >>> ColorfulWriteLine('Hello <Color=Green>Green</Color>!!')
        Hello Green!!

        where 'Hello' has default ConsoleColor (which is White), and Green will be printed
        in ConsoleColor.Green (which is Green).

        The value on the right of `Color=Green` must be in Logger.ColorNames.

        The following code by using Looger.Write() will have the same output with same style as above:

        >>> Logger.ColorfulWrite('Hello <Color=Green>Green</Color>!!')
        Hello Green!!

        """
        Logger.ColorfulWrite(log + '\n', consoleColor,
                               writeToFile, printToStdout, logFile)

    @staticmethod
    def Log(log: Any = '', consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        Write logs to Console with current time information

        Parameters
        ----------
        log : Any type. A string is preferred.
            Logs text
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).
        writeToFile : bool, optional.
            True to write logs into a file (default: True).
        printToStdout : bool, optional.
            True to print to standard output (default: True).
        logFile : str, optional.
            Logs file name (default: None). None to write to default log file '@AutomationLog.txt'
        printTruncateLen : int, optional.
            If <= 0, log is not truncated when print.

        Notes
        -----
        * Parameters of this functions must follow in Logger.Write() specification.

        Examples
        --------
        >>> Logger.Log("This line used Logger.Log()!")
        2021-07-07 14:56:24.345 test.py[3] <module> -> This line used Logger.Log()!

        """
        frameCount = 1
        while True:
            frame = sys._getframe(frameCount)
            _, scriptFileName = os.path.split(frame.f_code.co_filename)
            if scriptFileName != Logger._SelfFileName:
                break
            frameCount += 1

        t = datetime.datetime.now()
        log = '{}-{:02}-{:02} {:02}:{:02}:{:02}.{:03} {}[{}] {} -> {}\n'.format(
            t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond // 1000, scriptFileName, frame.f_lineno, frame.f_code.co_name, log)
        Logger.Write(log, consoleColor, writeToFile, printToStdout, logFile)

    @staticmethod
    def ColorfulLog(log: str = '', consoleColor: int = -1, writeToFile: bool = True, printToStdout: bool = True, logFile: str = None) -> None:
        """
        Write colorful logs to Console with current time information by using brackets.

        Parameters
        ----------
        log : Any type. A string is preferred.
            Logs text
        consoleColor : int, optional. A value in class 'ConsoleColor' is preferred, such as `ConsoleColor.DarkGreen`.
            Text's color on console (default: ConsoleColor.White).
        writeToFile : bool, optional.
            True to write logs into a file (default: True).
        printToStdout : bool, optional.
            True to print to standard output (default: True).
        logFile : str, optional.
            Logs file name (default: None). None to write to default log file '@AutomationLog.txt'
        printTruncateLen : int, optional.
            If <= 0, log is not truncated when print.

        Notes
        -----
        * Parameters of this functions must follow in Logger.Write() specification.

        Examples
        --------
        >>> Logger.Log("This line used <Color=DarkGray>Logger.Log()</Color>!")
        2021-07-07 14:56:24.345 test.py[3] <module> -> This line used Logger.Log()!

        where 'This line used' and '!' has default ConsoleColor (which is White), and 'Logger.Log()' will be printed
        in ConsoleColor.DarkGray (which is DarkGray).

        The value on the right of `Color=DarkGray` must be in Logger.ColorNames.

        """
        frameCount = 1
        while True:
            frame = sys._getframe(frameCount)
            _, scriptFileName = os.path.split(frame.f_code.co_filename)
            if scriptFileName != Logger._SelfFileName:
                break
            frameCount += 1

        t = datetime.datetime.now()
        log = '{}-{:02}-{:02} {:02}:{:02}:{:02}.{:03} {}[{}] {} -> {}\n'.format(
            t.year, t.month, t.day, t.hour, t.minute, t.second, t.microsecond // 1000, scriptFileName, frame.f_lineno, frame.f_code.co_name, log)
        Logger.ColorfulWrite(
            log, consoleColor, writeToFile, printToStdout, logFile)

    @staticmethod
    def DeleteLog() -> None:
        """Delete the log file."""
        if os.path.exists(Logger.FileName):
            os.remove(Logger.FileName)


################################################################################
################################# Benchmarking #################################
################################################################################
class Benchmarking:
    """Benchmarking Methods for Automation Testing"""
    # BM stands for BenchMarking
    _ROTATE_ANGLE = [0, 90, 180, 270]

    _BM_WAIT_TIME_MIN = 0
    _BM_WAIT_TIME_MAX = 3

    _KEY_PRESS_WAIT_TIME_MIN = 0
    _KEY_PRESS_WAIT_TIME_MAX = 2

    _RANDOM_KEY_LIST = [
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

    _MOUSE_LIST = [
        "left_click",
        "right_click"
    ]
    # "view_upward",
    # "view_downward",
    # "view_leftward",
    # "view_rightward"

    # Logger Progress Bar width
    _WIDTH = 50

    @staticmethod
    def NormalTest(duration) -> None:
        """
        Perform a normal Benchmarking. No actions would be made.

        @param:
            - duration: duration to perform the normal benchmarking
        """
        Logger.CountProgress(duration, width=Benchmarking._WIDTH)
        # time.sleep(duration)

    @staticmethod
    def RandomControlTest(duration: int) -> None:
        """
        Perform a random Character Control for games.

        @param:
            - duration: duration to perform the random character control
        """
        waitTime = 0
        tmp = Benchmarking._RANDOM_KEY_LIST.copy()
        tmp.extend(Benchmarking._RANDOM_KEY_LIST)

        total = duration
        counts = 0
        Logger.WriteProgress(
            counts, total, width=Benchmarking._WIDTH)
        while(duration > 0):

            waitTime = random.uniform(
                Benchmarking._BM_WAIT_TIME_MIN, Benchmarking._BM_WAIT_TIME_MAX)
            keyTime = random.uniform(
                Benchmarking._KEY_PRESS_WAIT_TIME_MIN, Benchmarking._KEY_PRESS_WAIT_TIME_MAX)
            action = random.choice(tmp)

            if keyTime > duration:
                keyTime = int(duration / 2)
                waitTime = duration - keyTime

            if action in Benchmarking._MOUSE_LIST:
                Benchmarking.mouseCharacterControl(action, keyTime)
            elif action in Benchmarking._RANDOM_KEY_LIST:
                Benchmarking.keyCharacterControl(action, keyTime)

            duration -= keyTime
            counts += keyTime
            Logger.WriteProgress(
                counts, total, width=Benchmarking._WIDTH, unit="s")

            time.sleep(waitTime)

            duration -= waitTime
            counts += waitTime
            Logger.WriteProgress(
                counts, total, width=Benchmarking._WIDTH, unit="s")

    @staticmethod
    def RandomInputTest(duration, ) -> None:
        """
        Perform a random Typing Words for Office.

        @param:
            - duration: duration to perform the random typing
        """
        waitTime = 0

        total = duration
        counts = 0
        Logger.WriteProgress(
            counts, total, width=Benchmarking._WIDTH, unit="s")
        while(duration > 0):

            waitTime = random.uniform(
                Benchmarking._BM_WAIT_TIME_MIN, Benchmarking._BM_WAIT_TIME_MAX)
            keyTime = random.uniform(
                Benchmarking._KEY_PRESS_WAIT_TIME_MIN, Benchmarking._KEY_PRESS_WAIT_TIME_MAX)
            action = random.choice(_RANDOM_WORD_LIST)

            if keyTime > duration:
                keyTime = int(duration / 2)
                waitTime = duration - keyTime

            Benchmarking.keyCharacterControl(action, keyTime)

            duration -= keyTime
            counts += keyTime
            Logger.WriteProgress(
                counts, total, width=Benchmarking._WIDTH, unit="s")

            time.sleep(waitTime)

            duration -= waitTime
            counts += waitTime
            Logger.WriteProgress(
                counts, total, width=Benchmarking._WIDTH, unit="s")

    @staticmethod
    def RandomRotateTest(duration) -> None:
        """
        Perform a random screen rotating

        @param:
            - duration: duration to perform the random screen rotating
        """
        waitTime = 0
        altTabTime = 0

        total = duration
        counts = 0
        Logger.WriteProgress(
            counts, total, width=Benchmarking._WIDTH, unit="s")
        while(duration > 0):
            waitTime = random.uniform(5, 20)

            Benchmarking.changeDisplayDirection(
                0, random.choice(Benchmarking._ROTATE_ANGLE))

            time.sleep(waitTime)

            duration -= waitTime
            counts += waitTime
            Logger.WriteProgress(
                counts, total, width=Benchmarking._WIDTH, unit="s")

        Benchmarking.changeDisplayDirection(0, 0)

    @staticmethod
    def StressTest(duration) -> None:
        """
        Perform a stressed Benchmarking. Randomly performing an ALT+TAB action.

        @param:
            - duration: duration to perform the stressed benchmarking
        """
        waitTime = 0
        keyTime = 0

        total = duration
        counts = 0
        Logger.WriteProgress(
            counts, total, width=Benchmarking._WIDTH, unit="s")
        while(duration >= 0):

            waitTime = random.uniform(
                Benchmarking._BM_WAIT_TIME_MIN, Benchmarking._BM_WAIT_TIME_MAX)
            keyTime = random.uniform(
                Benchmarking._KEY_PRESS_WAIT_TIME_MIN, Benchmarking._KEY_PRESS_WAIT_TIME_MAX)

            if keyTime > duration:
                keyTime = int(duration / 2)
                waitTime = duration - keyTime

            Input.key_alt_tab()
            time.sleep(keyTime)
            duration -= keyTime
            counts += keyTime
            Logger.WriteProgress(
                counts, total, width=Benchmarking._WIDTH, unit="s")

            Input.key_alt_tab()
            time.sleep(waitTime)

            duration -= waitTime
            counts += waitTime
            Logger.WriteProgress(
                counts, total, width=Benchmarking._WIDTH, unit="s")

    @staticmethod
    def mouseCharacterControl(action, keyTime) -> None:
        """
        A method called by randomCharacterControl() to perform mouse control for characters.

        @param:
            - action: action to perform
            - keyTime: duration to perform the key time
        """
        res = keyTime
        if action == "view_upward":
            Input.moveTo(960, 1000, keyTime)
        if action == "view_downward":
            Input.moveTo(960, 80, keyTime)
        if action == "view_leftward":
            Input.moveTo(1800, 540), keyTime
        if action == "view_rightward":
            Input.moveTo(120, 540, keyTime)
        if action == "left_click":
            Input.clickLeft(None, None, keyTime)
        if action == "right_click":
            Input.clickRight(None, None, keyTime)

    @staticmethod
    def keyCharacterControl(action, keyTime, WriteProgress: bool = False) -> None:
        """
        A method called by randomCharacterControl() to perform keyboard control for characters.

        @param:
            - action: action to perform
            - keyTime: duration to perform the key time
        """
        # utils.input.key_input(action, keyTime)
        Input.callTinyTask('tinytask/'+action)
        if WriteProgress:
            Logger.CountProgress(
                0, keyTime, width=Benchmarking._WIDTH)
        else:
            time.sleep(keyTime)

    @staticmethod
    def changeDisplayDirection(deviceIndex, angle) -> bool:
        """
        Rotate the Display Screen's Direction

        @param:
            - deviceIndex - display device index
            - angle - angle to be rotated

        @RETURN:
            - True - succeed in rotating the screen.
            - False - failed to rotate the screen.
        """
        # if not hasDisplayDevice(deviceIndex):
        #     return
        try:
            device = win32api.EnumDisplayDevices(None, deviceIndex)
            dm = win32api.EnumDisplaySettings(
                device.DeviceName, win32con.ENUM_CURRENT_SETTINGS)
            if angle == 90:
                dm.DisplayOrientation = win32con.DMDO_90  # 待改变的值
                # 以下的720或者1280 代表我的屏幕的长宽
                # 在应用项目的时候,建议使用GetSystemMetrics 动态获取长宽
                # 在每次改变方向的时候,都要判断是否需要交换屏幕的长宽
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

            win32api.ChangeDisplaySettingsEx(device.DeviceName, dm)

            return True

        except Exception:
            return False


############################################################################
################################## VK_Code #################################
############################################################################
class VK_CODE():
    """Uses Two Dict to represent VK_CODE"""

    _VK_CODE1 = {
        'backspace': 0x08,
        'tab': 0x09,
        'clear': 0x0C,
        'enter': 0x0D,
        'shift': 0x10,
        'ctrl': 0x11,
        'alt': 0x12,
        'pause': 0x13,
        'caps_lock': 0x14,
        'esc': 0x1B,
        'spacebar': 0x20,
        'page_up': 0x21,
        'page_down': 0x22,
        'end': 0x23,
        'home': 0x24,
        'left_arrow': 0x25,
        'up_arrow': 0x26,
        'right_arrow': 0x27,
        'down_arrow': 0x28,
        'select': 0x29,
        'print': 0x2A,
        'execute': 0x2B,
        'print_screen': 0x2C,
        'ins': 0x2D,
        'del': 0x2E,
        'help': 0x2F,
        '0': 0x30,
        '1': 0x31,
        '2': 0x32,
        '3': 0x33,
        '4': 0x34,
        '5': 0x35,
        '6': 0x36,
        '7': 0x37,
        '8': 0x38,
        '9': 0x39,
        'a': 0x41,
        'b': 0x42,
        'c': 0x43,
        'd': 0x44,
        'e': 0x45,
        'f': 0x46,
        'g': 0x47,
        'h': 0x48,
        'i': 0x49,
        'j': 0x4A,
        'k': 0x4B,
        'l': 0x4C,
        'm': 0x4D,
        'n': 0x4E,
        'o': 0x4F,
        'p': 0x50,
        'q': 0x51,
        'r': 0x52,
        's': 0x53,
        't': 0x54,
        'u': 0x55,
        'v': 0x56,
        'w': 0x57,
        'x': 0x58,
        'y': 0x59,
        'z': 0x5A,
        'numpad_0': 0x60,
        'numpad_1': 0x61,
        'numpad_2': 0x62,
        'numpad_3': 0x63,
        'numpad_4': 0x64,
        'numpad_5': 0x65,
        'numpad_6': 0x66,
        'numpad_7': 0x67,
        'numpad_8': 0x68,
        'numpad_9': 0x69,
        'multiply_key': 0x6A,
        'add_key': 0x6B,
        'separator_key': 0x6C,
        'subtract_key': 0x6D,
        'decimal_key': 0x6E,
        'divide_key': 0x6F,
        'F1': 0x70,
        'F2': 0x71,
        'F3': 0x72,
        'F4': 0x73,
        'F5': 0x74,
        'F6': 0x75,
        'F7': 0x76,
        'F8': 0x77,
        'F9': 0x78,
        'F10': 0x79,
        'F11': 0x7A,
        'F12': 0x7B,
        'F13': 0x7C,
        'F14': 0x7D,
        'F15': 0x7E,
        'F16': 0x7F,
        'F17': 0x80,
        'F18': 0x81,
        'F19': 0x82,
        'F20': 0x83,
        'F21': 0x84,
        'F22': 0x85,
        'F23': 0x86,
        'F24': 0x87,
        'num_lock': 0x90,
        'scroll_lock': 0x91,
        'left_shift': 0xA0,
        'right_shift ': 0xA1,
        'left_control': 0xA2,
        'right_control': 0xA3,
        'left_menu': 0xA4,
        'right_menu': 0xA5,
        'browser_back': 0xA6,
        'browser_forward': 0xA7,
        'browser_refresh': 0xA8,
        'browser_stop': 0xA9,
        'browser_search': 0xAA,
        'browser_favorites': 0xAB,
        'browser_start_and_home': 0xAC,
        'volume_mute': 0xAD,
        'volume_Down': 0xAE,
        'volume_up': 0xAF,
        'next_track': 0xB0,
        'previous_track': 0xB1,
        'stop_media': 0xB2,
        'play/pause_media': 0xB3,
        'start_mail': 0xB4,
        'select_media': 0xB5,
        'start_application_1': 0xB6,
        'start_application_2': 0xB7,
        'attn_key': 0xF6,
        'crsel_key': 0xF7,
        'exsel_key': 0xF8,
        'play_key': 0xFA,
        'zoom_key': 0xFB,
        'clear_key': 0xFE,
        '+': 0xBB,
        ',': 0xBC,
        '-': 0xBD,
        '.': 0xBE,
        '/': 0xBF,
        '`': 0xC0,
        ';': 0xBA,
        '[': 0xDB,
        '\\': 0xDC,
        ']': 0xDD,
        "'": 0xDE
    }

    _VK_CODE2 = {
        'A': 'a',
        'B': 'b',
        'C': 'c',
        'D': 'd',
        'E': 'e',
        'F': 'f',
        'G': 'g',
        'H': 'h',
        'I': 'i',
        'J': 'j',
        'K': 'k',
        'L': 'l',
        'M': 'm',
        'N': 'n',
        'O': 'o',
        'P': 'p',
        'Q': 'q',
        'R': 'r',
        'S': 's',
        'T': 't',
        'U': 'u',
        'V': 'v',
        'W': 'w',
        'X': 'x',
        'Y': 'y',
        'Z': 'z',
        ')': '0',
        '!': '1',
        '@': '2',
        '#': '3',
        '$': '4',
        '%': '5',
        '^': '6',
        '&': '7',
        '*': '8',
        '(': '9',
        '=': '+',
        '<': ',',
        '_': '-',
        '>': '.',
        '?': '/',
        '~': '`',
        ':': ';',
        '{': '[',
        '|': '\\',
        '}': ']',
        '"': "'"
    }

    @staticmethod
    def getVK_CODE1() -> Dict[str, str]:
        """
        Return the first type of representation of VK_CODE

        @RETURN: The first type of representation of VK_CODE
        """
        return dict(VK_CODE._VK_CODE1)

    @staticmethod
    def getVK_CODE2() -> Dict[str, str]:
        """
        Return the second type of representation of VK_CODE

        @RETURN: The second type of representation of VK_CODE
        """
        return dict(VK_CODE._VK_CODE2)


_RANDOM_WORD_LIST = VK_CODE.getVK_CODE2().copy()
_RANDOM_WORD_LIST.update(VK_CODE.getVK_CODE1())
_RANDOM_WORD_LIST = list(_RANDOM_WORD_LIST.keys())


################################################################################
#################################### Input #####################################
################################################################################
class Input:
    """Assisting Input Methods"""

    @staticmethod
    def key_input(key, t=0.05):
        """
        Perform a key pressdown and pressup.

        @param:
            - key - a key to be pressed.
            - t - time period in second between pressdown and pressup (default to 0.05).

        @RETURN:
            - 1 - succeed in performing a key pressing process.
            - 0 - failed to perform a key pressing process.
        """
        if key in VK_CODE._VK_CODE2:
            key = VK_CODE._VK_CODE2[key]
        if key in VK_CODE._VK_CODE1:
            # Pressdown
            win32api.keybd_event(VK_CODE._VK_CODE1[key], 0, 0, 0)
            # Duration between pressdown and pressup
            time.sleep(t)
            # Pressup
            win32api.keybd_event(
                VK_CODE._VK_CODE1[key], 0, win32con.KEYEVENTF_KEYUP, 0)
            return 1
        return 0

    @staticmethod
    def key_inputs(str_input='', t=0.05) -> Literal[0, 1]:
        """
        Perform a serious of key pressdowns and pressups.

        @param:
            - string of keys - a string of keys to be pressed (default to '').
            - t - time period in second between each key to be pressed (default to 0.05).

        @RETURN:
            - 1 - succeed in performing a key pressing process.
            - 0 - failed to perform a key pressing process.
        """
        for k in str_input:
            keyInputStatusCode = Input.key_input(k)
            if not keyInputStatusCode:
                return keyInputStatusCode
            time.sleep(t)
        return keyInputStatusCode

    @staticmethod
    def key_alt_tab(t=0.5) -> None:
        """
        Perform a key action of ALT + TAB.

        @param:
            - t - time period in second between pressdown and pressup (default to 0.05).
        """
        win32api.keybd_event(VK_CODE._VK_CODE1["alt"], 0, 0, 0)
        win32api.keybd_event(VK_CODE._VK_CODE1["tab"], 0, 0, 0)
        time.sleep(t)
        win32api.keybd_event(
            VK_CODE._VK_CODE1["tab"], 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(
            VK_CODE._VK_CODE1["alt"], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def key_alt_f4(t=0.6) -> None:
        """
        Perform a key action of ALT + F4.

        @param:
            - t - time period in second between pressdown and pressup (default to 0.05).
        """
        duration = float('%.1f' % (t / 3))
        win32api.keybd_event(VK_CODE._VK_CODE1["alt"], 0, 0, 0)
        time.sleep(duration)
        win32api.keybd_event(VK_CODE._VK_CODE1["F4"], 0, 0, 0)
        time.sleep(duration)
        win32api.keybd_event(
            VK_CODE._VK_CODE1["F4"], 0, win32con.KEYEVENTF_KEYUP, 0)
        time.sleep(duration)
        win32api.keybd_event(
            VK_CODE._VK_CODE1["alt"], 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def clickLeft(x=None, y=None, duration=0) -> Tuple:
        """
        Perform a mouse action of left clicking on screen position at (x, y).

        @param:
            - x - horizontal position to be clicked.
            - y - vertical position to be clicked.
        """
        if x == None and y == None:
            x, y = win32api.GetCursorPos()
        # win32api.SetCursorPos((x, y))
        # time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
        time.sleep(duration)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)
        return x, y

    @staticmethod
    def clickRight(x=None, y=None, duration=0) -> Tuple:
        """
        Perform a mouse action of right clicking on screen position at (x, y).

        @param:
            - x - horizontal position to be clicked.
            - y - vertical position to be clicked.
        """
        if x == None and y == None:
            x, y = win32api.GetCursorPos()
        # win32api.SetCursorPos((x, y))
        # time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, x, y, 0, 0)
        time.sleep(duration)
        win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, x, y, 0, 0)
        return x, y

    @staticmethod
    def move(dest_x, dest_y, start_x=None, start_y=None, duration=0) -> Tuple:
        """
        Perform a mouse action to Input.move the mouse
        from (start_x, start_y) to (dest_x, dest_y) in duration time.

        @param:
            - dest_x - horizontal position to end
            - dest_y - vertical position to end
            - start_x - horizontal position to start
            - start_y - vertical position to start
            - duration - action's duration in seconds
        """
        if start_x == None:
            start_x = win32api.GetCursorPos()[0]
        if start_y == None:
            start_y = win32api.GetCursorPos()[1]
        win32api.SetCursorPos((start_x, start_y))
        pag.moveTo(dest_x, dest_y, duration=duration, tween=pag.easeInOutQuad)
        return dest_x, dest_y

    @staticmethod
    def moveTo(dest_x, dest_y, duration=0) -> None:
        """
        Perform a mouse action of clicking on screen position at (x, y).

        @param:
            - x - horizontal position to be clicked.
            - y - vertical position to be clicked.
        """
        start_x, start_y = win32api.GetCursorPos()
        Input.move(start_x, start_y, dest_x, dest_y, duration)

    @staticmethod
    def getMouse(t=0) -> None:
        """
        Get the mouse position and print in the console

        @param:
            - t - period to get the mouse position

        @RETURN:
            - (x, y) - a tuple which x represent the x-position of the mouse and y represent the y-position of the mouse.
        """
        try:
            while True:
                print("Press Ctrl-C to end")
                screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
                x, y = pag.position()  # 返回鼠标的坐标
                print("Screen size: (%s %s),  Position : (%s, %s)\n" %
                      (screenWidth, screenHeight, x, y))  # 打印坐标

                time.sleep(t)  # 每个1s中打印一次 , 并执行清屏
                os.system('cls')  # 执行系统清屏指令
        except KeyboardInterrupt:
            print('end')

    @staticmethod
    def logMouse(t=0) -> None:
        """
        Get the mouse position and print in the console only when the mouse position changes

        @param:
            - t - period to get the mouse position

        @RETURN:
            - (x, y) - a tuple which x represent the x-position of the mouse and y represent the y-position of the mouse.
        """
        try:
            x, y = pag.position()  # 返回鼠标的坐标
            while True:
                screenWidth, screenHeight = pag.size()  # 获取屏幕的尺寸
                xNew, yNew = pag.position()  # 返回鼠标的坐标
                if xNew != x and yNew != y:
                    print("Screen size: (%s %s),  Position : (%s, %s)\n" %
                          (screenWidth, screenHeight, x, y))  # 打印坐标
                    x, y = (xNew, yNew)

        except KeyboardInterrupt:
            os.system('cls')  # 执行系统清屏指令
            print('end')

    @staticmethod
    def callTinyTask(file) -> Any:
        """
        Calling the .exe file made by TinyTask

        @param:
            - file: a TinyTask File Name to be performed

        @RETURN:
            - 0 - failed
            - 1 - succeed
        """
        return win32api.ShellExecute(1, 'open', os.path.join(os.getcwd(), file), '', '', 1)


################################################################################
##################################### Game #####################################
################################################################################
class Game:
    """a Game Object to Save Game Automation Info"""

    def __init__(self, gameName: str = "",
                 steamDirectory: str = "", documentDirectory: str = "", benchDirectory: str = "",
                 exe: str = "", relativePath: str = "", absolutePath: str = "",
                 loopTimes: int = 1, mode: Literal[0, 1, 2, 3, 4] = 0) -> None:
        """
        mode:
            0- norm
            1- alt-tab
            2- randomControl
            3- randomInput
            4- randomRotate
        """
        self.gameName = gameName

        if not steamDirectory is None and not os.path.isdir(steamDirectory):
            self.steamDirectory = None
            Logger.WriteLine(
                'GAME() WARNING %s: BenchmarkAutomation is not initialized with a valid steamDirectory.' % gameName, ConsoleColor.Yellow)
        else:
            self.steamDirectory = steamDirectory

        if not documentDirectory is None and not os.path.isdir(documentDirectory):
            self.documentDirectory = None
            Logger.WriteLine(
                'GAME() WARNING %s: BenchmarkAutomation is not initialized with a valid documentDirectory.' % gameName, ConsoleColor.Yellow)
        else:
            self.documentDirectory = documentDirectory

        if not benchDirectory is None and not os.path.isdir(benchDirectory):
            self.benchDirectory = None
            Logger.WriteLine(
                'GAME() WARNING %s: BenchmarkAutomation is not initialized with a valid benchDirectory.' % gameName, ConsoleColor.Yellow)
        else:
            self.benchDirectory = benchDirectory

        self.exe = exe

        if not relativePath is None and not os.path.isdir(relativePath):
            self.relativePath = None
            Logger.WriteLine(
                'GAME() WARNING %s: BenchmarkAutomation is not initialized with a valid relativePath.' % gameName, ConsoleColor.Yellow)
        else:
            self.relativePath = relativePath

        if not absolutePath is None and not os.path.isdir(absolutePath) and not os.path.isabs(absolutePath):
            self.absolutePath = None
            Logger.WriteLine(
                'GAME() WARNING %s: BenchmarkAutomation is not initialized with a valid absolutePath.' % gameName, ConsoleColor.Yellow)
        else:
            self.absolutePath = absolutePath

        self.loopTimes = loopTimes

        if mode >= 0 and mode <= 4:
            self.mode = mode
        else:
            Logger.WriteLine(
                'GAME() WARNING %s: BenchmarkAutomation is not initialized with a valid mode.' % gameName, ConsoleColor.Yellow)

        self.exePath = ""
        self.launcherMode = -1

        self.LauncherWaitTime = 15

        self._START_ACTIONS = None
        self._QUIT_ACTIONS = None

    ################################ Base Info #################################
    def setGameName(self, name: str) -> None:
        """
        """
        self.gameName = name

    def getGameName(self) -> str:
        """
        """
        return self.gameName

    def setSteamDirectory(self, dir: str) -> None:
        """
        """
        self.steamDirectory = dir

    def getSteamDirectory(self) -> str:
        """
        """
        return self.steamDirectory

    def setDocumentDirectory(self, dir: str) -> None:
        """
        """
        self.documentDirectory = dir

    def getDocumentDirectory(self) -> str:
        """
        """
        return self.documentDirectory

    def setBenchDirectory(self, dir: str) -> None:
        """
        """
        self.benchDirectory = dir

    def getBenchDirectory(self) -> str:
        """
        """
        return self.benchDirectory

    def setRelativePath(self, dir: str) -> None:
        """
        """
        self.relativePath = dir

    def getRelativePath(self) -> str:
        """
        """
        return self.relativePath

    def setAbsolutePath(self, dir: str) -> None:
        """
        """
        self.absolutePath = dir

    def getAbsolutePath(self) -> str:
        """
        """
        return self.absolutePath

    ################################# Executor #################################
    def setExecutor(self, exe: str) -> None:
        """
        """
        self.exe = exe

    def getExecutor(self) -> str:
        """
        """
        return self.exe

    def setExecutorPath(self, exePath: str) -> None:
        """
        exePath:
        S/s- Steam
        R/r- Relative
        A/a- Abolute
        Other- Directly add to full .exe path
        """
        paths = exePath.split("/")

        full_exe = ""
        for p in paths:
            if str.lower(p) == "s":
                if self.getSteamDirectory() is None:
                    Logger.WriteLine(
                        "GAME() ERROR %s: try to join None Steam Directory." % self.getGameName(), ConsoleColor.Red)
                    return 0
                full_exe = os.path.join(full_exe, self.getSteamDirectory())
            elif str.lower(p) == "r":
                if self.getRelativePath() is None:
                    Logger.WriteLine(
                        "GAME() ERROR %s: try to join None Relative Path." % self.getGameName(), ConsoleColor.Red)
                    return 0
                full_exe = os.path.join(full_exe, self.getRelativePath())
            elif str.lower(p) == "a":
                if self.getAbsolutePath() is None:
                    Logger.WriteLine(
                        "GAME() ERROR %s: try to join None Absolute Path." % self.getGameName(), ConsoleColor.Red)
                    return 0
                full_exe = os.path.join(full_exe, self.getAbsolutePath())
            else:
                full_exe = os.path.join(full_exe, p)

        self.exePath: str = full_exe

    def getExecutorPath(self) -> str:
        """
        """
        return self.exePath

    ################################# Launcher #################################
    def setLauncherMode(self, mode: Literal[0, 1, 2, 3]) -> None:
        """
        0- No launcher
        1- UIAutomation
        2- Click on given position
        3- call TinyTask
        """
        self.launcherMode = mode

    def getLauncherMode(self) -> Literal[0, 1, 2, 3]:
        """
        0- No launcher
        1- UIAutomation
        2- Click on given position
        3- call TinyTask
        """
        return self.launcherMode

    def setLauncher(self, waitTime: int = 20,
                    uiAppControlType: str = None, uiAppName: str = None,
                    uiStartControlType: str = None, uiStartIndex: int = None, uiStartName: str = None,
                    clickPos: tuple = None,
                    TinyTaskName: str = None) -> None:
        """
        """
        self.LauncherWaitTime = waitTime
        if not self.hasLauncher():
            Logger.WriteLine(
                'GAME() WARNING %s: Launcher Mode is not enabled.' % self.getGameName(), ConsoleColor.Yellow)
            return
        if self.getLauncherMode() == 1:
            ## 1 - UIAutomation
            self.uiAppControlType: str = uiAppControlType
            self.uiAppName: str = uiAppName
            self.uiStartControlType: str = uiStartControlType
            self.uiStartName: str = uiStartName
            if uiStartIndex is None and not uiStartName is None:
                self.uiStartIndex = 0
            else:
                self.uiStartIndex: int = uiStartIndex
        elif self.getLauncherMode() == 2:
            # 2 - click on given position
            if clickPos is None:
                Logger.WriteLine(
                    'GAME() ERROR %s: clickPos should not be None.' % self.getGameName(), ConsoleColor.Red)
                return
            self.clickPos: tuple = clickPos
        elif self.getLauncherMode() == 3:
            # 3 - call TinyTask
            if TinyTaskName is None:
                Logger.WriteLine(
                    'GAME() ERROR %s: TinyTaskName should not be None.' % self.getGameName(), ConsoleColor.Red)
                return
            self.TinyTaskName: str = TinyTaskName

    def hasLauncher(self) -> bool:
        """
        """
        return self.getLauncherMode() > 0 and self.getLauncherMode() <= 3

    ################################# Actions ##################################
    def setStartActions(self, actions: List[List[Any]]):
        """
        """
        self._START_ACTIONS = actions

    def getStartActions(self):
        """
        """
        return self._START_ACTIONS

    def setQuitActions(self, actions: List[List[Any]]):
        """
        """
        self._QUIT_ACTIONS = actions

    def getQuitActions(self):
        """
        """
        return self._QUIT_ACTIONS

    def startActions(self, actions: List[List[Any]]) -> int:
        """
        [["w", "wait", duration],
         ["k", key, duration],
         ["ks", keys, duration],
         ["cl", (x, y), duration],
         ["cr", (x, y), duration],
         ["mv", (x, y), duration],
         ["t", "TinyTaskName", duration],
         ["s", "key_alt_tab | key_alt_f4", duration]]
        """
        try:
            num = 0
            for action in actions:
                if not isinstance(action, List):
                    Logger.WriteLine(
                        'GAME() ERROR %s: Actions() actions Type error' % self.getGameName(), ConsoleColor.Red)
                    return 0

                ActionType, tar, duration = action

                Logger.WriteFlush('Performing Action %s %s : At %s in %s seconds' % (
                    num, ActionType, tar, duration), ConsoleColor.DarkGray)
                num += 1

                ActionType = str.lower(ActionType)
                if not ActionType in ["w", "k", "ks", "cl", "cr", "mv", "t", "s"]:
                    Logger.WriteLine('GAME() ERROR %s: Invalid ActionType %s' % (
                        self.getGameName(), ActionType), ConsoleColor.Red)
                    return 0
                if not isinstance(duration, int) and not isinstance(duration, float):
                    Logger.WriteLine('GAME() ERROR %s: Invalid Duration %s' % (
                        self.getGameName(), duration), ConsoleColor.Red)
                    return 0
                if ActionType == "w":
                    # time.sleep(duration)
                    Logger.CountProgress(
                        duration, log="Waiting", consoleColor=ConsoleColor.DarkGray)
                    resCode = duration

                if not isinstance(tar, str) and not isinstance(tar, Tuple):
                    Logger.WriteLine('GAME() ERROR %s: Invalid TargetType %s' % (
                        self.getGameName(), tar), ConsoleColor.Red)
                    return 0

                # k - Single key
                if ActionType == "k":
                    resCode = Input.key_input(tar, duration)

                # ks - Multiple Keys
                if ActionType == "ks":
                    resCode = Input.key_inputs(tar, duration)

                # cl - Left-Click
                if ActionType == "cl":
                    x, y = tar
                    resCode = sum(Input.clickLeft(x, y, duration))

                # cr - Right-Click
                if ActionType == "cr":
                    x, y = tar
                    resCode = sum(Input.clickRight(x, y, duration))

                # mv - Move mouse position
                if ActionType == "mv":
                    x, y = tar
                    resCode = sum(Input.moveTo(x, y, duration))

                # t - Call TinyTask
                if ActionType == "t":
                    resCode = Input.callTinyTask(tar)
                    time.sleep(duration)

                # s - Special Function in Input Class
                if ActionType == "s":
                    if tar == "key_alt_tab":
                        Input.key_alt_tab(duration)
                    if tar == "key_alt_f4":
                        Input.key_alt_f4(duration)
                    resCode = duration

                if not resCode:
                    Logger.WriteLine(
                        'GAME() ERROR %s: Action %s Failed in Actions()' % (self.getGameName(), action), ConsoleColor.Red)
        except Exception as e:
            Logger.WriteLine(
                'GAME() ERROR %s: %s' % (self.getGameName(), e), ConsoleColor.Red)
        else:
            return resCode

    def start(self):
        """
        """
        return self.startActions(self.getStartActions())

    def quit(self):
        """
        """
        return self.startActions(self.getQuitActions())

    ############################### Benchmarking ###############################
    def setBenchmarkingMode(self, mode: int) -> None:
        """
        """
        self.mode = mode

    def getBenchmarkingMode(self) -> int:
        """
        """
        return self.mode

    def startBenchMarking(self, duration: int = 300) -> None:
        """
        mode:
            0- norm
            1- alt-tab
            2- randomControl
            3- randomInput
            4- randomRotate
        """
        # Normal Benchmarking
        if self.getBenchmarkingMode() == 0:
            Benchmarking.NormalTest(duration)
        # Alt-Tab Benchmarking
        elif self.getBenchmarkingMode() == 1:
            Benchmarking.StressTest(duration)
        # Random-Control Benchmarking
        elif self.getBenchmarkingMode() == 2:
            Benchmarking.RandomControlTest(duration)
        # Random-Input Benchmarking
        elif self.getBenchmarkingMode() == 3:
            Benchmarking.RandomInputTest(duration)
        # Random-Rotate Benchmarking
        elif self.getBenchmarkingMode() == 4:
            Benchmarking.RandomRotateTest(duration)
        else:
            Logger.WriteLine("GAME() ERROR %s: Benchmarking Mode %s is not valid" %
                             (self.getGameName(), self.getBenchmarkingMode()), ConsoleColor.Red)

    ################################## Launch ##################################
    def checkLaunch(self) -> bool:
        """
        """
        if self.getExecutor() is None:
            Logger.WriteLine(
                'GAME() ERROR %s: Executor is None. Please use setExecutor() to initialize first.' % self.getGameName(), ConsoleColor.Red)
            return False
        if self.getExecutorPath() is None:
            Logger.WriteLine(
                'GAME() ERROR %s: Executor Path is None. Please use setExecutorPath() to initialize first.' % self.getGameName(), ConsoleColor.Red)
            return False
        exeLocation = os.path.join(self.getExecutorPath(), self.getExecutor())
        if not os.path.isfile(exeLocation):
            Logger.WriteLine(
                'GAME() ERROR %s: Executor\'s Full Path is not valid. Current Path: %s' % (self.getGameName(), exeLocation), ConsoleColor.Red)
            return False

        # Check Executor
        if self.hasLauncher():
            # Using UIAutomation
            if self.getLauncherMode() == 1:
                # Check APP
                if self.uiAppControlType is None:
                    Logger.WriteLine(
                        'GAME() ERROR %s: uiAppControlType should not be None.' % self.getGameName(), ConsoleColor.Red)
                    return False
                if self.uiAppName is None:
                    Logger.WriteLine(
                        'GAME() ERROR %s: uiAppName should not be None.' % self.getGameName(), ConsoleColor.Red)
                    return False
                # Check Start Button
                if self.uiStartControlType is None:
                    Logger.WriteLine(
                        'GAME() ERROR %s: uiStartControlType should not be None.' % self.getGameName(), ConsoleColor.Red)
                    return False
                if self.uiStartName is None:
                    Logger.WriteLine(
                        'GAME() ERROR %s: uiStartName should not be None.' % self.getGameName(), ConsoleColor.Red)
                    return False
                if self.uiStartIndex is None and self.uiStartName is None:
                    Logger.WriteLine(
                        'GAME() ERROR %s: uiStartIndex or uiStartName should not be None.' % self.getGameName(), ConsoleColor.Red)
                    return False
            # Using win32 Mouse Click Action
            elif self.getLauncherMode() == 2:
                if self.clickPos is None:
                    Logger.WriteLine(
                        'GAME() ERROR %s: clickPos should not be None.' % self.getGameName(), ConsoleColor.Red)
                    return False
            # Calling TinyTask executor
            elif self.getLauncherMode() == 3:
                if self.TinyTaskName is None:
                    Logger.WriteLine(
                        'GAME() ERROR %s: TinyTaskName should not be None.' % self.getGameName(), ConsoleColor.Red)
                    return False

        return True

    def launch(self, GameWaitTime: int = 60) -> int:
        """
        """
        startGame: int = 0

        self.checkLaunch()

        # Open Game
        exe = os.path.join(self.getExecutorPath(), self.getExecutor())
        try:
            startGame = win32api.ShellExecute(1, 'open', exe, '', '', 1)

            if self.hasLauncher:
                Logger.WriteLine(
                    'waiting %s seconds for launcher to start......' % self.LauncherWaitTime, ConsoleColor.Gray)
                Logger.CountProgress(self.LauncherWaitTime)
                # time.sleep(self.LauncherWaitTime)

                # Using UIAutomation
                if self.getLauncherMode() == 1:
                    if self.uiAppControlType == "PaneControl":
                        app = auto.PaneControl(
                            searchDepth=1, Name=self.uiAppName)
                    elif self.uiAppControlType == "WindowControl":
                        app = auto.WindowControl(
                            searchDepth=1, Name=self.uiAppName)
                    elif self.uiAppControlType == "ImageControl":
                        app = auto.ImageControl(
                            searchDepth=1, Name=self.uiAppName)
                    elif self.uiAppControlType == "ButtonControl":
                        app = auto.ButtonControl(
                            searchDepth=1, Name=self.uiAppName)
                    else:
                        Logger.WriteLine(
                            "GAME() ERROR %s: %s is not recognized as a ControlType. Please check again or report this issue." % (self.getGameName(), self.uiAppControlType), ConsoleColor.Red)
                        return 0

                    # Set the launcher window to the very top of the screen
                    app.SetTopmost(True)

                    # Click on Start Button
                    if self.uiStartControlType == "PaneControl":
                        auto.PaneControl(
                            foundIndex=self.uiStartIndex, Name=self.uiStartName).Click()
                    elif self.uiStartControlType == "WindowControl":
                        auto.WindowControl(
                            foundIndex=self.uiStartIndex, Name=self.uiStartName).Click()
                    elif self.uiStartControlType == "ImageControl":
                        auto.ImageControl(
                            foundIndex=self.uiStartIndex, Name=self.uiStartName).Click()
                    elif self.uiStartControlType == "ButtonControl":
                        auto.ButtonControl(
                            foundIndex=self.uiStartIndex, Name=self.uiStartName).Click()
                    else:
                        Logger.WriteLine(
                            "GAME() ERROR %s: %s is not recognized as a ControlType. Please check again or report this issue." % (self.getGameName(), self.uiStartControlType), ConsoleColor.Red)
                        return 0

                # Using win32 Mouse Click Action
                elif self.getLauncherMode() == 2:
                    xClickPos, yClickPos = self.clickPos
                    Input.clickLeft(xClickPos, yClickPos)

                # Calling TinyTask executor
                elif self.getLauncherMode() == 3:
                    Input.callTinyTask(self.TinyTaskName)

            Logger.WriteLine(
                'waiting %s seconds for Game to start......' % GameWaitTime, ConsoleColor.Gray)
            Logger.CountProgress(GameWaitTime)
            # time.sleep(GameWaitTime )
        except Exception as e:
            Logger.WriteLine('GAME() ERROR %s: %e' %
                             (self.getGameName(), e), ConsoleColor.Gray)

        # Dealling In-Game Start Buttons

        return startGame


################################################################################
############################# BenchmarkAutomation ##############################
################################################################################
class BenchmarkAutomation:
    """
    """

    def __init__(self, steamDirectory: str = "", documentDirectory: str = "",
                 OverallLoopTimes: int = 1, GameLoopTimes: int = -1, BenchmarkingTime: int = 600) -> None:
        """
        """
        if not steamDirectory is None and not os.path.isdir(steamDirectory):
            self.steamDirectory = None
            Logger.WriteLine(
                'BA() WARNING: BenchmarkAutomation is not initialized with a valid steamDirectory.', ConsoleColor.Yellow)
        else:
            self.steamDirectory = steamDirectory

        if not documentDirectory is None and not os.path.isdir(documentDirectory):
            self.documentDirectory = None
            Logger.WriteLine(
                'BA() WARNING: BenchmarkAutomation is not initialized with a valid documentDirectory.', ConsoleColor.Yellow)
        else:
            self.documentDirectory = documentDirectory

        self.gameList = dict()

        self.OverallLoopTimes = OverallLoopTimes
        self.GameLoopTimes = GameLoopTimes

        self.BenchmarkingTime = BenchmarkingTime

    ################################ Base Info #################################
    def addGameList(self, gameName: str, gameObj: Game = None,
                    exe: str = "", relativePath: str = "", absolutePath: str = "",
                    mode: int = 0) -> Any:
        """
        """
        if gameName is None:
            Logger.WriteLine(
                'BA() ERROR: addGameList() should be called with at least 1 arguments', ConsoleColor.Red)
        try:
            if not gameObj is None:
                self.gameList[gameName] = gameObj
            else:
                self.gameList[gameName] = Game(
                    gameName=gameName, steamDirectory=self.getSteamDirectory, documentDirectory=self.getDocumentDirectory(),
                    exe=exe, relativePath=relativePath, absolutePath=absolutePath,
                    loopTimes=self.getGameLoopTimes(), mode=mode)
        except Exception:
            Logger.WriteLine(
                'BA() ERROR: Unknown Error addGameList()', ConsoleColor.Red)

    def getGameList(self) -> List:
        """
        """
        return list(self.gameList.keys())

    def setSteamDirectory(self, dir: str) -> None:
        """
        """
        self.steamDirectory = dir

    def getSteamDirectory(self) -> str:
        """
        """
        return self.steamDirectory

    def setDocumentDirectory(self, dir: str) -> None:
        """
        """
        self.documentDirectory = dir

    def getDocumentDirectory(self) -> str:
        """
        """
        return self.documentDirectory

    def setOverallLoopTimes(self, tar: int) -> None:
        """
        """
        self.OverallLoopTimes = tar

    def getOverallLoopTimes(self) -> int:
        """
        """
        return self.OverallLoopTimes

    def setGameLoopTimes(self, tar: int) -> None:
        """
        """
        self.GameLoopTimes = tar

    def getGameLoopTimes(self) -> int:
        """
        """
        return self.GameLoopTimes

    def setBenchmarkTime(self, tar: int) -> None:
        """
        """
        self.BenchmarkingTime = tar

    def getBenchmarkTime(self) -> int:
        """
        """
        return self.BenchmarkingTime

    ################################## Start ###################################
    def checkStart(self) -> bool:
        """
        """
        if self.getSteamDirectory() is None:
            Logger.WriteLine(
                'BA() ERROR: SteamDirectory is None. Please use setSteamDirectory() to initialize first.', ConsoleColor.Red)
            return False

        if self.getOverallLoopTimes() < 1:
            Logger.WriteLine(
                'BA() ERROR: OverallLoopTimes is less than 1. Please use setOverallLoopTimes() to reset first.', ConsoleColor.Red)
            return False

        if self.getBenchmarkTime() < 10:
            Logger.WriteLine(
                'BA() ERROR: BenchmarkTime is less than 10 seconds. Use setBenchmarkTime() to modify.', ConsoleColor.Red)
            return False

        if self.getGameList() is None:
            Logger.WriteLine(
                'BA() ERROR: GameList is None. Please use addGameList() to initialize first.', ConsoleColor.Red)
            return False
        for game in self.getGameList():
            checkCode = self.gameList[game].checkStart()
            if not checkCode:
                Logger.WriteLine(
                    'BA() ERROR: Game %s failed to passed the checkStart(). Please examine its Info again' % game, ConsoleColor.Red)
                return False

        if self.getGameLoopTimes() < -1:
            Logger.WriteLine(
                'BA() INFO: GameLoopTimes is negative. Game will only run once regarding success or failure. Use setGameLoopTimes() to modify.', ConsoleColor.White)

        if self.getBenchmarkTime() < 60:
            Logger.WriteLine(
                'BA() WARNING: BenchmarkTime is less than 1 min. Use setBenchmarkTime() to modify.', ConsoleColor.Yellow)

    def start(self) -> int:
        """
        """
        try:
            res = dict()
            for game in self.getGameList():
                if not game in res:
                    res[game] = []

                if self.getGameLoopTimes() < 1:
                    startCode, quitCode = self._start(game)
                    res[game].append((startCode, quitCode))
                    Logger.WriteLine("BA() FINISHED %s: Start Code %s and Quit Code %s" % (
                        game, startCode, quitCode))
                    continue
                for i in range(self.getGameLoopTimes()):
                    startCode, quitCode = self._start(game)
                    res[game].append((startCode, quitCode))
                    Logger.WriteLine("BA() FINISHED %s: Start Code %s and Quit Code %s" % (
                        game, startCode, quitCode))
            return res
        except Exception as e:
            Logger.WriteLine(
                'BA() ERROR: %s' % e, ConsoleColor.Red)
            return

    def _start(self, game: str) -> Tuple[int, int]:
        """
        """
        startCode = self.gameList[game].launch(GameWaitTime=30)
        startCode = self.gameList[game].start()
        self.gameList[game].startBenchMarking(self.getBenchmarkTime())
        quitCode = self.gameList[game].quit()
        return startCode, quitCode

    ############################## Helper Methods ##############################
    ################################### WIN ####################################
    @staticmethod
    def searchFile(pathname, filename):
        """
        Return all matched files under a specific path.

        @param:
            - pathname - a specific path to search for.
            - filename - a filename to search for (Regular Expression can be used).

        @RETURN:
            - A list of sting representing all matched file names
        """
        matchedFile = []
        for root, dirs, files in os.walk(pathname):
            for file in files:
                if re.match(filename, file):
                    file_name = os.path.abspath(os.path.join(root, file))
                    matchedFile.append(file_name)
        return matchedFile

    @staticmethod
    def killProgress(process):
        """
        A function call a terminal and utilize CMD command to kill a progress.

        @param:
            - process - a process to be forced to kill.

        @RETURN:
            - non-Zero - succeed to call the terminal for killing the process.
            - 0 - failed to open the terminal.
            - -1 - EXCEPTION occurred.
        """
        # return os.system('taskkill /F /IM %s'%name) # An alternative way to kill a process.
        statusCode = 0
        try:
            statusCode = subprocess.Popen(
                'taskkill /F /IM %s' % process, close_fds=True)
        except Exception:
            return 0
        else:
            return statusCode

    ################################### Json ###################################
    @staticmethod
    def read_json(file) -> Dict:
        """
        Read a .json file and return a json type.

        @param:
            - file - a filename to be read as .json data.

        @RETURN:
            - A Python's Data Object representing the data in the .json file.
        """
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if data == None:
                data = dict()
            return data
        except Exception:
            Logger.WriteLine('ERROR: Unable to read %s' %
                             (data, file), ConsoleColor.Red)
            return None

    @staticmethod
    def write_json(file, data) -> bool:
        """
        Over-write the .json file with input data.

        @param:
            - file - a filename to be write.
            - data - data to write in the .json file

        @RETURN:
            - True - Succeed to Write data in json
            - False - Exception occurred
        """
        try:
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            return True
        except Exception:
            Logger.WriteLine('ERROR: Unable to write %s in %s' %
                             (data, file), ConsoleColor.Red)
            return False

    @staticmethod
    def printAll(data):
        """
        Print everything in the data Object
        """
        if type(data) == type(str()):
            print(data)
        else:
            for d in data:
                print(d)

    ############################### Crash Dumps ################################
    @staticmethod
    def detectCrashDumps(tar="MEMORY.DMP") -> Tuple[list, list]:
        """
        Detect whether the window's dump is generated under %LOCALAPPDATA%\CrashDumps

        @param:
            - tar - the target path to copy to (default to "C:\WinDumps")

        @RETURN:
            - True - The dump file is detected
            - False - otherwise, the file is not detected
        """
        # path = "%LOCALAPPDATA%\CrashDumps"
        src1 = os.path.expandvars(r'%LOCALAPPDATA%\CrashDumps')
        src2 = os.path.expandvars(r'C:\Windows')
        return BenchmarkAutomation.searchFile(src1, tar), BenchmarkAutomation.searchFile(src2, "MEMORY.DMP")

    @staticmethod
    def dealCrashDumps(tar="C:\\WinDumps") -> None:
        """
        Copy the Windows dump file to the desired location and remove the dump files under %LOCALAPPDATA%\CrashDumps

        @param:
            - tar - the target path to copy to (default to "C:\WinDumps")
        """

        dst = tar
        files1, files2 = BenchmarkAutomation.detectCrashDumps()
        while files1 + files2:

            ####################################################################
            # New Code
            src = os.path.expandvars(r'%LOCALAPPDATA%\CrashDumps')
            for files in os.listdir(src):
                if files == "MEMORY.DMP":
                    dst_name = os.path.join(
                        dst, "MEMORY_%s.DMP" % datetime.datetime.now().strftime("%m.%d-%H%M-%Y"))
                else:
                    dst_name = os.path.join(dst, files)
                src_name = os.path.join(src, files)
                if os.path.isfile(src_name):
                    exe = 'copy ' + src_name + ' %s' % dst_name
                    os.system(exe)
                    if BenchmarkAutomation.searchFile(src, files):
                        os.system('del '+src_name)
                else:
                    print("TAR is not a file!")

            src = "C:\\Windows"
            for files in files2:
                dst_name = os.path.join(
                    dst, "[Windows]MEMORY_%s.DMP" % datetime.datetime.now().strftime("%m.%d-%H%M-%Y"))
                src_name = files
                if os.path.isfile(src_name):
                    exe = 'copy ' + src_name + ' %s' % dst_name
                    os.system(exe)
                    if BenchmarkAutomation.searchFile(src, "MEMORY.DMP"):
                        os.system('del '+src_name)

            # TODO optional: cmd command=> xcopy /s/e "D:\A_FOLDER" "E:\B_FOLDER\"
            files1, files2 = BenchmarkAutomation.detectCrashDumps()

        ########################################################################
        # Past Code
        # # Copy the dump file
        # tarFile = "MEMORY_" + datetime.datetime.now().strftime("%m.%d-%H%M-%Y")
        # if not tar is None:
        #     exe = 'copy %LOCALAPPDATA%\CrashDumps\MEMORY.DMP '+tar+'\%s.DMP'%tarFile
        #     res = tar+'\%s.DMP'%tarFile
        # else:
        #     exe = 'copy %LOCALAPPDATA%\CrashDumps\MEMORY.DMP %s.DMP'%tarFile
        #     res = '\%s.DMP'%tarFile
        # os.system(exe)
        # if searchFile(tar, tarFile):
        #     os.system('del %LOCALAPPDATA%\CrashDumps\MEMORY.DMP')
        #     return res
