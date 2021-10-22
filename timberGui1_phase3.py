import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import warnings
import pandas as pd
import tkinter.messagebox as messagebox
import datetime
import numpy as np
warnings.simplefilter("ignore")

class timberFilter(ttk.Frame):
    #add the timber filtering buttons, functions here
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.inFile = None
        self.outPath = None
        self.grid()
        self.createWidgets()
        self.runCount = 0
     
    def csvFilter(self):
        try:
            if not self.inFile:
                messagebox.showinfo('Missing input','Please select the county input file')
                return
        except:
            messagebox.showinfo('Missing input','Please select the county input file')
            return
        
        try:
            if not self.outPath:
                messagebox.showinfo('Missing output','Please select the output file directory')
                return
        except:
            messagebox.showinfo('Missing output','Please select the output file directory')
            return
        
        df = pd.read_csv(self.inFile, index_col=False)
        
        #now filter through the dataframe keeping rows that meet certain criteria
        #size, value, trees
        df = df[df['GIS_ACRES'] >= float(self.e1.get())]
        df = df[df['MKRAT'] >= float(self.e2.get())]
        df = df[df['DECIDPER'] >= float(self.e3.get())]
        df = df[df['EVERGPER'] >= float(self.e4.get())]
        
        #parcel access
        if self.waterFeat.get() == 1:
            df = df[df['WATER'] == 1]
        
        if self.accessDist.get() == 1:
            df = df[df['ROAD'] == 1]
        
        #ownership
        if self.privOwner.get() == 1:
            df = df[df['PRIVATE'] == 1]
        
        if self.owner.get() == 1:
            df = df[df['OWNERSTATE'] != 'WA']
        if self.owner.get() == 2:
            df = df[df['OWNERSTATE'] == 'WA']
            
        #counties
        keeps = []
        if self.countyClal.get()==1:
            keeps.append('Clallam')
        if self.countyIsla.get()==1:
            keeps.append('Island')
        if self.countyJeff.get()==1:
            keeps.append('Jefferson')
        if self.countyKing.get()==1:
            keeps.append('King')
        if self.countySanj.get()==1:
            keeps.append('SanJuan')
        if self.countySkag.get()==1:
            keeps.append('Skagit')
        if self.countySnoh.get()==1:
            keeps.append('Snohomish')
        if self.countyWhat.get()==1:
            keeps.append('Whatcom')
            
        df = df[df['COUNTY'].isin(keeps)]
        
        self.runCount += 1
        
        now = datetime.datetime.now()
        todDate = str(now.year) + '_' + str(now.month) + '_' + str(now.day)
        csvName = 'recParcels' + '_' + todDate + '_' + str(self.runCount) + '.csv'
        csvPath = self.outPath + '/' + csvName
        
        df.to_csv(csvPath)
    
    def filePath(self):
        self.inFile = filedialog.askopenfilename(title = 'Select file', filetypes = (('CSV Files', '*.csv'),))
        
        self.inTextBox.configure(state='normal') #configures textbox for UI purposes
        self.inTextBox.delete(1.0, 'end')
        self.inTextBox.insert('end',self.inFile)
        self.inTextBox.configure(state='disabled')
        
    def outputPath(self):
        self.outPath = filedialog.askdirectory()

        self.outTextBox.configure(state='normal') #configures textbox for UI purposes
        self.outTextBox.delete(1.0, 'end')
        self.outTextBox.insert('end',self.outPath)
        self.outTextBox.configure(state='disabled')
        
    def quitProg(self):
       window.destroy()
    
    def createWidgets(self):
        self.owner = tk.IntVar(self)
        self.privOwner = tk.IntVar(self)
        self.accessDist = tk.IntVar(self)
        self.waterFeat = tk.IntVar(self)
        
        self.countySnoh = tk.IntVar(self)
        self.countySanj = tk.IntVar(self)
        self.countyClal = tk.IntVar(self)
        self.countyIsla = tk.IntVar(self)
        self.countyJeff = tk.IntVar(self)
        self.countyKing = tk.IntVar(self)
        self.countySkag = tk.IntVar(self)
        self.countyWhat = tk.IntVar(self)
        
        self.e1 = tk.IntVar(self)
        self.e2 = tk.IntVar(self)
        self.e3 = tk.IntVar(self)
        self.e4 = tk.IntVar(self)
        
        ##grid placement in order

        #entries: e1 = acreage, e2 = value ratio
        #e3 = deciduous coverage, e4 = evergreen coverage

        #row0
        inButton = tk.Button(self,text='Select county input file',
                             command=self.filePath).grid(row=0, column=0, sticky=tk.E)
        
        self.inTextBox = tk.Text(self, state='disabled', width=70, height=1)
        self.inTextBox.grid(row=0, column=1, sticky=tk.W)
        
        #row1
        outputButton = tk.Button(self,text='Select output file directory',
                                command=self.outputPath).grid(row=1, column=0, sticky=tk.E)

        self.outTextBox = tk.Text(self, state='disabled', width=70, height=1)
        self.outTextBox.grid(row=1, column=1, columnspan=3, sticky=tk.W)

        #row2
        ownerLabel = tk.Label(self,
                            text=('Owner status (private owners exclude governments, '
                            'corporations, and other organizations)'),
                            font='Helvetica 10 bold').grid(row=2, column=0, sticky=tk.W, columnspan=3)
        
        countyChoiceLabel = tk.Label(self,
                                     text=('Select county(-ies)'),
                                     font='Helvetica 10 bold').grid(row=2, column=1, sticky=tk.W)

        #row3
        r1 = tk.Radiobutton(self,
                        text='Out-of-state owner only (Note: This filter will not work for Clallam or Jefferson county due to missing data)',
                        variable = self.owner,
                        value = 1).grid(row=3, column=0, sticky=tk.W)
        
        cc1 = tk.Checkbutton(self,
                             text='Snohomish',
                             variable=self.countySnoh).grid(row=3, column=1, sticky=tk.W)
        
        cc2 = tk.Checkbutton(self, text='San Juan',
                             variable=self.countySanj).grid(row=3, column=1, sticky=tk.W, padx = 100)

        #row4
        r2 = tk.Radiobutton(self,
                        text='In-state owner only (Note: This filter will not work for Clallam or Jefferson county due to missing data)',
                        variable = self.owner,
                        value = 2).grid(row=4, column=0, sticky=tk.W)
        
        cc2 = tk.Checkbutton(self, text='Clallam',
                             variable=self.countyClal).grid(row=4, column=1, sticky=tk.W)
        
        cc2 = tk.Checkbutton(self, text='Island',
                             variable=self.countyIsla).grid(row=4, column=1, sticky=tk.W, padx=100)

        #row5
        r3 = tk.Radiobutton(self,
                        text='All owners (Note: This filter will not work for Clallam or Jefferson county due to missing data)',
                        variable = self.owner,
                        value = 3).grid(row=5, column=0, sticky=tk.W)
        
        cc2 = tk.Checkbutton(self, text='Jefferson',
                             variable=self.countyJeff).grid(row=5, column=1, sticky=tk.W)
        
        cc2 = tk.Checkbutton(self, text='King',
                             variable=self.countyKing).grid(row=5, column=1, sticky=tk.W, padx=100)

        #row6
        c3 = tk.Checkbutton(self,
                        text='Private owner only (Note: This filter will not work for San Juan or Island County due to missing data)',
                        variable=self.privOwner).grid(row=6, column=0, sticky=tk.W)
        
        cc2 = tk.Checkbutton(self, text='Skagit',
                             variable=self.countySkag).grid(row=6, column=1, sticky=tk.W)
        
        cc2 = tk.Checkbutton(self, text='Whatcom',
                             variable=self.countyWhat).grid(row=6, column=1, sticky=tk.W, padx=100)

        #row7
        accessVar = tk.Label(self,
                            text=('Parcel access'),
                            font='Helvetica 10 bold').grid(row=7, column=0, sticky=tk.W)

        #row8
        c4 = tk.Checkbutton(self,
                        text='Parcels adjacent to roads only',
                        variable=self.accessDist).grid(row=8, column=0, sticky=tk.W)

        #row9
        c5 = tk.Checkbutton(self,
                        text='Parcels with no water features',
                        variable=self.waterFeat).grid(row=9, column=0, sticky=tk.W)

        #row10
        parcelSize = tk.Label(self,
                            text=('Minimum parcel size (minimum of 5, in acres):'),
                            font='Helvetica 10 bold').grid(row=10, column=0, sticky=tk.E)

        self.e1 = tk.Entry(self)
        self.e1.insert(10, '5')
        self.e1.grid(row=10, column=1, sticky=tk.W)

        #row11
        parcelVal = tk.Label(self,
                            text=('Land to total value ratio (0 to 1):'),
                            font='Helvetica 10 bold').grid(row=11, column=0, sticky=tk.E)

        self.e2 = tk.Entry(self)
        self.e2.insert(10, '.75')
        self.e2.grid(row=11, column=1, sticky=tk.W)

        #row13
        decidVar = tk.Label(self,
                            text=('Deciduous percent coverage per parcel (0 to 100):'),
                            font='Helvetica 10 bold').grid(row=13, column=0, sticky=tk.E)

        self.e3 = tk.Entry(self)
        self.e3.insert(10, '15')
        self.e3.grid(row=13, column=1, sticky=tk.W)

        #row14
        evergVar = tk.Label(self,
                            text=('Evergreen percent coverage per parcel (0 to 100):'),
                            font='Helvetica 10 bold').grid(row=14, column=0, sticky=tk.E)

        self.e4 = tk.Entry(self)
        self.e4.insert(10, '15')
        self.e4.grid(row=14, column=1, sticky=tk.W)

        #row15
        runButton = tk.Button(self, text='Run with selected filters',
                            command=self.csvFilter).grid(row=15, column=0, sticky=tk.W)

        quitButton = tk.Button(self,text='Quit',
                            command=self.quitProg).grid(row=15, column=1, sticky=tk.W)
    
