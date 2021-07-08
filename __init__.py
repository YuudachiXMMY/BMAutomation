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

from BenchmarkAutomation import *