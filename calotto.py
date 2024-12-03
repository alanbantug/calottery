import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename

from openpyxl import load_workbook
from openpyxl.comments import Comment

import os

import threading

from time import time, sleep
from datetime import datetime, timedelta

import subprocess as sp

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables

        self.origin = os.getcwd()

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", anchor="center")
        Style().configure("B.TLabel", font="Verdana 8", background="white", width="20")
        Style().configure("G.TLabel", font="Verdana 8")
        Style().configure("L.TLabel", font="Courier 40 bold", width="8")
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")

        # Set button styles
        Style().configure("B.TButton", font="Verdana 8", relief="ridge")

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TRadiobutton", font="Verdana 8")
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        # Create widgets
        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_b = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_c = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_d = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_e = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_f = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_g = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_h = Separator(self.main_container, orient=HORIZONTAL)
        self.sep_i = Separator(self.main_container, orient=HORIZONTAL)
        self.mainLabel = Label(self.main_container, text="MY LOTTERY PLAYGROUND", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="This is my Lottery playground where I play around with various ways", style="S.TLabel" )
        self.subLabelB = Label(self.main_container, text="of generating and analyzing results of all the draw games in the  ", style="S.TLabel" )
        self.subLabelC = Label(self.main_container, text="California Lottery. ", style="S.TLabel" )

        self.fantasy = Button(self.main_container, text="Fantasy", style="B.TButton", command=self.showFantasy)
        self.super = Button(self.main_container, text="Super", style="B.TButton", command=self.showSuper)
        self.power = Button(self.main_container, text="Power", style="B.TButton", command=self.showPower)
        self.mega = Button(self.main_container, text="Mega", style="B.TButton", command=self.showMega)
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        # Position widgets
        self.mainLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')
        
        self.sep_a.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.subLabelA.grid(row=2, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.subLabelB.grid(row=3, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')
        self.subLabelC.grid(row=4, column=0, columnspan=2, padx=5, pady=0, sticky='NSEW')

        self.sep_b.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.fantasy.grid(row=6, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.super.grid(row=6, column=1, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.power.grid(row=7, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.mega.grid(row=7, column=1, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.sep_c.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.exit.grid(row=9, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

    def showFantasy(self):
        
        f = threading.Thread(None, self.fantasyThread, ())
        f.start()

    def fantasyThread(self):
        
        # os.system('python fantasy.py')
        os.system('python C:/Users/Alan/Scripts/Code/calottery/fantasy.py')

    def showSuper(self):
        
        s = threading.Thread(None, self.superThread, ())
        s.start()

    def superThread(self):
        
        # os.system('python super.py')
        os.system('python C:/Users/Alan/Scripts/Code/calottery/super.py')

    def showPower(self):
        
        p = threading.Thread(None, self.powerThread, ())
        p.start()

    def powerThread(self):
        
        # os.system('python power.py')
        os.system('python C:/Users/Alan/Scripts/Code/calottery/power.py')

    def showMega(self):
        
        m = threading.Thread(None, self.megaThread, ())
        m.start()

    def megaThread(self):
        
        # os.system('python mega.py')
        os.system('python C:/Users/Alan/Scripts/Code/calottery/mega.py')

root = Tk()
root.title("MY LOTTERY PLAYGROUND")

# Set size

wh = 230
ww = 420

root.resizable(height=False, width=False)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
