import tkinter
import os

from tkinter import *
from tkinter import font
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk
from itertools import combinations
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import threading
import random

import dbaccess as db
import displayGenerate as dg

class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # variables
        self.numberA = StringVar()
        self.numberB = StringVar()
        self.numberC = StringVar()
        self.numberD = StringVar()
        self.numberE = StringVar()
        self.numberS = StringVar()

        self.offset = StringVar()

        self.sortOrder = IntVar()
        self.sortSuperOrder = IntVar()

        self.topCount = IntVar()
        self.noClose = IntVar()
        self.skipWinner = IntVar()
        self.noCon = IntVar()
        self.pattern = IntVar()

        self.generated = []

        self.varCountLimit = StringVar()
        self.limitList = ['5', '5', '4', '3', '2']
        rfont = font.Font(family='Verdana', size=8)
        lfont = font.Font(family='Verdana', size=8, slant="italic")
        bfont = font.Font(family='Verdana', size=16, weight="bold")
        efont = font.Font(family='Verdana', size=16)

        # Set button styles
        Style().configure("B.GButton", font="Verdana 8", relief="raised", height=10)
        Style().configure("B.TButton", font=bfont, relief="raised", height=20)
        Style().configure("E.TButton", font=efont, relief="raised", height=20)
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("B.TRadiobutton", font="Verdana 8")

        # Set label styles
        Style().configure("M.TLabel", font="Verdana 12 bold")
        Style().configure("T.TLabel", font="Verdana 8")
        Style().configure("B.TLabel", font=lfont, foreground="blue")
        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")
        Style().configure("F.TButton", font=rfont, relief="raised", height=20)

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))
        self.headerA  = Label(self.main_container, text="Super Lotto", style="M.TLabel" )
        self.headerB = Label(self.main_container, text="Play and enjoy the Super Lotto game fro CA Lottery", style="T.TLabel" )

        self.parentTab = Notebook(self.main_container)
        self.dataTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.statTab = Frame(self.parentTab)   # second page
        self.generateTab = Frame(self.parentTab)   # second page
        self.parentTab.add(self.dataTab, text='   Data     ')
        self.parentTab.add(self.statTab, text='   Stats     ')
        self.parentTab.add(self.generateTab, text=' Generate   ')

        self.dataDisplay = LabelFrame(self.dataTab, text=' Winners', style="O.TLabelframe")
        self.dataCheck = LabelFrame(self.dataTab, text=' Combination Check', style="O.TLabelframe")

        self.dscroller = Scrollbar(self.dataDisplay, orient=VERTICAL)
        self.dataSelect = Listbox(self.dataDisplay, yscrollcommand=self.dscroller.set, width=95, height=17)
        self.reloadAll = Button(self.dataDisplay, text="Reload All", style="F.TButton", command = lambda : self.loadData())
        self.retrieveData = Button(self.dataDisplay, text="Retrieve Data", style="F.TButton")

        self.numA = Entry(self.dataCheck, textvariable=self.numberA, width="5")
        self.numB = Entry(self.dataCheck, textvariable=self.numberB, width="5")
        self.numC = Entry(self.dataCheck, textvariable=self.numberC, width="5")
        self.numD = Entry(self.dataCheck, textvariable=self.numberD, width="5")
        self.numE = Entry(self.dataCheck, textvariable=self.numberE, width="5")
        self.superLabel  = Label(self.dataCheck, text="Super", style="T.TLabel" )
        self.super = Entry(self.dataCheck, textvariable=self.numberS, width="5")
        self.clearSelect = Button(self.dataCheck, text="Clear", style="F.TButton", command = lambda : self.clearFilter())
        self.checkSelect = Button(self.dataCheck, text="Check", style="F.TButton", command = lambda : self.loadFilteredData())

        self.selectReturn = Button(self.main_container, text="EXIT", style="E.TButton",command=self.exitRoutine)
        self.progressBar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", length=280)

        # position widgets
        self.headerA.grid(row=0, column=0, padx=5, pady=1, sticky='NSEW')
        self.headerB.grid(row=1, column=0, padx=5, pady=1, sticky='NSEW')
        self.parentTab.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')

        self.dataSelect.grid(row=0, column=0, padx=(10,0), pady=5, sticky='NSEW')
        self.dscroller.grid(row=0, column=1, padx=(10,0), pady=5, sticky='NSEW')
        self.reloadAll.grid(row=1, column=0, columnspan=5, padx=(10,5), pady=5, sticky='NSEW')
        self.retrieveData.grid(row=2, column=0, columnspan=5, padx=(10,5), pady=5, sticky='NSEW')
        self.dataDisplay.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.numA.grid(row=0, column=0, padx=(10,0), pady=(5, 10), sticky='W')
        self.numB.grid(row=0, column=0, padx=(60,0), pady=(5, 10), sticky='W')
        self.numC.grid(row=0, column=0, padx=(110,0), pady=(5, 10), sticky='W')
        self.numD.grid(row=0, column=0, padx=(160,0), pady=(5, 10), sticky='W')
        self.numE.grid(row=0, column=0, padx=(210,0), pady=(5, 10), sticky='W')
        self.superLabel.grid(row=0, column=0, padx=(260,0), pady=(5, 10), sticky='W')
        self.super.grid(row=0, column=0, padx=(310,0), pady=(5, 10), sticky='W')

        self.checkSelect.grid(row=0, column=0, padx=(410,0), pady=(5,10), sticky='W')
        self.clearSelect.grid(row=0, column=0, padx=(510,0), pady=(5,10), sticky='W')
        self.dataCheck.grid(row=8, column=0, columnspan=5, padx=5, pady=2, sticky="NSEW")

        self.selectReturn.grid(row=10, column=0, columnspan=5, padx=5, pady=(0,5), sticky='NSEW')
        self.progressBar.grid(row=11, column=0, columnspan=5, padx=5, pady=(0,5), sticky='NSEW')

        '''
        define widgets for stats tab
        '''
        self.statDisplay = LabelFrame(self.statTab, text=' Count ', style="O.TLabelframe")
        self.trendDisplay = LabelFrame(self.statTab, text=' Top Numbers Trend ', style="O.TLabelframe")
        self.nscroller = Scrollbar(self.statDisplay, orient=VERTICAL)
        self.sortStat = Button(self.statDisplay, text="Sort", style="F.TButton", command=self.statNumberOrder)
        self.statNumbers = Listbox(self.statDisplay, yscrollcommand=self.nscroller.set, width=20, height=12)
        self.sscroller = Scrollbar(self.statDisplay, orient=VERTICAL)
        self.sortSuperStat = Button(self.statDisplay, text="Sort", style="F.TButton", command=self.statSuperOrder)
        self.statSupers = Listbox(self.statDisplay, yscrollcommand=self.sscroller.set, width=20, height=8)

        self.trendPlot = Label(self.trendDisplay)
        self.reloadTrend = Button(self.trendDisplay, text="Reload", style="F.TButton", command=self.reload)

        self.statNumbers.grid(row=0, column=0, padx=(10,0), pady=5, sticky='NSEW')
        self.nscroller.grid(row=0, column=1, padx=(5,0), pady=5, sticky='NSEW')
        self.sortStat.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.statSupers.grid(row=2, column=0, padx=(10,0), pady=5, sticky='NSEW')
        self.sscroller.grid(row=2, column=1, padx=(5,0), pady=5, sticky='NSEW')
        self.sortSuperStat.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.statDisplay.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.trendPlot.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.reloadTrend.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.trendDisplay.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

        '''
        define widgets for generator tab
        '''
        self.genOpt = LabelFrame(self.generateTab, text='Generate Options', style="O.TLabelframe")
        # self.topNumsOnly = Checkbutton(self.genOpt, text="Top numbers only", style="B.TCheckbutton", variable=self.topNumbers)
        self.offsetLabel = Label(self.genOpt, text="Top number count : ", style="T.TLabel")
        self.topOffset = Entry(self.genOpt, textvariable=self.offset, width="8")
        self.topCountList = OptionMenu(self.genOpt, self.varCountLimit, *self.limitList)
        self.topCountList.config(width=12)
        self.avoidClose = Checkbutton(self.genOpt, text="No close winners", style="B.TCheckbutton", variable=self.noClose)
        self.skipLastWin = Checkbutton(self.genOpt, text="Skip last winner", style="B.TCheckbutton", variable=self.skipWinner)
        self.noConsec = Checkbutton(self.genOpt, text="No consecutives", style="B.TCheckbutton", variable=self.noCon)
        self.commonPattern = Checkbutton(self.genOpt, text="Common patterns", style="B.TCheckbutton", variable=self.pattern)

        self.h_sep_ga = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.generateTab, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.generateTab, 2))

        self.genSet = Button(self.generateTab, text="GENERATE", style="F.TButton", command=self.generate)
        self.genSave = Button(self.generateTab, text="SAVE", style="F.TButton", command=self.save_generated)
        self.genClear = Button(self.generateTab, text="CLEAR", style="F.TButton", command=self.clear_generated)

        self.offsetLabel.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        self.topCountList.grid(row=0, column=0, padx=(170,0), pady=5, sticky="W")
        self.avoidClose.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.noConsec.grid(row=1, column=0, padx=(170,0), pady=5, sticky="W")
        self.skipLastWin.grid(row=1, column=0, padx=(320,0), pady=5, sticky='W')
        self.commonPattern.grid(row=1, column=0, padx=(460,0), pady=5, sticky="NSEW")

        self.genOpt.grid(row=3, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=20, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=21, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genSave.grid(row=21, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genClear.grid(row=21, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.dataconn = db.databaseConn()

        self.sortOrder.set(0)

        # self.topNumbers.set(0)
        self.noClose.set(0)
        self.skipWinner.set(0)
        self.noCon.set(0)
        self.pattern.set(0)

        self.varCountLimit.set('5')

        self.loadData()
        self.loadStats()
        self.loadSuperStats()
        self.loadTrend()

    def loadData(self):

        winners = self.dataconn.get_super_data('super_lotto')

        self.dataSelect.delete(0, END)

        for winner in winners:

            formatted = self.formatDataLine(winner)

            self.dataSelect.insert(END, formatted)

        self.dscroller.config(command=self.dataSelect.yview)

    def clearFilter(self):

        self.numberA.set('')
        self.numberB.set('')
        self.numberC.set('')
        self.numberD.set('')
        self.numberE.set('')

    def loadFilteredData(self):

        selected = []

        if self.numberA.get():
            selected.append(int(self.numberA.get()))

        if self.numberB.get():
            selected.append(int(self.numberB.get()))

        if self.numberC.get():
            selected.append(int(self.numberC.get()))

        if self.numberD.get():
            selected.append(int(self.numberD.get()))

        if self.numberE.get():
            selected.append(int(self.numberE.get()))

        if self.numberS.get():
            selected.append(int(self.numberS.get()))

        if len(selected) < 6:
            messagebox.showerror('Incomplete filter', 'Please enter five numbers to filter.')
            return

        winners = self.dataconn.get_super_filtered('super_lotto', selected)

        self.dataSelect.delete(0, END)

        if len(winners) > 0:
            for winner in winners:

                formatted = self.formatDataLine(winner)

                self.dataSelect.insert(END, formatted)

        else:
            self.dataSelect.insert(END, 'No data found')

        self.dscroller.config(command=self.dataSelect.yview)

    def formatDataLine(self, winner):

        winner_data = list(winner)

        winner_data[1:] = ['{:02d}'.format(int(num)) for num in winner_data[1:]]

        return "     -     ".join(winner_data)

    def loadStats(self):

        stats = self.dataconn.get_number_stats('super_lotto', self.sortOrder.get())

        self.statNumbers.delete(0, END)

        for idx, stat in enumerate(stats):

            if idx == 26:
                self.statNumbers.insert(END, '==========')

            if self.sortOrder.get() == 2:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), stat[1]])
            else:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), '{:04d}'.format(stat[1])])

            self.statNumbers.insert(END, stat_line)

        self.nscroller.config(command=self.statNumbers.yview)

    def loadSuperStats(self):

        stats = self.dataconn.get_extra_stats('super_lotto', self.sortSuperOrder.get())

        self.statSupers.delete(0, END)

        for idx, stat in enumerate(stats):

            if self.sortSuperOrder.get() == 2:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), stat[1]])
            else:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), '{:04d}'.format(stat[1])])

            self.statSupers.insert(END, stat_line)

        self.sscroller.config(command=self.statSupers.yview)

    def loadTrend(self):

        self.progressBar.start()
        if os.path.exists('super.jpg'):
            pass
        else:
            self.loadTrendFromData()

        image = Image.open("super.jpg")
        image = image.resize((440,360))
        results_fig = ImageTk.PhotoImage(image)

        # Define a style
        root.results_fig = results_fig
        Style().configure("DT.TLabel", image=results_fig, background="white", anchor="left", font="Verdana 2")

        self.trendPlot['style'] = 'DT.TLabel'
        
        self.progressBar.stop()

    def check_top_n(self, data, top):

        dd, na, nb, nc, nd, ne = data

        num_set = [na, nb, nc, nd, ne]

        # get the top numbers prior to the draw date passed
        top_numbers = self.dataconn.get_top_stats_by_date(dd, top, 'super_lotto')

        return len([num for num in num_set if num in top_numbers])

    def loadTrendFromData(self):

        self.progressBar.start()

        winners = self.dataconn.get_super_data('super_lotto')

        cols = ['Draw Date', 'A', 'B', 'C', 'D', 'E', 'M']
        df = pd.DataFrame.from_records(winners, columns=cols)

        df['TOP'] = df[['Draw Date', 'A', 'B', 'C', 'D', 'E']].apply(self.check_top_n, args=(25, ), axis=1)

        plt.figure(figsize=(5,3))
        plt.plot(df['TOP'][:50])
        plt.savefig('super.jpg')

        self.progressBar.stop()

    def reload(self):

        try:
            os.remove('super.jpg')
        except:
            pass

        t = threading.Thread(None, self.loadTrend, ())
        t.start()
        

    def statNumberOrder(self):

        if self.sortOrder.get() == 0:
            self.sortOrder.set(1)
        elif self.sortOrder.get() == 1:
            self.sortOrder.set(2)
        else:
            self.sortOrder.set(0)

        self.loadStats()

    def statSuperOrder(self):

        if self.sortSuperOrder.get() == 0:
            self.sortSuperOrder.set(1)
        elif self.sortSuperOrder.get() == 1:
            self.sortSuperOrder.set(2)
        else:
            self.sortSuperOrder.set(0)

        self.loadSuperStats()

    def generate(self):

        if self.generated:
            self.get_a_set() 
        else: 

            if self.genSet['text'] == 'GENERATE':
                resp = messagebox.askyesno('Generating combinations', 'Generation will take some time. Continue?')
            else:
                resp = messagebox.askyesno('Generated List End', 'All generated numbers shown. Generate again?')

            if resp:

                t = threading.Thread(None, self.generateThread, ())
                t.start()

            else:
                self.genSet['text'] = 'GENERATE'

    def generateThread(self):

        self.progressBar.start()
        t_count = int(self.varCountLimit.get())
        l_count = 5 - t_count

        all_numbers = [n[0] for n in self.dataconn.get_number_stats('super_lotto', 0)]

        # print(list(self.dataconn.get_latest_winner('super_lotto')[0])[1:])

        if self.skipWinner.get() == 1:
            all_numbers = [n for n in all_numbers if n not in list(self.dataconn.get_latest_winner('super_lotto')[0])[1:]]

        # top_numbers = all_numbers[:25]
        # low_numbers = all_numbers[25:]

        # random.shuffle(top_numbers)
        # random.shuffle(low_numbers)

        # use_numbers = top_numbers[:t_count] + low_numbers[:l_count]

        self.generate_sets(all_numbers, t_count, l_count)
        self.progressBar.stop()

    def generate_sets(self, numbers, t_count, l_count):

        start = datetime.now()
        print(start)

        top_combos = list(self.set_iterator(numbers[:25], t_count))
        bot_combos = list(self.set_iterator(numbers[25:], l_count))

        all_combos = []

        for tc in top_combos:
            for bc in bot_combos:
                tcl = list(tc)
                bcl = list(bc)
                tcl.extend(bcl)
                all_combos.append(sorted(tcl))

        print(len(all_combos))

        # iterator = self.set_iterator(numbers)
        # combis = list(iterator)

        combi_sets = []
        combi_set = []
    
        count = 0

        while True:

            random.shuffle(all_combos)

            for idx, combi in enumerate(all_combos):

                comb = list(sorted(combi))

                if self.check_numbers(combi_set, comb):
                    comb.append(self.get_a_super())
                    combi_set.append(comb)

                if len(combi_set) == 5:
                    combi_sets.append(combi_set)
                    combi_set = []

            combi_set = []
            count += 1

            if count > 500:
                break
            
            if len(combi_sets) >= 400:
                break

        end = datetime.now()
        print(end)
        print("Time elapsed: ", end - start)
        print(len(combi_sets), count)

        self.generated = combi_sets
        self.genSet['text'] = 'NEXT'
        self.get_a_set()

        # return combi_sets

    def set_iterator(self, nums, count):

        random.shuffle(nums)

        return combinations(nums, count)

    def get_a_set(self):

        generated = self.generated.pop(0)
        self.dataconn.store_super_plays(generated)
        
        for i in range(5):
            win = self.dataconn.check_super_winner(generated[i])
            self.dGen[i].changeTopStyle(generated[i], win)

    def get_a_super(self):

        sups = [n+1 for n in range(27)]
        
        random.shuffle(sups)

        return sups.pop()

    def check_numbers(self, generated, num_set):

        # check if any of the numbers were selected before
        for gen in generated:
            check = [n for n in num_set if n not in gen[:5]]

            if len(check) < 5:
                return False

        # check that consecutives do not exceed 1
        con_count = 0
        for i in range(len(num_set) - 1):
            if num_set[i] == num_set[i+1] - 1:
                con_count += 1

        if self.noCon.get() == 1:
            if con_count > 0:
                return False
        else:
            if con_count > 1:
                return False

        if self.noClose.get():
            if self.dataconn.check_close_super_winner(num_set):
                pass
            else:
                return False

        if self.pattern.get() == 1:
            if self.check_pattern(num_set):
                pass
            else:
                return False

        return True

    def check_pattern(self, num_set):

        odd_count = len([num for num in num_set if num % 2 == 1])

        if odd_count not in [0, 5]:
            return True
        else:
            return False

    def clear_generated(self):

        resp = messagebox.askyesno('Reset','This will reset generated numbers. Continue?')

        if resp:
            self.generated = []
            self.genSet['text'] = 'GENERATE'

            for i in range(5):
                self.dGen[i].clearTopStyle()


    def save_generated(self):

        self.dataconn.save_super_plays()

    def getCountLimits(self):

        menu = self.topCountList['menu']
        menu.delete(0, 'end')

        for lim in [25, 20, 15]:
            menu.add_command(label=lim, command=lambda value=lim: self.varCountLimit.set(value))

    def exitRoutine(self):

        ''' This function will be executed when the user exits
        '''

        self.dataconn.delete_super_plays()
        root.destroy()

root = Tk()
root.title("SUPER LOTTO")

# Set size
wh = 590
ww = 650

#root.resizable(height=False, width=False)

root.minsize(ww, wh)
root.maxsize(ww, wh)

# Position in center screen

ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (ww/2)
y = (hs/2) - (wh/2)

root.geometry('%dx%d+%d+%d' % (ww, wh, x, y))

app = Application(root)

root.mainloop()
