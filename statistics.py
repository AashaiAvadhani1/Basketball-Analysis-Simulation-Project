#later be able to replace the gameID with a variable that changes based
#on the game being played

import csv
import pandas
import time
from tkinter import *
import tkinter as tk

class StatisticsMethods():

    def __init__(self):
        pass



#researched the time library documentation
    def convertTimeLeftToStringFormat(timeLeft):
        secondToStringFormatConversion = time.strftime('%M:%S', time.gmtime(timeLeft))
        return secondToStringFormatConversion
