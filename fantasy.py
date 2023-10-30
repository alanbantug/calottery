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

        self.offset = StringVar()

        self.sortOrder = IntVar()

        self.topNumbers = IntVar()
        self.topCount = IntVar()
        self.noClose = IntVar()
        self.skipWinner = IntVar()
        self.noCon = IntVar()
        self.pattern = IntVar()
        self.baseOption = IntVar()

        self.generated = [] 

        self.varCountLimit = StringVar()
        self.limitList = ['5', '5', '4', '3', '2']
        self.varClassList = StringVar()
        self.classList = ['0', '0', '1']

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
        self.headerA  = Label(self.main_container, text="Fantasy Five", style="M.TLabel" )
        self.headerB = Label(self.main_container, text="Play and enjoy the Fantasy Five game fro CA Lottery", style="T.TLabel" )

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
        self.dataSelect = Listbox(self.dataDisplay, yscrollcommand=self.dscroller.set, width=70, height=11)
        self.reloadAll = Button(self.dataDisplay, text="Reload All", style="F.TButton", command = lambda : self.loadData())
        self.retrieveData = Button(self.dataDisplay, text="Retrieve Data", style="F.TButton")

        self.numA = Entry(self.dataCheck, textvariable=self.numberA, width="5")
        self.numB = Entry(self.dataCheck, textvariable=self.numberB, width="5")
        self.numC = Entry(self.dataCheck, textvariable=self.numberC, width="5")
        self.numD = Entry(self.dataCheck, textvariable=self.numberD, width="5")
        self.numE = Entry(self.dataCheck, textvariable=self.numberE, width="5")
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
        self.checkSelect.grid(row=0, column=0, padx=(260,0), pady=(5,10), sticky='W')
        self.clearSelect.grid(row=0, column=0, padx=(360,0), pady=(5,10), sticky='W')
        self.dataCheck.grid(row=8, column=0, columnspan=5, padx=5, pady=2, sticky="NSEW")

        self.selectReturn.grid(row=10, column=0, columnspan=5, padx=5, pady=(0,5), sticky='NSEW')
        self.progressBar.grid(row=11, column=0, columnspan=5, padx=5, pady=(0,5), sticky='NSEW')

        '''
        define widgets for stats tab
        '''
        self.statDisplay = LabelFrame(self.statTab, text=' Count ', style="O.TLabelframe")
        self.trendDisplay = LabelFrame(self.statTab, text=' Top Numbers Trend ', style="O.TLabelframe")
        self.sscroller = Scrollbar(self.statDisplay, orient=VERTICAL)
        self.sortStat = Button(self.statDisplay, text="Sort", style="F.TButton", command=self.statSortOrder)
        self.statSelect = Listbox(self.statDisplay, yscrollcommand=self.sscroller.set, width=18, height=17)
        self.trendPlot = Label(self.trendDisplay)
        self.reloadTrend = Button(self.trendDisplay, text="Reload", style="F.TButton", command=self.reload)

        self.statSelect.grid(row=0, column=0, padx=(10,0), pady=5, sticky='NSEW')
        self.sscroller.grid(row=0, column=1, padx=(5,0), pady=5, sticky='NSEW')
        self.sortStat.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.statDisplay.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky='NSEW')
        self.trendPlot.grid(row=0, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.reloadTrend.grid(row=1, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')
        self.trendDisplay.grid(row=0, column=1, columnspan=4, padx=5, pady=5, sticky='NSEW')

        '''
        define widgets for generator tab
        '''
        self.mainOptions = LabelFrame(self.generateTab, text='Options', style="O.TLabelframe")
        self.topsOption = Radiobutton(self.mainOptions, text="Top numbers", style="B.TRadiobutton", variable=self.baseOption, value=1)
        self.classOption = Radiobutton(self.mainOptions, text="Class", style="B.TRadiobutton", variable=self.baseOption, value=2)
        self.topCountList = OptionMenu(self.mainOptions, self.varCountLimit, *self.limitList)
        self.topCountList.config(width=5)
        self.classOptList = OptionMenu(self.mainOptions, self.varClassList, *self.classList)
        self.classOptList.config(width=5)

        self.filterOptions = LabelFrame(self.generateTab, text='Filters', style="O.TLabelframe")
        self.topNumsOnly = Checkbutton(self.filterOptions, text="Top numbers only", style="B.TCheckbutton", variable=self.topNumbers)
        self.avoidClose = Checkbutton(self.filterOptions, text="No past winners", style="B.TCheckbutton", variable=self.noClose)
        self.noConsec = Checkbutton(self.filterOptions, text="No Consecutives", style="B.TCheckbutton", variable=self.noCon)
        self.skipLastWin = Checkbutton(self.filterOptions, text="Skip last winner", style="B.TCheckbutton", variable=self.skipWinner)
        self.commonPattern = Checkbutton(self.filterOptions, text="Common patterns", style="B.TCheckbutton", variable=self.pattern)

        self.h_sep_ga = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gb = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gc = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gd = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_ge = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gf = Separator(self.generateTab, orient=HORIZONTAL)
        self.h_sep_gg = Separator(self.generateTab, orient=HORIZONTAL)

        self.dGen = []

        for i in range(5):
            self.dGen.append(dg.displayNumbers(self.generateTab, 1))

        self.genSet = Button(self.generateTab, text="GENERATE", style="F.TButton", command=self.generate)
        self.genSave = Button(self.generateTab, text="SAVE", style="F.TButton", command=self.save_generated)
        self.genClear = Button(self.generateTab, text="CLEAR", style="F.TButton", command=self.clear_generated)

        self.topsOption.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        self.topCountList.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")
        self.classOption.grid(row=1, column=0, padx=5, pady=5, sticky="NSEW")
        self.classOptList.grid(row=1, column=1, padx=5, pady=5, sticky="NSEW")
        self.mainOptions.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky='NSEW')

        self.noConsec.grid(row=0, column=0, padx=5, pady=5, sticky="NSEW")
        self.skipLastWin.grid(row=0, column=1, padx=5, pady=5, sticky="NSEW")
        self.avoidClose.grid(row=1, column=1, padx=5, pady=(12,5), sticky="NSEW")
        self.commonPattern.grid(row=1, column=0, padx=5, pady=(12,5), sticky="NSEW")
        self.filterOptions.grid(row=0, column=2, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.h_sep_ga.grid(row=4, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        for i in range(5):
            self.dGen[i].positionDisplays(5, i)

        self.h_sep_gb.grid(row=16, column=0, columnspan=5, padx=5, pady=5, sticky='NSEW')

        self.genSet.grid(row=17, column=0, columnspan=3, padx=5, pady=(5, 2), sticky='NSEW')
        self.genSave.grid(row=17, column=3, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')
        self.genClear.grid(row=17, column=4, columnspan=1, padx=5, pady=(5, 2), sticky='NSEW')

        self.dataconn = db.databaseConn()

        self.sortOrder.set(0)

        self.topNumbers.set(0)
        self.noClose.set(0)
        self.noCon.set(0)
        self.skipWinner.set(0)
        self.pattern.set(0)

        self.varCountLimit.set('5')
        self.baseOption.set(1)

        self.loadData()
        self.loadStats()
        self.loadTrend()

        self.game_mean = int(575757/2)

    def loadData(self):

        winners = self.dataconn.get_fantasy_data()

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

        if len(selected) < 5:
            messagebox.showerror('Incomplete filter', 'Please enter five numbers to filter.')
            return

        winners = self.dataconn.get_fantasy_filtered(selected)

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

        stats = self.dataconn.get_number_stats('fantasy_five', self.sortOrder.get())

        self.statSelect.delete(0, END)

        for idx, stat in enumerate(stats):

            if idx == 26:
                self.statSelect.insert(END, '==========')

            if self.sortOrder.get() == 2:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), stat[1]])
            else:
                stat_line = "  -  ".join(['{:02d}'.format(stat[0]), '{:04d}'.format(stat[1])])

            self.statSelect.insert(END, stat_line)

        self.sscroller.config(command=self.statSelect.yview)

    def loadTrend(self):

        if os.path.exists('fantasy.jpg'):
            self.loadImage()
        else:
            t = threading.Thread(None, self.loadTrendFromData, ())
            t.start()

    def loadTrendFromData(self):
        
        self.progressBar.start()
        
        winners = self.dataconn.get_fantasy_data()

        cols = ['Draw Date', 'A', 'B', 'C', 'D', 'E']
        df = pd.DataFrame.from_records(winners, columns=cols)

        df['TOP'] = df[['Draw Date', 'A', 'B', 'C', 'D', 'E']].apply(self.check_top_n, args=(25, ), axis=1)
        df['IDX'] = df[['A', 'B', 'C', 'D', 'E']].apply(self.check_index_class, axis=1)

        plt.figure(figsize=(3,3))
        plt.plot(df['TOP'][:40], 'x-', label='T25', color='blue', alpha=0.5)
        plt.plot(df['IDX'][:40], 'o-', label='IDX', color='green', alpha=0.5)
        plt.grid(axis='both', color='grey', alpha=0.5)
        plt.legend(title='Labels', loc='upper right')
        plt.savefig('fantasy.jpg')

        self.progressBar.stop()

        self.loadImage()
        messagebox.showinfo('Reloaded', 'Trend graph has been reloaded.')

        return 
    
    def loadImage(self):

        image = Image.open("fantasy.jpg")
        image = image.resize((300,270))
        results_fig = ImageTk.PhotoImage(image)

        # Define a style
        root.results_fig = results_fig
        Style().configure("DT.TLabel", image=results_fig, background="white", anchor="left", font="Verdana 2")

        self.trendPlot['style'] = 'DT.TLabel'

    def check_top_n(self, data, start):

        dd, na, nb, nc, nd, ne = data

        num_set = [na, nb, nc, nd, ne]

        # get the top numbers prior to the draw date passed
        top_numbers = self.dataconn.get_top_stats_by_date(dd, 'fantasy_five')[start:start + 25]

        return len([num for num in num_set if num in top_numbers])

    def reload(self):

        try:
            os.remove('fantasy.jpg')
        except:
            pass

        self.loadTrend()

    def statSortOrder(self):

        if self.sortOrder.get() == 0:
            self.sortOrder.set(1)
        elif self.sortOrder.get() == 1:
            self.sortOrder.set(2)
        else:
            self.sortOrder.set(0)

        self.loadStats()

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

        ''' This function will generate combinations of numbers using the getCombination method of the sg object
        '''

        self.progressBar.start()

        all_numbers = [n[0] for n in self.dataconn.get_number_stats('fantasy_five', 0)]
        top_numbers = all_numbers[:25]

        if self.skipWinner.get() == 1:
            if self.baseOption.get() == 1 and int(self.varCountLimit.get()) == 5:
                self.skipWinner.set(0)
            else:
                all_numbers = [n for n in all_numbers if n not in list(self.dataconn.get_latest_winner('fantasy_five')[0])[1:]]
                top_numbers = [n for n in all_numbers if n not in list(self.dataconn.get_latest_winner('fantasy_five')[0])[1:]]

        self.generate_sets(all_numbers, top_numbers)

        self.progressBar.stop()

        return

    def generate_sets(self, all_numbers, top_numbers):

        start = datetime.now()
        print(start)

        self.count_limit = 5000

        if self.baseOption.get() == 1:

            selected = self.generate_and_filter(all_numbers, top_numbers)

        if self.baseOption.get() == 2:

            selected = self.retrieve_qualified_combos()

        ''' The logic below will select combinations and remove them from succeeding iterations
            This will ensure that combinations will not be selected again
        '''

        random.shuffle(selected)
        combos_all = self.set_iterator(selected)
        count = 0

        combo_sets = []

        while True:

            try:
                combo = next(combos_all)
                added = False
                
                if combo_sets:
                    for combo_set in combo_sets:
                        if len(combo_set) < 25:
                            if len(set(combo_set).intersection(set(combo))) == 0:
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
        
        print(f'After top number filter  : {len(selected)}')

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
        
        if self.pattern.get():

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
                    if self.dataconn.check_fantasy_winner(combo): # if winner, bypass
                        pass 
                    else:
                        selected.append(combo)
                except:
                    break
            
        print(f'After winner filter      : {len(selected)}')

        return selected 
    
    def retrieve_qualified_combos(self): 

        select_sql = f'''
        select combo_idx from fantasy_combos
        order by combo_idx desc
        limit 1'''

        hi_count = self.dataconn.execute_select(select_sql)

        game_mean = int(hi_count[0][0]/2)

        print(game_mean)

        select_sql = f'''
        select combo_key
        from fantasy_combos'''

        if int(self.varClassList.get()) == 0:
            select_sql += f''' where combo_idx <= {game_mean}'''
        else: 
            select_sql += f''' where combo_idx >  {game_mean}'''

        if self.noClose.get():
            select_sql += ''' and win_count = 0'''

        if self.noCon.get():
            select_sql += ''' and con_count = 0'''
        else:
            select_sql += ''' and con_count < 3'''

        if self.pattern.get():
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
        self.dataconn.store_fantasy_plays(generated)
        
        for i in range(5):
            win = self.dataconn.check_fantasy_winner(generated[i])
            self.dGen[i].changeTopStyle(generated[i], win)

    def check_index_class(self, num_set):

        combo_key = ''.join(['{:02d}'.format(int(num)) for num in num_set])

        idx_val = self.dataconn.get_combo_index(combo_key, 'fantasy_combos')
        
        return 1 if idx_val > self.game_mean else 0

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
                else:
                    prev = num 
        
        return True if count == 0 else False

    def check_pattern(self, num_set):

        odd_count = len([num for num in num_set if num % 2 == 1])

        if odd_count not in [0, 5]:
            return True
        else:
            return False

    def check_last_select(self, num_set, winners_list):

        match_check = [len(set(winner).intersection(set(num_set))) for winner in winners_list]
        
        match_check = [match for match in match_check if match in [0,1]]
        
        return True if len(match_check) in range(82, 92) else False

    def clear_generated(self):

        for i in range(5):
            self.dGen[i].clearTopStyle()

        self.generated = []
        self.genSet['text'] = 'GENERATE'

    def save_generated(self):

        self.dataconn.save_fantasy_plays()
        messagebox.showinfo('Saved', 'Combination set save in database')

    def getCountLimits(self):

        menu = self.topCountList['menu']
        menu.delete(0, 'end')

        for lim in [25, 20, 15]:
            menu.add_command(label=lim, command=lambda value=lim: self.varCountLimit.set(value))

    def exitRoutine(self):

        ''' This function will be executed when the user exits
        '''

        self.dataconn.delete_fantasy_plays()
        root.destroy()

root = Tk()
root.title("FANTASY FIVE")

# Set size
wh = 495
ww = 500

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
