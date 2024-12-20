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
import matplotlib 
matplotlib.use('agg')


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
        self.sortPowerOrder = IntVar()

        self.topCount = IntVar()
        self.noClose = IntVar()
        self.noCon = IntVar()
        self.oddPatterns = IntVar()
        self.evenPatterns = IntVar()
        self.baseOption = IntVar()
        self.classOpt = IntVar()
        self.plotTopNumbers = IntVar()
        self.plotBotNumbers = IntVar()
        self.plotIdxClass = IntVar()
        self.plotPatClass = IntVar()

        self.generated = []

        self.varTopCount = StringVar()
        self.varBotCount = StringVar()
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
        Style().configure("C.TButton", font=rfont, relief="raised", width=20)

        # Set scale styles
        Style().configure("S.TScale", orient=HORIZONTAL, width=25)

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))
        self.headerA  = Label(self.main_container, text="Powerball Lotto", style="M.TLabel" )
        self.headerB = Label(self.main_container, text="Play and enjoy the Powerball game from CA Lottery", style="T.TLabel" )

        self.parentTab = Notebook(self.main_container)
        self.dataTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.statTab = Frame(self.parentTab)   # second page
        self.generateTab = Frame(self.parentTab)   # third page
        self.playsTab = Frame(self.parentTab)   # fourth page
        self.parentTab.add(self.dataTab, text='   Data     ')
        self.parentTab.add(self.statTab, text='   Stats     ')
        self.parentTab.add(self.generateTab, text=' Generate   ')

        self.dataDisplay = LabelFrame(self.dataTab, text=' Winners', style="O.TLabelframe")
        self.dataCheck = LabelFrame(self.dataTab, text=' Combination Check', style="O.TLabelframe")
        self.playsDisplay = LabelFrame(self.dataTab, text='Plays', style="O.TLabelframe")

        self.dscroller = Scrollbar(self.dataDisplay, orient=VERTICAL)
        self.dataSelect = Listbox(self.dataDisplay, yscrollcommand=self.dscroller.set, width=95, height=20)
        self.enterData = Button(self.dataDisplay, text="Enter Data", style="F.TButton", command = lambda : self.callEntry())
        self.filterData = Button(self.dataDisplay, text="Filter Data", style="F.TButton", command = lambda : self.loadFilteredData())
        self.reloadAll = Button(self.dataDisplay, text="Reload All", style="F.TButton", command = lambda : self.loadData())

        self.playsscroller = Scrollbar(self.playsDisplay, orient=VERTICAL)
        self.playsSelect = Listbox(self.playsDisplay, yscrollcommand=self.playsscroller.set, width=65, height=24)
        self.playReload = Button(self.playsDisplay, text="RELOAD", style="F.TButton", command=self.loadBets)

        self.numA = Entry(self.dataCheck, textvariable=self.numberA, width="5")
        self.numB = Entry(self.dataCheck, textvariable=self.numberB, width="5")
        self.numC = Entry(self.dataCheck, textvariable=self.numberC, width="5")
        self.numD = Entry(self.dataCheck, textvariable=self.numberD, width="5")
        self.numE = Entry(self.dataCheck, textvariable=self.numberE, width="5")
        self.powerLabel  = Label(self.dataCheck, text="Power", style="T.TLabel" )
        self.power = Entry(self.dataCheck, textvariable=self.numberS, width="5")
        self.clearSelect = Button(self.dataCheck, text="Clear", style="C.TButton", command = lambda : self.clearFilter())

        self.selectReturn = Button(self.main_container, text="EXIT", style="E.TButton",command=self.exitRoutine)
        self.progressBar = Progressbar(self.main_container, orient="horizontal", mode="indeterminate", length=280)

        # position widgets
        self.headerA.grid(row=0, column=0, padx=5, pady=1, sticky='NSEW')
        self.headerB.grid(row=1, column=0, padx=5, pady=1, sticky='NSEW')
        self.parentTab.grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')

        self.dataSelect.grid(row=0, column=0, columnspan=3, padx=(10,0), pady=5, sticky='NSEW')
        self.dscroller.grid(row=0, column=3, columnspan=1, padx=(10,0), pady=5, sticky='NSEW')
        self.enterData.grid(row=1, column=0, columnspan=1, padx=(10,5), pady=5, sticky='NSEW')
        self.filterData.grid(row=1, column=1, columnspan=1, padx=(10,5), pady=5, sticky='NSEW')
        self.reloadAll.grid(row=1, column=2, columnspan=1, padx=(10,5), pady=5, sticky='NSEW')
        self.dataDisplay.grid(row=7, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.numA.grid(row=0, column=0, padx=(10,0), pady=(5, 5), sticky='W')
        self.numB.grid(row=0, column=0, padx=(70,0), pady=(5, 5), sticky='W')
        self.numC.grid(row=0, column=0, padx=(130,0), pady=(5, 5), sticky='W')
        self.numD.grid(row=0, column=0, padx=(190,0), pady=(5, 5), sticky='W')
        self.numE.grid(row=0, column=0, padx=(250,0), pady=(5, 5), sticky='W')
        self.powerLabel.grid(row=0, column=0, padx=(310,0), pady=(5, 10), sticky='W')
        self.power.grid(row=0, column=0, padx=(370,0), pady=(5, 10), sticky='W')

        self.playsSelect.grid(row=0, column=0, columnspan=3, padx=(10,0), pady=5, sticky='NSEW')
        self.playsscroller.grid(row=0, column=3, columnspan=1, padx=(10,0), pady=5, sticky='NSEW')
        self.playReload.grid(row=1, column=0, columnspan=3, padx=(10,0), pady=(3,5), sticky='NSEW')
        self.playsDisplay.grid(row=7, column=3, columnspan=2, rowspan=2, padx=5, pady=2, sticky='NSEW')

        self.clearSelect.grid(row=0, column=0, padx=(430,0), pady=(5,10), sticky='W')
        self.dataCheck.grid(row=8, column=0, columnspan=3, padx=5, pady=2, sticky="NSEW")

        self.selectReturn.grid(row=10, column=0, columnspan=5, padx=5, pady=(0,5), sticky='NSEW')
        self.progressBar.grid(row=11, column=0, columnspan=5, padx=5, pady=(0,5), sticky='NSEW')

        '''
        define widgets for stats tab
        '''
        self.statDisplay = LabelFrame(self.statTab, text=' Count ', style="O.TLabelframe")
        self.trendDisplay = LabelFrame(self.statTab, text=' Top Numbers Trend ', style="O.TLabelframe")
        self.nscroller = Scrollbar(self.statDisplay, orient=VERTICAL)
        self.sortStat = Button(self.statDisplay, text="Sort", style="F.TButton", command=self.statNumberOrder)
        self.statNumbers = Listbox(self.statDisplay, yscrollcommand=self.nscroller.set, width=22, height=23)
        self.sscroller = Scrollbar(self.statDisplay, orient=VERTICAL)
        self.sortPowerStat = Button(self.statDisplay, text="Sort", style="F.TButton", command=self.statPowerOrder)
        self.statPowers = Listbox(self.statDisplay, yscrollcommand=self.sscroller.set, width=22, height=23)

        self.trendPlot = Label(self.trendDisplay)
        self.reloadTrend = Button(self.trendDisplay, text="Reload", style="F.TButton", command=self.reload)
        self.plotTop = Checkbutton(self.trendDisplay, text="Top Numbers", style="B.TCheckbutton", variable=self.plotTopNumbers)
        self.plotBot = Checkbutton(self.trendDisplay, text="Bot Numbers", style="B.TCheckbutton", variable=self.plotBotNumbers)
        self.plotIdx = Checkbutton(self.trendDisplay, text="Index Class", style="B.TCheckbutton", variable=self.plotIdxClass)
        self.plotPat = Checkbutton(self.trendDisplay, text="Pat Class", style="B.TCheckbutton", variable=self.plotPatClass)

        self.statNumbers.grid(row=0, column=0, padx=(10,0), pady=5, sticky='NSEW')
        self.nscroller.grid(row=0, column=1, padx=(5,0), pady=5, sticky='NSEW')
        self.statPowers.grid(row=0, column=2, padx=(10,0), pady=5, sticky='NSEW')
        self.sscroller.grid(row=0, column=3, padx=(5,0), pady=5, sticky='NSEW')

        self.sortStat.grid(row=1, column=0, columnspan=2, padx=5, pady=(12, 5), sticky='NSEW')
        self.sortPowerStat.grid(row=1, column=2, columnspan=2, padx=5, pady=(12, 5), sticky='NSEW')
        self.statDisplay.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')

        self.plotTop.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        self.plotBot.grid(row=0, column=0, padx=(160,5), pady=5, sticky='NSEW')
        self.plotIdx.grid(row=0, column=0, padx=(320,5), pady=5, sticky='NSEW')
        self.plotPat.grid(row=0, column=0, padx=(480,5), pady=5, sticky='NSEW')
        self.trendPlot.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.reloadTrend.grid(row=2, column=0, columnspan=5, padx=5, pady=(8,5), sticky='NSEW')
        self.trendDisplay.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

        '''
        define widgets for generator tab
        '''

        self.mainOptions = LabelFrame(self.generateTab, text=' Options ', style="O.TLabelframe")
        self.topsOption = Radiobutton(self.mainOptions, text="Top 25", style="B.TRadiobutton", variable=self.baseOption, value=0)
        self.topCountList = OptionMenu(self.mainOptions, self.varTopCount, *self.limitList)
        self.topCountList.config(width=5)
        self.botOption = Radiobutton(self.mainOptions, text="Bot 25", style="B.TRadiobutton", variable=self.baseOption, value=1)
        self.botCountList = OptionMenu(self.mainOptions, self.varBotCount, *self.limitList)
        self.botCountList.config(width=5)

        self.filterOptions = LabelFrame(self.generateTab, text='Filters', style="O.TLabelframe")
        self.avoidClose = Checkbutton(self.filterOptions, text="No past winners", style="B.TCheckbutton", variable=self.noClose)
        self.noConsec = Checkbutton(self.filterOptions, text="No consecutives", style="B.TCheckbutton", variable=self.noCon)
        self.classOption = Checkbutton(self.filterOptions, text="Use odd idx class", style="B.TCheckbutton", variable=self.classOpt)

        self.patternOptions = LabelFrame(self.generateTab, text='Patterns', style="O.TLabelframe")
        self.leaningOdd = Checkbutton(self.patternOptions, text="Lean odd ", style="B.TCheckbutton", variable=self.oddPatterns, command=self.checkLeaningEven)
        self.leaningEven = Checkbutton(self.patternOptions, text="Lean even ", style="B.TCheckbutton", variable=self.evenPatterns, command=self.checkLeaningOdd)

        self.h_sep_ga = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.generateTab, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.generateTab, 4))

        self.genSet = Button(self.generateTab, text="GENERATE", style="F.TButton", command=self.generate)
        self.genSave = Button(self.generateTab, text="SAVE", style="F.TButton", command=self.save_generated)
        self.genClear = Button(self.generateTab, text="CLEAR", style="F.TButton", command=self.clear_generated)

        self.topsOption.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.topCountList.grid(row=0, column=0, padx=(90,5), pady=5, sticky="W")
        self.botOption.grid(row=0, column=0, padx=(180,5), pady=5, sticky="W")
        self.botCountList.grid(row=0, column=0, padx=(270,5), pady=5, sticky="W")
        self.mainOptions.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.noConsec.grid(row=0, column=0, padx=5, pady=5, sticky="W")
        self.avoidClose.grid(row=1, column=0, padx=5, pady=5, sticky="W")
        self.classOption.grid(row=2, column=0, padx=5, pady=5, sticky="W")
        self.filterOptions.grid(row=0, column=2, columnspan=2, rowspan=2, padx=5, pady=2, sticky='NSEW')

        self.leaningOdd.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        self.leaningEven.grid(row=0, column=1, padx=(90,5), pady=5, sticky="NSEW")
        self.patternOptions.grid(row=1, column=0, columnspan=2, padx=5, pady=2, sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=22, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=23, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genSave.grid(row=23, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genClear.grid(row=23, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        ''' add widgets for bets tab
        '''

        self.dataconn = db.databaseConn()

        self.sortOrder.set(0)

        self.noClose.set(0)
        self.noCon.set(0)
        self.baseOption.set(0)
        self.varTopCount.set('5')
        self.varBotCount.set('5')

        self.loadData()
        self.loadStats()
        self.loadPowerStats()
        self.loadTrend()
        self.loadBets()

    def callEntry(self):

       os.system('python C:/Users/Alan/Scripts/Code/data_entry/data_entry.py')

    def loadData(self):

        winners = self.dataconn.get_mps_data('power_ball')

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

        winners = self.dataconn.get_mps_filtered('power_ball', selected)

        self.dataSelect.delete(0, END)

        if len(winners) > 0:
            for winner in winners:

                formatted = self.formatDataLine(winner)

                self.dataSelect.insert(END, formatted)

        else:
            self.dataSelect.insert(END, 'No data found')

        self.dscroller.config(command=self.dataSelect.yview)

    def loadBets(self):

        winners = self.dataconn.get_plays('power_ball_bets', True)

        self.playsSelect.delete(0, END)

        for winner in winners:

            formatted = self.formatBetsLine(winner)

            self.playsSelect.insert(END, formatted)

        self.playsscroller.config(command=self.playsSelect.yview)

    def formatBetsLine(self, winner):

        winner_data = list(winner)

        play_date = winner_data[0]
        numbers = winner_data[1:]

        winner_data[1:] = ['{:02d}'.format(int(num)) for num in winner_data[1:]]

        if self.dataconn.check_mps_winner('power_ball', numbers[:5], play_date):
            winner_data.append('W')

        return "     -     ".join(winner_data)
    
    def formatDataLine(self, winner):

        winner_data = list(winner)

        winner_data[1:] = ['{:02d}'.format(int(num)) for num in winner_data[1:]]

        return "     -     ".join(winner_data)

    def loadStats(self):

        stats = self.dataconn.get_number_stats('power_ball', self.sortOrder.get())

        self.statNumbers.delete(0, END)

        for idx, stat in enumerate(stats):

            if idx == 25:
                self.statNumbers.insert(END, '==========')

            if self.sortOrder.get() == 2:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), stat[1]])
            else:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), '{:04d}'.format(stat[1])])

            self.statNumbers.insert(END, stat_line)

        self.nscroller.config(command=self.statNumbers.yview)

    def loadPowerStats(self):

        stats = self.dataconn.get_extra_stats('power_ball', self.sortPowerOrder.get())

        self.statPowers.delete(0, END)

        for idx, stat in enumerate(stats):

            if self.sortPowerOrder.get() == 2:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), stat[1]])
            else:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), '{:04d}'.format(stat[1])])

            self.statPowers.insert(END, stat_line)

        self.sscroller.config(command=self.statPowers.yview)

    def loadTrend(self):

        if os.path.exists('power.jpg'):
            self.loadImage()
        else:
            t = threading.Thread(None, self.loadTrendFromData, ())
            t.start()

    def loadTrendFromData(self):

        self.progressBar.start()

        if self.plotTopNumbers.get() == 0 and self.plotBotNumbers.get() == 0 and self.plotIdxClass.get() == 0 and self.plotPatClass.get() == 0:
            self.plotTopNumbers.set(1)

        winners = self.dataconn.get_mps_data('power_ball')

        cols = ['Draw Date', 'A', 'B', 'C', 'D', 'E', 'M']
        df = pd.DataFrame.from_records(winners, columns=cols)

        plt.figure(figsize=(5,3))

        if self.plotTopNumbers.get() == 1:
            df['TOPS'] = df[['Draw Date', 'A', 'B', 'C', 'D', 'E']].apply(self.check_top_n, axis=1)
            plt.plot(df['TOPS'][:50], 'o--', label='T25', color='blue')

        if self.plotBotNumbers.get() == 1:
            df['BOTS'] = df[['Draw Date', 'A', 'B', 'C', 'D', 'E']].apply(self.check_bot_n, axis=1)
            plt.plot(df['BOTS'][:50], 'o-', label='B25', color='red')

        if self.plotIdxClass.get() == 1:
            df['IDX'] = df[['A', 'B', 'C', 'D', 'E']].apply(self.check_index_class, axis=1)
            plt.plot(df['IDX'][:50], 'o--', label='IDX', color='yellow', alpha=0.5)

        if self.plotPatClass.get() == 1:
            df['PAT'] = df[['A', 'B', 'C', 'D', 'E']].apply(self.check_pattern_class, axis=1)
            plt.plot(df['PAT'][:50], 'o--', label='PAT', color='green', alpha=0.5)

        plt.grid(axis='both', color='grey', alpha=0.5)
        plt.legend(title='Label', loc='upper right')
        ax = plt.gca()
        ax.set_yticks([5,4,3,2,1,0])
        plt.savefig('power.jpg')

        self.progressBar.stop()

        self.loadImage()
        messagebox.showinfo('Reloaded', 'Trend graph has been reloaded.')

        return
    
    def reload(self):

        try:
            os.remove('power.jpg')
        except:
            pass

        self.loadTrend()
        
    def loadImage(self):

        image = Image.open("power.jpg")
        image = image.resize((700,345))
        results_fig = ImageTk.PhotoImage(image)

        # Define a style
        root.results_fig = results_fig
        Style().configure("DT.TLabel", image=results_fig, background="white", anchor="left", font="Verdana 2")

        self.trendPlot['style'] = 'DT.TLabel'

    def check_top_n(self, data):

        dd, na, nb, nc, nd, ne = data

        num_set = [na, nb, nc, nd, ne]

        # get the top numbers prior to the draw date passed
        top_numbers = self.dataconn.get_top_stats_by_date(dd, 'power_ball')[:25]

        return len([num for num in num_set if num in top_numbers])

    def check_bot_n(self, data):

        dd, na, nb, nc, nd, ne = data

        num_set = [na, nb, nc, nd, ne]

        # get the bot numbers prior to the draw date passed
        bot_numbers = self.dataconn.get_top_stats_by_date(dd, 'power_ball')[-25:]

        return len([num for num in num_set if num in bot_numbers])

    def statNumberOrder(self):

        if self.sortOrder.get() == 0:
            self.sortOrder.set(1)
        elif self.sortOrder.get() == 1:
            self.sortOrder.set(2)
        else:
            self.sortOrder.set(0)

        self.loadStats()

    def statPowerOrder(self):

        if self.sortPowerOrder.get() == 0:
            self.sortPowerOrder.set(1)
        elif self.sortPowerOrder.get() == 1:
            self.sortPowerOrder.set(2)
        else:
            self.sortPowerOrder.set(0)

        self.loadPowerStats()

    def checkLeaningOdd(self):

        if self.oddPatterns.get() == 1:
            self.evenPatterns.set(0)

    def checkLeaningEven(self):

        if self.evenPatterns.get() == 1:
            self.oddPatterns.set(0)

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

        all_numbers = [n[0] for n in self.dataconn.get_number_stats('power_ball', 0)]
        top_numbers = all_numbers[:25]

        self.generate_sets(all_numbers, top_numbers)

        self.progressBar.stop()

    def generate_sets(self, all_numbers, top_numbers):

        start = datetime.now()
        print(start)

        self.count_limit = 10000

        selected = self.retrieve_qualified_combos()

        ''' The logic below will select combinations and remove them from succeeding iterations
            This will ensure that combinations will not be selected again
        '''
        
        random.shuffle(selected)
        print(f'For grouping             : {len(selected)}')
        combos_all = self.set_iterator(selected)
        count = 0

        inter_count = 0
        max_count = 0

        combo_sets = []

        while True:

            try:
                combo = next(combos_all)
                added = False
                
                if combo_sets:
                    for combo_set in combo_sets:
                        if len(combo_set) > max_count:
                            max_count = len(combo_set)
                        if len(combo_set) < 25:
                            if len(set(combo_set).intersection(set(combo))) <= inter_count:
                                combo_set.extend(combo)
                                added = True
                                break
                            
                    if not added:
                        combo_sets.append(combo)
                        
                else:
                    combo_sets.append(combo)
                    
                count += 1
                
                if count == self.count_limit:
                    break
            except:
                break
        
        print(max_count)
        end = datetime.now()
        print(end)
        print("Time elapsed: ", end - start)

        self.generated = [self.format_sets(n_set) for n_set in combo_sets if len(n_set) == 25]

        print(f'Combo sets    : {len(combo_sets)}')
        print(f'Complete sets : {len(self.generated)}')

        self.genSet['text'] = 'NEXT'
        self.get_a_set()

    def generate_and_filter(self, all_numbers, top_numbers):

        combos_all = self.set_generator(all_numbers, 5)
        selected = []

        while True:

            try:
                combo = next(combos_all)
                selected.append(sorted(list(combo)))
            except Exception as e:
                break

        print(f'All combinations         : {len(selected)}')

        combos_all = self.set_iterator(selected)
        selected = []

        while True:

            try:
                combo = next(combos_all)
                if len(set(top_numbers).intersection(set(combo))) == int(self.varCountLimit.get()):
                    selected.append(list(combo))
            except:
                break

        print(f'After top numbers filter : {len(selected)}')

        if self.noCon.get():
            combos_all = self.set_iterator(selected)
            selected = []

            while True:

                try:
                    combo = next(combos_all)
                    if self.check_consecutives(combo):
                        selected.append(combo)
                except:
                    break

        print(f'After consecutive filter : {len(selected)}')

        if self.leanPattern.get() == 0:

            combos_all = self.set_iterator(selected)
            selected = []

            while True:

                try:
                    combo = next(combos_all)
                    if self.check_pattern(combo):
                        selected.append(combo)
                except:
                    break

        print(f'After pattern filter     : {len(selected)}')

        if self.noClose.get():

            combos_all = self.set_iterator(selected)
            selected = []

            while True:

                try:
                    combo = next(combos_all)
                    if self.dataconn.check_mps_winner('power_ball', combo): # if winner, bypass 
                        pass 
                    else:
                        selected.append(combo)
                except:
                    break

        print(f'After winner filter      : {len(selected)}') 

        return selected 
    
    def retrieve_qualified_combos(self):
        
        select_sql = f'''
        select combo_key
        from power_combos
        where'''

        if self.baseOption.get() == 0:

            tops = int(self.varTopCount.get())
            select_sql += f''' top_count = {tops}'''

        if self.baseOption.get() == 1:

            bots = int(self.varBotCount.get())
            select_sql += f''' bot_count = {bots}'''

        if self.classOpt.get() == 1:
            select_sql += f''' and mod(combo_idx, 2) = 1'''
        else:
            select_sql += f''' and mod(combo_idx, 2) = 0'''

        if self.noClose.get():
            select_sql += ''' and win_count = 0'''

        if self.noCon.get():
            select_sql += ''' and con_count = 0'''
        else:
            select_sql += ''' and con_count < 3'''

        if self.oddPatterns.get() == 1:
            select_sql += ''' and odd_count >= 3''' 
        elif self.evenPatterns.get() == 1:
            select_sql += ''' and odd_count < 3''' 
        else:
            select_sql += ''' and odd_count in (4,3,2,1)''' 

        combo_keys = self.dataconn.execute_select(select_sql)

        selected = [self.split_key(combo_key[0]) for combo_key in combo_keys]

        print(f'Qualified combinations   : {len(selected)}')

        return selected  

    def format_sets(self, number_set):

        c_set = []
        for i in range(0,25,5):
            c_set.append(number_set[i:i+5])
        
        return c_set

    def split_key(self, combo_key):
        
        numbers = []
        for i in range(0,10,2):
            numbers.append(int(combo_key[i:i+2]))
    
        return numbers

    def set_generator(self, nums, count):

        random.shuffle(nums)

        return combinations(nums, count)

    def set_iterator(self, combos):

        return iter(combos)

    def get_a_set(self):

        random.shuffle(self.generated)
        generated = self.generated.pop(0)
        random.shuffle(generated)

        for gen in generated:
            gen.append(self.get_extra())

        self.dataconn.store_mps_plays('power_ball_bets', generated)
        
        for i in range(5):
            win = self.dataconn.check_mps_winner('power_ball', generated[i])
            self.dGen[i].changeTopStyle(generated[i], win)

    def get_extra(self):

        sups = [n+1 for n in range(26)]
        
        random.shuffle(sups)

        return sups.pop()

    def check_index_class(self, num_set):

        combo_key = ''.join(['{:02d}'.format(int(num)) for num in num_set])

        idx_val = self.dataconn.get_combo_index(combo_key, 'power_combos')
        
        return idx_val % 2

    def check_pattern_class(self, num_set):

        count = len([num for num in num_set if num % 2 > 0])

        return 1 if count > 2 else 0

    def check_consecutives(self, num_set):

        count = 0
        prev = 0

        for num in num_set:
            if prev == 0:
                prev = num 
            else: 
                if num - 1 == prev:
                    count += 1

                prev = num 
        
        return True if count == 0 else False

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

        self.dataconn.save_mps_plays('power_ball_bets')
        messagebox.showinfo('Saved', 'Combination set save in database')

    def getCountLimits(self):

        menu = self.topCountList['menu']
        menu.delete(0, 'end')

        for lim in [25, 20, 15]:
            menu.add_command(label=lim, command=lambda value=lim: self.varCountLimit.set(value))

    def exitRoutine(self):

        ''' This function will be executed when the user exits
        '''

        self.dataconn.delete_mps_plays('power_ball_bets')
        root.destroy()

root = Tk()
root.title("POWER BALL")

# Set size
wh = 610
ww = 1100

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
