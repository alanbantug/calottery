#! python3

import tkinter
from tkinter import *

from tkinter.ttk import *
import os

class displaySelection(object):

    def __init__(self, container, intvars, ltype):

        self.ltype = ltype

        if self.ltype == 1:
            self.topLimit = 39

        elif self.ltype == 2:
            self.topLimit = 47

        elif self.ltype == 3:
            self.topLimit = 70

        elif self.ltype == 4:
            self.topLimit = 69

        self.nums = []
        self.intvars = []

        Style().configure("B.TCheckbutton", font="Verdana 8")

        for i in range(self.topLimit):
            idx = "{0:02}".format(i + 1)
            self.nums.append(Checkbutton(container, text=idx, style="B.TCheckbutton", variable=intvars[i]))

        self.h_sep_a = Separator(container, orient=HORIZONTAL)

    def positionCheckbuttons(self, row, col):

        if self.ltype == 1:
            self.positionFantasy(row, col)
        elif self.ltype == 2:
            self.positionSuper(row, col)
        elif self.ltype == 3:
            self.positionMega(row, col)
        elif self.ltype == 4:
            self.positionPower(row, col)

    def positionFantasy(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.nums[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=3, sticky='W')
            col_ctr += 1
            if col_ctr > 10:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 40

        row_ctr += 1

    def positionSuper(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.nums[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=1, sticky='W')
            col_ctr += 1
            if col_ctr > 10:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 40

        row_ctr += 1

        self.h_sep_a.grid(row=row_ctr, column=col, padx=5, pady=5, sticky='NSEW')

        x_position = 9
        col_ctr = 1
        row_ctr += 1

    def positionMega(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.num[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=5, sticky='W')
            col_ctr += 1
            if col_ctr > 10:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 20

        row_ctr += 1

        self.h_sep_a.grid(row=row_ctr, column=col, padx=5, pady=5, sticky='NSEW')

        x_position = 9
        col_ctr = 1
        row_ctr += 1

        for i in range(self.extLimit):
            self.ext[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=5, sticky='W')
            col_ctr += 1
            if col_ctr > 10:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 20

    def positionPower(self, row, col):

        x_position = 9
        col_ctr = 1
        row_ctr = row

        for i in range(self.topLimit):
            self.num[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=5, sticky='W')
            col_ctr += 1
            if col_ctr > 10:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 20

        row_ctr += 1

        self.h_sep_a.grid(row=row_ctr, column=col, padx=5, pady=5, sticky='NSEW')

        x_position = 9
        col_ctr = 1
        row_ctr += 1

        for i in range(self.extLimit):
            self.ext[i].grid(row=row_ctr, column=col, padx=(x_position,10), pady=5, sticky='W')
            col_ctr += 1
            if col_ctr > 10:
                col_ctr = 1
                row_ctr += 1
                x_position = 9
            else:
                x_position += 20