class csvEdit(ttk.Frame):
    #csv editing functionality here
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        self.inFile = None
        self.outPath = None
        self.parcCount = 0
        self.df = None
        self.grid()
        self.createWidgets2()
        
    def nextParc(self):
        try:
            if self.df.empty:
                messagebox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
        except:
            messagebox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
            return
        
        #save typed results
        self.df.loc[:, ('CLAYRANK1')][self.parcCount] = self.rankText.get('1.0','end-1c')
        self.df.loc[:, ('CLAYRANK2')][self.parcCount] = self.rankText2.get('1.0','end-1c')
        self.df.loc[:, ('GENNOTES')][self.parcCount] = self.notesText.get('1.0','end-1c')
        self.df.loc[:, ('CONNOTES')][self.parcCount] = self.contactText.get('1.0','end-1c')
        
        #clear fields for next entry
        self.rankText.delete(1.0, 'end')
        self.notesText.delete(1.0, 'end')
        self.rankText2.delete(1.0, 'end')
        self.contactText.delete(1.0, 'end')
        
        #count stuff for parcel ID and number
        self.parcCount = self.parcCount+1
        
        if self.parcCount < 0:
            self.parcCount = len(self.df.index) + self.parcCount

        if self.parcCount >= len(self.df.index):
            self.parcCount = len(self.df.index) - self.parcCount
            
        parcCountStr = '%s/%s' % (self.parcCount+1, len(self.df.index))
        
        try:
            parcIDCurrent = int(self.df.loc[:, ('PARCEL_ID')][self.parcCount])
        except:
            parcIDCurrent = self.df.loc[:, ('PARCEL_ID')][self.parcCount]

        ownerCurrent = self.df.loc[:, ('OWNERADD')][self.parcCount]
        taxCurrent = self.df.loc[:, ('TAXADD')][self.parcCount]
        sizeCurrent = round(self.df.loc[:, ('GIS_ACRES')][self.parcCount],2)
        countyCurrent = self.df.loc[:, ('COUNTY')][self.parcCount]
        
        self.countyIDBox.configure(state='normal')
        self.countyIDBox.delete(1.0, 'end')
        self.countyIDBox.insert('end', countyCurrent)
        self.countyIDBox.configure(state='disabled')

        self.parcNumBox.configure(state='normal')
        self.parcNumBox.delete(1.0, 'end')
        self.parcNumBox.insert('end', parcCountStr)
        self.parcNumBox.configure(state='disabled')

        self.parcIDBox.configure(state='normal')
        self.parcIDBox.delete(1.0, 'end')
        self.parcIDBox.insert('end', parcIDCurrent)
        self.parcIDBox.configure(state='disabled')

        self.ownerText.configure(state='normal')
        self.ownerText.delete(1.0, 'end')
        self.ownerText.insert('end', ownerCurrent)
        self.ownerText.configure(state='disabled')

        self.taxText.configure(state='normal')
        self.taxText.delete(1.0, 'end')
        self.taxText.insert('end', taxCurrent)
        self.taxText.configure(state='disabled')

        self.sizeText.configure(state='normal')
        self.sizeText.delete(1.0, 'end')
        self.sizeText.insert('end', sizeCurrent)
        self.sizeText.configure(state='disabled')
        
        #check for and populate existing rank/notes fields
        self.rankText.insert('end', self.df.loc[:, ('CLAYRANK1')][self.parcCount])
        self.notesText.insert('end', self.df.loc[:, ('GENNOTES')][self.parcCount])
        self.rankText2.insert('end', self.df.loc[:, ('CLAYRANK2')][self.parcCount])
        self.contactText.insert('end', self.df.loc[:, ('CONNOTES')][self.parcCount])
        
    def prevParc(self):
        try:
            if self.df.empty:
                messagebox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
        except:
            messagebox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
            return
        
        #save typed results
        self.df.loc[:, ('CLAYRANK1')][self.parcCount] = self.rankText.get('1.0','end-1c')
        self.df.loc[:, ('CLAYRANK2')][self.parcCount] = self.rankText2.get('1.0','end-1c')
        self.df.loc[:, ('GENNOTES')][self.parcCount] = self.notesText.get('1.0','end-1c')
        self.df.loc[:, ('CONNOTES')][self.parcCount] = self.contactText.get('1.0','end-1c')
        
        #clear fields for next entry
        self.rankText.delete(1.0, 'end')
        self.notesText.delete(1.0, 'end')
        self.rankText2.delete(1.0, 'end')
        self.contactText.delete(1.0, 'end')
        
        #count stuff for parcel ID and number
        self.parcCount = self.parcCount-1
        
        if self.parcCount < 0:
            self.parcCount = len(self.df.index) + self.parcCount

        if self.parcCount >= len(self.df.index):
            self.parcCount = len(self.df.index) - self.parcCount
            
        parcCountStr = '%s/%s' % (self.parcCount+1, len(self.df.index))
        
        try:
            parcIDCurrent = int(self.df.loc[:, ('PARCEL_ID')][self.parcCount])
        except:
            parcIDCurrent = self.df.loc[:, ('PARCEL_ID')][self.parcCount]

        ownerCurrent = self.df.loc[:, ('OWNERADD')][self.parcCount]
        taxCurrent = self.df.loc[:, ('TAXADD')][self.parcCount]
        sizeCurrent = round(self.df.loc[:, ('GIS_ACRES')][self.parcCount],2)
        countyCurrent = self.df.loc[:, ('COUNTY')][self.parcCount]
        
        self.countyIDBox.configure(state='normal')
        self.countyIDBox.delete(1.0, 'end')
        self.countyIDBox.insert('end', countyCurrent)
        self.countyIDBox.configure(state='disabled')

        self.parcNumBox.configure(state='normal')
        self.parcNumBox.delete(1.0, 'end')
        self.parcNumBox.insert('end', parcCountStr)
        self.parcNumBox.configure(state='disabled')

        self.parcIDBox.configure(state='normal')
        self.parcIDBox.delete(1.0, 'end')
        self.parcIDBox.insert('end', parcIDCurrent)
        self.parcIDBox.configure(state='disabled')

        self.ownerText.configure(state='normal')
        self.ownerText.delete(1.0, 'end')
        self.ownerText.insert('end', ownerCurrent)
        self.ownerText.configure(state='disabled')

        self.taxText.configure(state='normal')
        self.taxText.delete(1.0, 'end')
        self.taxText.insert('end', taxCurrent)
        self.taxText.configure(state='disabled')

        self.sizeText.configure(state='normal')
        self.sizeText.delete(1.0, 'end')
        self.sizeText.insert('end', sizeCurrent)
        self.sizeText.configure(state='disabled')
        
        #check for and populate existing rank/notes fields
        self.rankText.insert('end', self.df.loc[:, ('CLAYRANK1')][self.parcCount])
        self.notesText.insert('end', self.df.loc[:, ('GENNOTES')][self.parcCount])
        self.rankText2.insert('end', self.df.loc[:, ('CLAYRANK2')][self.parcCount])
        self.contactText.insert('end', self.df.loc[:, ('CONNOTES')][self.parcCount])
        
    def parcNavigate(self):
        try:
            if self.df.empty:
                messagebox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
        except:
            messagebox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
            return
        
        try:
            v = int(self.parcNavText.get('1.0', 'end-1c'))
        except:
            messagebox.showinfo('Integers only','Please enter a whole number.')
            return
        
        newParc = int(self.parcNavText.get('1.0', 'end-1c'))

        #make sure entered value is valid
        if newParc < 1 or newParc > len(self.df.index):
            messagebox.showinfo('Invalid parcel number','Make sure parcel number is between 1 and the maximum parcel number for this CSV.')
            self.parcNavText.delete(1.0, 'end')
            return
        
        #save typed results
        self.df.loc[:, ('CLAYRANK1')][self.parcCount] = self.rankText.get('1.0','end-1c')
        self.df.loc[:, ('CLAYRANK2')][self.parcCount] = self.rankText2.get('1.0','end-1c')
        self.df.loc[:, ('GENNOTES')][self.parcCount] = self.notesText.get('1.0','end-1c')
        self.df.loc[:, ('CONNOTES')][self.parcCount] = self.contactText.get('1.0','end-1c')
        
        #clear fields for next entry
        self.rankText.delete(1.0, 'end')
        self.notesText.delete(1.0, 'end')
        self.rankText2.delete(1.0, 'end')
        self.contactText.delete(1.0, 'end')
        
        #set new parcCount to entered value
        self.parcCount = newParc-1
        self.parcNavText.delete(1.0, 'end')
        
        parcCountStr = '%s/%s' % (self.parcCount+1, len(self.df.index))
        
        try:
            parcIDCurrent = int(self.df.loc[:, ('PARCEL_ID')][self.parcCount])
        except:
            parcIDCurrent = self.df.loc[:, ('PARCEL_ID')][self.parcCount]

        ownerCurrent = self.df.loc[:, ('OWNERADD')][self.parcCount]
        taxCurrent = self.df.loc[:, ('TAXADD')][self.parcCount]
        sizeCurrent = round(self.df.loc[:, ('GIS_ACRES')][self.parcCount],2)
        countyCurrent = self.df.loc[:, ('COUNTY')][self.parcCount]
        
        self.countyIDBox.configure(state='normal')
        self.countyIDBox.delete(1.0, 'end')
        self.countyIDBox.insert('end', countyCurrent)
        self.countyIDBox.configure(state='disabled')

        self.parcNumBox.configure(state='normal')
        self.parcNumBox.delete(1.0, 'end')
        self.parcNumBox.insert('end', parcCountStr)
        self.parcNumBox.configure(state='disabled')

        self.parcIDBox.configure(state='normal')
        self.parcIDBox.delete(1.0, 'end')
        self.parcIDBox.insert('end', parcIDCurrent)
        self.parcIDBox.configure(state='disabled')

        self.ownerText.configure(state='normal')
        self.ownerText.delete(1.0, 'end')
        self.ownerText.insert('end', ownerCurrent)
        self.ownerText.configure(state='disabled')

        self.taxText.configure(state='normal')
        self.taxText.delete(1.0, 'end')
        self.taxText.insert('end', taxCurrent)
        self.taxText.configure(state='disabled')

        self.sizeText.configure(state='normal')
        self.sizeText.delete(1.0, 'end')
        self.sizeText.insert('end', sizeCurrent)
        self.sizeText.configure(state='disabled')
        
        #check for and populate existing rank/notes fields
        self.rankText.insert('end', self.df.loc[:, ('CLAYRANK1')][self.parcCount])
        self.notesText.insert('end', self.df.loc[:, ('GENNOTES')][self.parcCount])
        self.rankText2.insert('end', self.df.loc[:, ('CLAYRANK2')][self.parcCount])
        self.contactText.insert('end', self.df.loc[:, ('CONNOTES')][self.parcCount])
    
    def quitProg(self):
        if self.outPath == None:
            userQuit = messagebox.askyesno('Warning','CSV cannot be saved without an output path selected.\nQuit without saving?')
            if userQuit == False:
                return
            if userQuit == True:
                window.destroy()
                return

        #save current fields
        try:
            self.df.loc[:, ('CLAYRANK1')][self.parcCount] = self.rankText.get('1.0','end-1c')
            self.df.loc[:, ('CLAYRANK2')][self.parcCount] = self.rankText2.get('1.0','end-1c')
            self.df.loc[:, ('GENNOTES')][self.parcCount] = self.notesText.get('1.0','end-1c')
            self.df.loc[:, ('CONNOTES')][self.parcCount] = self.contactText.get('1.0','end-1c')
        except:
            window.destroy()
            return
        
        nameRaw = self.inFile.split('.')[0]
        if 'annotated' not in nameRaw:
            outNameRaw = nameRaw + '_' + 'annotated.csv'
        
        if 'annotated' in nameRaw:
            if nameRaw[-1] == 'd':
                outNameRaw = nameRaw + '1' + '.csv'
            elif nameRaw[-1].isnumeric():
                outNameRaw = nameRaw[:-1] + str(int(nameRaw[-1])+1) + '.csv'     
        
        try:
            self.df = self.df.drop(['TAXADD','OWNERADD','Unnamed: 0'],axis=1)
        except:
            self.df = self.df.drop(['TAXADD','OWNERADD'],axis=1)
        self.df.to_csv(outNameRaw)

        window.destroy()
        
    def filePath(self):
        self.inFile = filedialog.askopenfilename(title = 'Select file', filetypes = (('CSV Files', '*.csv'),))
        
        self.inTextBox.configure(state='normal') #configures textbox for UI purposes
        self.inTextBox.delete(1.0, 'end')
        self.inTextBox.insert('end',self.inFile)
        self.inTextBox.configure(state='disabled')
        
    def outputPath(self):
        self.outPath = filedialog.askdirectory()

        self.outTextBox.configure(state='normal') #configures textbox for UI purposes
        self.outTextBox.delete(1.0, 'end')
        self.outTextBox.insert('end',self.outPath)
        self.outTextBox.configure(state='disabled')
        
    def loadCSV(self):
        try:
            if not self.inFile:
                messagebox.showinfo('Missing input','Please select an input file')
                return
        except:
            messagebox.showinfo('Missing input','Please select an input file')
            return
        
        self.df = pd.read_csv(self.inFile, index_col=False)
        
        #recast GIS_ACRES as float
        self.df['GIS_ACRES'] = self.df['GIS_ACRES'].astype(float)
                
        #cast these as strings, replace NA and NaN with blanks
        self.df['CLAYRANK1'] = self.df['CLAYRANK1'].astype(str)
        self.df['CLAYRANK2'] = self.df['CLAYRANK2'].astype(str)
        self.df['GENNOTES'] = self.df['GENNOTES'].astype(str)
        self.df['CONNOTES'] = self.df['CONNOTES'].astype(str)

        self.df['CLAYRANK1'] = self.df['CLAYRANK1'].replace('nan','')
        self.df['CLAYRANK2'] = self.df['CLAYRANK2'].replace('nan','')
        self.df['GENNOTES'] = self.df['GENNOTES'].replace('nan','')
        self.df['CONNOTES'] = self.df['CONNOTES'].replace('nan','')
        
        self.df[['CLAYRANK1', 'CLAYRANK2', 'GENNOTES', 'CONNOTES']] = self.df[['CLAYRANK1', 'CLAYRANK2', 'GENNOTES', 'CONNOTES']].fillna('')
        
        #now cast address fields as strings
        self.df['TAXPRNAME'] = self.df['TAXPRNAME'].astype(str)
        self.df['TAXPRLINE1'] = self.df['TAXPRLINE1'].astype(str)
        self.df['TAXPRCITY'] = self.df['TAXPRCITY'].astype(str)
        self.df['TAXPRSTATE'] = self.df['TAXPRSTATE'].astype(str)
        self.df['TAXPRZIP'] = self.df['TAXPRZIP'].astype(str)
        
        self.df['OWNERNAME'] = self.df['OWNERNAME'].astype(str)
        self.df['OWNERLINE1'] = self.df['OWNERLINE1'].astype(str)
        self.df['OWNERCITY'] = self.df['OWNERCITY'].astype(str)
        self.df['OWNERSTATE'] = self.df['OWNERSTATE'].astype(str)
        self.df['OWNERZIP'] = self.df['OWNERZIP'].astype(str)        
        
        #remove the .0 from the end of the zip fields when those fields exist
        self.df['TAXPRZIP'] = self.df['TAXPRZIP'].str[:5]
        self.df['OWNERZIP'] = self.df['OWNERZIP'].str[:5]

        #create and populate TAXADD and OWNERADD fields
        self.df['TAXADD'] = self.df['TAXPRNAME'] + '\n' + self.df['TAXPRLINE1'] + '\n' + self.df['TAXPRCITY'] + ', ' + self.df['TAXPRSTATE'] + ' ' + self.df['TAXPRZIP']
        
        #no zip and no name
        self.df['TAXADD'] = np.where(self.df['TAXPRZIP'].eq('nan') & self.df['TAXPRNAME'].eq('nan'), 
                                self.df['TAXPRLINE1'] + '\n' + self.df['TAXPRCITY'] + ', ' + self.df['TAXPRSTATE'],
                                self.df['TAXADD'])
        
        #no zip yes name
        self.df['TAXADD'] = np.where(self.df['TAXPRZIP'].eq('nan') & ~self.df['TAXPRNAME'].eq('nan'), 
                                self.df['TAXPRNAME'] + '\n' + self.df['TAXPRLINE1'] + '\n' + self.df['TAXPRCITY'] + ', ' + self.df['TAXPRSTATE'],
                                self.df['TAXADD'])
        
        #yes zip no name
        self.df['TAXADD'] = np.where(~self.df['TAXPRZIP'].eq('nan') & self.df['TAXPRNAME'].eq('nan'), 
                                self.df['TAXPRLINE1'] + '\n' + self.df['TAXPRCITY'] + ', ' + self.df['TAXPRSTATE'] + ' ' + self.df['TAXPRZIP'],
                                self.df['TAXADD'])
        
        #no city means not enough info
        self.df['TAXADD'] = np.where(self.df['TAXPRCITY'].eq('nan'), 'Taxpayer info missing', self.df['TAXADD'])
        
        #owneradd now
        self.df['OWNERADD'] = self.df['OWNERNAME'] + '\n' + self.df['OWNERLINE1'] + '\n' + self.df['OWNERCITY'] + ', ' + self.df['OWNERSTATE'] + ' ' + self.df['OWNERZIP']
        
        #no zip and no name        
        self.df['OWNERADD'] = np.where(self.df['OWNERZIP'].eq('nan') & self.df['OWNERNAME'].eq('nan'), 
                                self.df['OWNERLINE1'] + '\n' + self.df['OWNERCITY'] + ', ' + self.df['OWNERSTATE'],
                                self.df['OWNERADD'])
        
        #no zip yes name
        self.df['OWNERADD'] = np.where(self.df['OWNERZIP'].eq('nan') & ~self.df['OWNERNAME'].eq('nan'), 
                                self.df['OWNERNAME'] + '\n' + self.df['OWNERLINE1'] + '\n' + self.df['OWNERCITY'] + ', ' + self.df['OWNERSTATE'],
                                self.df['OWNERADD'])
        
        #yes zip no name
        self.df['OWNERADD'] = np.where(~self.df['OWNERZIP'].eq('nan') & self.df['OWNERNAME'].eq('nan'), 
                                self.df['OWNERLINE1'] + '\n' + self.df['OWNERCITY'] + ', ' + self.df['OWNERSTATE'] + ' ' + self.df['OWNERZIP'],
                                self.df['OWNERADD'])
        
        #no city means not enough info
        self.df['OWNERADD'] = np.where(self.df['OWNERCITY'].eq('nan'), 'Owner info missing', self.df['OWNERADD'])
        
        #populate GUI with first row data
        parcCountStr = '%s/%s' % (self.parcCount+1, len(self.df.index))
        
        try:
            parcIDCurrent = int(self.df.loc[:, ('PARCEL_ID')][self.parcCount])
        except:
            parcIDCurrent = self.df.loc[:, ('PARCEL_ID')][self.parcCount]

        ownerCurrent = self.df.loc[:, ('OWNERADD')][self.parcCount]
        taxCurrent = self.df.loc[:, ('TAXADD')][self.parcCount]
        sizeCurrent = round(self.df.loc[:, ('GIS_ACRES')][self.parcCount],2)
        countyCurrent = self.df.loc[:, ('COUNTY')][self.parcCount]
        
        self.countyIDBox.configure(state='normal')
        self.countyIDBox.delete(1.0, 'end')
        self.countyIDBox.insert('end', countyCurrent)
        self.countyIDBox.configure(state='disabled')

        self.parcNumBox.configure(state='normal')
        self.parcNumBox.delete(1.0, 'end')
        self.parcNumBox.insert('end', parcCountStr)
        self.parcNumBox.configure(state='disabled')

        self.parcIDBox.configure(state='normal')
        self.parcIDBox.delete(1.0, 'end')
        self.parcIDBox.insert('end', parcIDCurrent)
        self.parcIDBox.configure(state='disabled')

        self.ownerText.configure(state='normal')
        self.ownerText.delete(1.0, 'end')
        self.ownerText.insert('end', ownerCurrent)
        self.ownerText.configure(state='disabled')

        self.taxText.configure(state='normal')
        self.taxText.delete(1.0, 'end')
        self.taxText.insert('end', taxCurrent)
        self.taxText.configure(state='disabled')

        self.sizeText.configure(state='normal')
        self.sizeText.delete(1.0, 'end')
        self.sizeText.insert('end', sizeCurrent)
        self.sizeText.configure(state='disabled')
        
        #check for and populate existing rank/notes fields
        self.rankText.insert('end', self.df.loc[:, ('CLAYRANK1')][self.parcCount])
        self.notesText.insert('end', self.df.loc[:, ('GENNOTES')][self.parcCount])
        self.rankText2.insert('end', self.df.loc[:, ('CLAYRANK2')][self.parcCount])
        self.contactText.insert('end', self.df.loc[:, ('CONNOTES')][self.parcCount])
        
    def createWidgets2(self):
        ##grid construction, organized by row and column
        #row0
        inButton = tk.Button(self,text='Select input CSV file',
                            command=self.filePath).grid(row=0, column=0, sticky=tk.E)

        self.inTextBox = tk.Text(self, state='disabled', width=90, height=1)
        self.inTextBox.grid(row=0, column=1, columnspan=5, sticky=tk.W)

        #row1
        outputButton = tk.Button(self,text='Select output file directory',
                                command=self.outputPath).grid(row=1, column=0, sticky=tk.E)

        self.outTextBox = tk.Text(self, state='disabled', width=90, height=1)
        self.outTextBox.grid(row=1, column=1, columnspan=5, sticky=tk.W)

        #row2
        runButton = tk.Button(self, text='Load selected CSV',
                            command=self.loadCSV).grid(row=2, column=0, sticky=tk.W)

        nextButton = tk.Button(self, text='Next parcel',
                            command=self.nextParc).grid(row=2, column=1, sticky=tk.W)

        prevButton = tk.Button(self, text='Previous parcel',
                            command=self.prevParc).grid(row=2, column=2, sticky=tk.W)

        quitButton = tk.Button(self,text='Save and quit',
                            command=self.quitProg).grid(row=2, column=3, sticky=tk.W)

        #row3
        parcLabel = tk.Label(self, text='Parcel ID:')
        parcLabel.grid(row=3, column=0, sticky=tk.E, pady=(15,5))

        self.parcIDBox = tk.Text(self, state='disabled', width=20, height=1)
        self.parcIDBox.grid(row=3, column=1, pady=(15,5), sticky=tk.W)

        parcNumLabel = tk.Label(self, text='Parcel number/total:')
        parcNumLabel.grid(row=3, column=2, sticky=tk.E, pady=(15,5))

        self.parcNumBox = tk.Text(self, state='disabled', width=15, height=1)
        self.parcNumBox.grid(row=3, column=3, sticky=tk.W, pady=(15,5))
        
        countyIDLabel = tk.Label(self, text='County:')
        countyIDLabel.grid(row=3, column=4, sticky=tk.E, pady=(15,5))
        
        self.countyIDBox = tk.Text(self, state='disabled', width=15, height=1)
        self.countyIDBox.grid(row=3, column=5, sticky=tk.W, pady=(15,5))

        #row4
        notesLabel = tk.Label(self, text='General notes:')
        notesLabel.grid(row=4, column=2, sticky=tk.W)

        ownerLabel = tk.Label(self, text='Owner info:')
        ownerLabel.grid(row=4, column=4, sticky=tk.W)

        taxLabel = tk.Label(self, text='Taxpayer info:')
        taxLabel.grid(row=4, column=6, sticky=tk.W)

        #row5
        rankLabel = tk.Label(self, text='Clay\'s timber rank:')
        rankLabel.grid(row=5, column=0, sticky=tk.E)

        self.rankText = tk.Text(self, width=18, height=1)
        self.rankText.grid(row=5, column=1, sticky=tk.W)
        
        self.notesText = tk.Text(self, width=45, height=5)
        self.notesText.grid(row=5, column=2, columnspan=2, rowspan=5, sticky=tk.W)

        self.ownerText = tk.Text(self, state='disabled', width=30, height=5)
        self.ownerText.grid(row=5, column=4, columnspan=2, rowspan = 5, sticky=tk.W)

        self.taxText = tk.Text(self, state='disabled', width=30, height=5)
        self.taxText.grid(row=5, column=6, columnspan=2, rowspan = 5, sticky=tk.W)

        #row6
        rankLabel2 = tk.Label(self, text = 'Clay\'s complete rank:')
        rankLabel2.grid(row=6, column=0, sticky=tk.E)

        self.rankText2 = tk.Text(self, width=18, height=1)
        self.rankText2.grid(row=6, column=1, sticky=tk.W)

        #row7
        parcNavLabel = tk.Label(self, text='Navigate to parcel #:')
        parcNavLabel.grid(row=7, column=0, sticky=tk.E, pady=(10,0))

        self.parcNavText = tk.Text(self, width=15, height=1)
        self.parcNavText.grid(row=7, column=1, sticky=tk.W, pady=(10,0))

        #row8
        parcNavButton = tk.Button(self, text='Navigate to parcel',
                                command=self.parcNavigate).grid(row=8, column=0, sticky=tk.E)

        #row10
        contactLabel = tk.Label(self, text = 'Contact notes:')
        contactLabel.grid(row=10, column=2, sticky=tk.W)
        
        sizeLabel = tk.Label(self, text='Parcel size (acres):')
        sizeLabel.grid(row=10, column=4, sticky=tk.W, pady=(5,0))

        self.sizeText = tk.Text(self, state='disabled', width=16, height=1)
        self.sizeText.grid(row=10, column=5, sticky=tk.W, pady=(5,0))

        #row11
        self.contactText = tk.Text(self, width=45, height=5)
        self.contactText.grid(row=11, column=2, columnspan=2, rowspan=5, sticky=tk.W)

def main():
    #set up GUI
    global window
    window = tk.Tk()
    
    #set up tabs
    tabControl = ttk.Notebook(window)
    
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    
    tabControl.add(tab1, text='Filters')
    tabControl.add(tab2, text='Notes')
    
    tabControl.grid() #maybe switch this to .pack(expand=1, fill='both')
    
    #instantiate the frame classes
    tfilter = timberFilter(master = tab1)
    tfilter.grid() #maybe switch this to a .pack()
    
    csve = csvEdit(master = tab2)
    csve.grid() #maybe switch this to a .pack()
    
    #Main loop
    window.title('Timber filter')
    window.mainloop()

if __name__ == '__main__':
    main()