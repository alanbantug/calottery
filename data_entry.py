import tkinter
from tkinter import *

from tkinter.ttk import *
from tkinter import messagebox

from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
from tkcalendar import Calendar
from datetime import datetime

import os
import json
# import shutil
# import psycopg2

import dbaccess as db


class Application(Frame):

    def __init__(self, master):

        self.master = master
        self.main_container = Frame(self.master)

        # Define the source and target folder variables

        self.origin = os.getcwd()
        self.gotData = IntVar()
        self.copying = 0
        self.source = ""
        self.target = ""
        self.script = ""
        self.allSet = True
        self.numA = StringVar()
        self.numB = StringVar()
        self.numC = StringVar()
        self.numD = StringVar()
        self.numE = StringVar()
        self.numF = StringVar()
        self.updatedFiles = IntVar()
        self.initFolders = IntVar()
        self.type = IntVar()
        self.credSet = IntVar()
        self.credSource = StringVar()

        # Create main frame
        self.main_container.grid(column=0, row=0, sticky=(N,S,E,W))

        # Set Label styles
        Style().configure("M.TLabel", font="Courier 20 bold", height="20", foreground="blue", anchor="center")
        Style().configure("A.TLabel", font="Verdana 8")
        Style().configure("D.TLabel", font="Verdana 8", background="white", width=25)
        Style().configure("MS.TLabel", font="Verdana 10" )
        Style().configure("S.TLabel", font="Verdana 8" )
        Style().configure("G.TLabel", font="Verdana 8")
        Style().configure("T.TLabel", font="Verdana 12 bold")

        # Set button styles
        Style().configure("D.TButton", font="Verdana 8", relief="ridge", width=25)
        Style().configure("B.TButton", font="Verdana 8", relief="ridge", width=16)

        # Set check button styles
        Style().configure("B.TCheckbutton", font="Verdana 8")
        Style().configure("D.TCheckButton", font="Verdana 8", width='20')

        Style().configure("O.TLabelframe.Label", font="Verdana 8", foreground="black")

        self.parentTab = Notebook(self.main_container)
        self.entUpdTab = Frame(self.parentTab)   # first page, which would get widgets gridded into it
        self.aboutTab = Frame(self.parentTab)   # third page
        self.parentTab.add(self.entUpdTab, text='    Data   ')
        self.parentTab.add(self.aboutTab, text='    About     ')

        # Create widgets
        ''' Main container
        '''
        self.sep_a = Separator(self.main_container, orient=HORIZONTAL)
        self.mainLabel = Label(self.main_container, text="DATA ENTRY AND UPDATE", style="M.TLabel" )
        self.subLabelA = Label(self.main_container, text="See About for more information about this script", style="S.TLabel" )
        
        self.exit = Button(self.main_container, text="EXIT", style="B.TButton", command=root.destroy)

        ''' position widgets
        '''
        self.mainLabel.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
        self.subLabelA.grid(row=1, column=0, padx=5, pady=0, sticky='NSEW')
        self.parentTab.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.sep_a.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        self.exit.grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky='NSEW')

        ''' Entry tab
        '''
        self.sep_b = Separator(self.entUpdTab, orient=HORIZONTAL)
        self.sep_c = Separator(self.entUpdTab, orient=HORIZONTAL)
        self.sep_d = Separator(self.entUpdTab, orient=HORIZONTAL)

        ''' game selection
        '''
        self.typeGroup = LabelFrame(self.entUpdTab, text=' Game Selection ', style="O.TLabelframe")
        self.typeA = Radiobutton(self.typeGroup, text="Fantasy", style="B.TRadiobutton", variable=self.type, value=1)
        self.typeB = Radiobutton(self.typeGroup, text="Super", style="B.TRadiobutton", variable=self.type, value=2)
        self.typeC = Radiobutton(self.typeGroup, text="Mega", style="B.TRadiobutton", variable=self.type, value=3)
        self.typeD = Radiobutton(self.typeGroup, text="Powerball", style="B.TRadiobutton", variable=self.type, value=4)

        ''' main numbers
        '''
        self.numbers = LabelFrame(self.entUpdTab, text='Numbers', style="O.TLabelframe")
        self.numberA = Entry(self.numbers, textvariable=self.numA, width="5")
        self.numberB = Entry(self.numbers, textvariable=self.numB, width="5")
        self.numberC = Entry(self.numbers, textvariable=self.numC, width="5")
        self.numberD = Entry(self.numbers, textvariable=self.numD, width="5")
        self.numberE = Entry(self.numbers, textvariable=self.numE, width="5")

        ''' super, mega or power
        '''
        self.extras = LabelFrame(self.entUpdTab, text='Extra', style="O.TLabelframe")
        self.numberF = Entry(self.extras, textvariable=self.numF, width="5")

        ''' date selection
        '''
        self.dateSelect = LabelFrame(self.entUpdTab, text='Select Date', style="O.TLabelframe")
        self.select = Button(self.dateSelect, text="DATE", style="D.TButton", command=self.showCalendar)
        self.dateLabel = Label(self.dateSelect, text="None", style="D.TLabel" )

        self.retrieve = Button(self.entUpdTab, text="RETRIEVE", style="B.TButton", command=self.getData)
        self.save = Button(self.entUpdTab, text="SAVE", style="B.TButton", command=self.saveData)
        self.clear = Button(self.entUpdTab, text="CLEAR", style="B.TButton", command=self.clearEntry)

        ''' position widgets
        '''

        self.typeA.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        self.typeB.grid(row=0, column=0, padx=(125,0), pady=5, sticky='W')
        self.typeC.grid(row=0, column=0, padx=(215,0), pady=5, sticky='W')
        self.typeD.grid(row=0, column=0, padx=(305,0), pady=5, sticky='W')
        self.typeGroup.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')

        self.sep_b.grid(row=1, column=0, padx=5, pady=5, sticky='NSEW')

        self.numberA.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        self.numberB.grid(row=0, column=0, padx=(75,0), pady=5, sticky='W')
        self.numberC.grid(row=0, column=0, padx=(145,0), pady=5, sticky='W')
        self.numberD.grid(row=0, column=0, padx=(215,0), pady=5, sticky='W')
        self.numberE.grid(row=0, column=0, padx=(285,10), pady=5, sticky='W')
        self.numbers.grid(row=2, column=0, padx=(5,20), pady=5, sticky='W')

        self.numberF.grid(row=0, column=0, padx=(10,10), pady=5, sticky='NSEW')
        self.extras.grid(row=2, column=0, padx=(350,0), pady=5, sticky='W')

        self.sep_c.grid(row=3, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.select.grid(row=0, column=0, padx=5, pady=5, sticky='W')
        self.dateLabel.grid(row=0, column=0, padx=(200,0), pady=5, sticky='W')
        self.dateSelect.grid(row=4, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')
        
        self.sep_d.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky='NSEW')

        self.retrieve.grid(row=6, column=0, padx=5, pady=5, sticky='W')
        self.save.grid(row=6, column=0, padx=(145,0), pady=5, sticky='W')
        self.clear.grid(row=6, column=0, padx=(285,0), pady=5, sticky='W')

        ''' About tab
        '''
        self.aboutTextA = Label(self.aboutTab, text="This script will allow users to enter, update and delete winners from ", style="A.TLabel" ) 
        self.aboutTextB = Label(self.aboutTab, text="the four main draw game in the California Lottery website. The data is", style="A.TLabel" )
        self.aboutTextC = Label(self.aboutTab, text="saved in SQL database and will be used for further analysis, including", style="A.TLabel" )
        self.aboutTextD = Label(self.aboutTab, text="feeding machine learning models", style="A.TLabel" )

        ''' Position
        '''

        self.aboutTextA.grid(row=1, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextB.grid(row=2, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextC.grid(row=3, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')
        self.aboutTextD.grid(row=4, column=0, columnspan=4, padx=5, pady=0, sticky='NSEW')

        self.dataconn = db.databaseConn()
        self.type.set(1)
        self.gotData.set(0)

    # def setCredentials(self):

    #     pathname = askopenfilename()

    #     self.credSource.set(pathname)
    #     self.credSet.set(0)
        
    #     if pathname:
    #         try:
    #             if self.credSource.get().endswith(".json"):
    #                 self.updateCreds()
    #                 self.credSet.set(1)
    #             else:
    #                 messagebox.showerror("Invalid file selected", "Invalid file type was selected. Please select again.")
    #                 self.credSource.set('')

    #         except Exception as e:
    #             print(e)

    # def updateCreds(self):
        
    #     target = 'credentials.json'

    #     try:
    #         shutil.copy(self.credSource.get(), target)
    #         messagebox.showinfo('Credentials set', 'Credentials successfully set')

    #         self.credSet.set(1)

    #     except Exception as e:
    #         print(f"An error occurred: {e}")

    # def create_connection(self):

    #     ''' Create connection to PostgreSQL database
    #     '''

    #     with open(r"credentials.json", "r") as credentials:
    #         creds = json.loads(credentials.read())

    #     conn = psycopg2.connect(database=creds['database'],
    #     user=creds['user'],
    #     password=creds['password'],
    #     host=creds['host'],
    #     port=creds['port'])

    #     return conn

    def getData(self):

        try:
            # conn = self.create_connection()

            if self.type.get() == 1:
                data = self.get_fantasy(self.dataconn)
                
                dd, n1, n2, n3, n4, n5 = data[0]

                self.numA.set(n1)
                self.numB.set(n2)
                self.numC.set(n3)
                self.numD.set(n4)
                self.numE.set(n5)

            else:
                data = self.get_extended(self.dataconn)

                dd, n1, n2, n3, n4, n5, n6 = data[0]

                self.numA.set(n1)
                self.numB.set(n2)
                self.numC.set(n3)
                self.numD.set(n4)
                self.numE.set(n5)
                self.numF.set(n6)

            # conn.close()

            self.gotData.set(1)

        except Exception as e:
            messagebox.showerror('Error', 'Combination for date not found')

    def get_fantasy(self, conn):

        dd = self.dateLabel['text']

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume
        from fantasy_five
        where draw_date = '{dd}'
        '''

        cur = conn.cursor()

        cur.execute(select_sql)

        winner = cur.fetchall()

        cur.close()

        return winner

    def get_extended(self, conn):

        if self.type.get() == 2:
            table_name = 'super_lotto'
        
        if self.type.get() == 3:
            table_name = 'mega_lotto'

        if self.type.get() == 4:
            table_name = 'power_ball'

        dd = self.dateLabel['text']

        select_sql = f'''
        select to_char(draw_date, 'YYYY-MM-DD'), numa, numb, numc, numd, nume, numx
        from {table_name}
        where draw_date = '{dd}'
        '''

        cur = conn.cursor()

        cur.execute(select_sql)

        winner = cur.fetchall()

        cur.close()

        return winner

    def saveData(self):

        if self.credSet.get():
            pass
        else:
            messagebox.showerror('Credentials not set', 'Please set credentials before saving data.')
            return

        # conn = self.create_connection()
        conn.autocommit = True

        if self.type.get() == 1:
            if self.save_fantasy(self.dataconn):
                messagebox.showinfo('Saved', 'Combination set save in database')
            else:
                messagebox.showerror('Error', 'Combination not saved')
        else:
            if self.save_extended(self.dataconn):
                messagebox.showinfo('Saved', 'Combination set save in database')
            else:
                messagebox.showerror('Error', 'Combination not saved')

    def save_fantasy(self, conn):

        try:
            
            numa = self.numA.get()
            numb = self.numB.get()
            numc = self.numC.get()
            numd = self.numD.get()
            nume = self.numE.get()
            draw = self.dateLabel['text']

            fantasy_data = (draw, numa, numb, numc, numd, nume)

            cursor = conn.cursor()

            if self.gotData.get():
                update_sql = f'''
                update fantasy_five
                set numa = {numa}, numb = {numb}, numc = {numc}, numd = {numd}, nume = {nume}
                where draw_date = '{draw}'
                '''

                cursor.execute(update_sql)

            else:
                insert_sql = '''
                insert into fantasy_five (draw_date, numa, numb, numc, numd, nume)
                values (%s, %s, %s, %s, %s, %s)
                '''

                cursor.execute(insert_sql, fantasy_data)
                
            cursor.close()
            # conn.close()
            
            return True
        
        except Exception as e:
            print(f'Error inserting record : {e}')
            # conn.close()
            return False            
            
    def save_extended(self, conn):
       
        if self.type.get() == 2:
           table_name = 'super_lotto'

        if self.type.get() == 3:
           table_name = 'mega_lotto'

        if self.type.get() == 4:
           table_name = 'power_ball'

        try:
            
            numa = self.numA.get()
            numb = self.numB.get()
            numc = self.numC.get()
            numd = self.numD.get()
            nume = self.numE.get()
            numx = self.numF.get()
            draw = self.dateLabel['text']

            extended_data = (draw, numa, numb, numc, numd, nume, numx)

            cursor = conn.cursor()

            if self.gotData.get():
                update_sql = f'''
                update {table_name}
                set numa = {numa}, numb = {numb}, numc = {numc}, numd = {numd}, nume = {nume}, numx = {numx}
                where draw_date = '{draw}'
                '''

                cursor.execute(update_sql)

            else:
                insert_sql = f'''
                insert into {table_name} (draw_date, numa, numb, numc, numd, nume, numx)
                values (%s, %s, %s, %s, %s, %s, %s)
                '''

                cursor.execute(insert_sql, extended_data)
                
            cursor.close()
            # conn.close()

            return True
        except Exception as e:
            print(f'Error inserting record : {e}')
            # conn.close()
            return False            
            
    def clearEntry(self):

        self.numA.set('')
        self.numB.set('')
        self.numC.set('')
        self.numD.set('')
        self.numE.set('')
        self.numF.set('')

        self.dateLabel['text'] = ''

    def showCalendar(self):

        self.popDate = Toplevel(self.main_container)

        curr_day = datetime.now().day
        curr_month = datetime.now().month
        curr_year = datetime.now().year

        self.cal = Calendar(self.popDate, selectmode = 'day', year = curr_year, 
                            month = curr_month, day = curr_day)
        self.selectDate = Button(self.popDate, text="Pick Date", style="B.TButton", command=self.pickDate)
        self.cal.grid(row=0, column=0, padx=5, pady=2, sticky='NSEW')
        self.selectDate.grid(row=1, column=0, padx=5, pady=2, sticky='NSEW')

        poph = 220
        popw = 260
        popws = self.popDate.winfo_screenwidth()
        pophs = self.popDate.winfo_screenheight()
        popx = (popws/2) - (popw/2)
        popy = (pophs/2) - (poph/2)

        self.popDate.geometry('%dx%d+%d+%d' % (popw, poph, popx, popy))
    
    def pickDate(self):
        
        # convert string to datetime
        dt = datetime.strptime(self.cal.get_date(), "%m/%d/%y" )

        # convert datetime to string in YYYY-MM-DD format
        ds = dt.strftime("%Y-%m-%d")
        
        # set label value
        self.dateLabel.config(text = ds)
        
        self.popDate.destroy()

root = Tk()
root.title("DATA ENTRY")

# Set size

wh = 400
ww = 435

root.resizable(height=False, width=False)

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
