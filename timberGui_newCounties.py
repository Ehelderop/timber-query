#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      eheldero
#
# Created:     03/05/2018
# Copyright:   (c) eheldero 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import Tkinter as tk
import tkFileDialog
import os
import gdal
import ogr
import shutil
import glob
from dbfpy import dbf
import csv
import datetime
import tkMessageBox

def main():
    master = tk.Tk()

    #filter variables
    owner = tk.IntVar(master)
    privOwner = tk.IntVar(master)
    accessDist = tk.IntVar(master)
    waterFeat = tk.IntVar(master)

    def dbfFilter():
        ##check for infile and outfile stuff
        global inPath
        global outPath

        try:
            if not inPath:
                tkMessageBox.showinfo('Missing input','Please select the county input file directory')
                return
        except:
            tkMessageBox.showinfo('Missing input','Please select the county input file directory')
            return

        try:
            if not outPath:
                tkMessageBox.showinfo('Missing output','Please select the output file directory')
                return
        except:
            tkMessageBox.showinfo('Missing output','Please select the output file directory')
            return

        ##set working directory to chosen inpath
        os.chdir(inPath)

        ##first, create a copy of the .shp since it will be edited directly
        #delete previous copy first
        coCopies = glob.glob('*_copy.*')
        for f in coCopies:
            os.remove(f)

        #now, copy all the different files that compose a shp
        coShps = os.listdir(inPath)

        for f in coShps:
            fl = f.split('.')
            if len(fl) == 2:
                nf = fl[0]+'_copy.'+fl[1]
                shutil.copy2(f,nf)
            if len(fl) == 3:
                nf = fl[0]+'_copy.'+fl[1]+'.'+fl[2]
                shutil.copy2(f,nf)
        shpPath = inPath + '/' + glob.glob('*_copy.shp')[0]
        shpName = fl[0]

        ##open copied shp w/ OGR
        driver = ogr.GetDriverByName('ESRI Shapefile')
        dataSource = driver.Open(shpPath, 1)
        layer = dataSource.GetLayer()

        ##attribute filter criteria
        parcelSize = e1.get()
        parcelVal = e2.get()
        decidPerc = e3.get()
        evergPerc = e4.get()

        layer.ResetReading()
        for feature in layer:
            if shpName not in ['Island','SanJuan']:
                tu = feature.GetFieldAsString('PRIVATE')

                if privOwner.get() == 1:
                    if float(tu) == 0:
                        layer.DeleteFeature(feature.GetFID())

            if shpName not in ['Clallam','Jefferson']:
                ts = feature.GetFieldAsString('OWNERSTATE')

                if owner.get() == 1:
                    if ts == 'WA':
                        layer.DeleteFeature(feature.GetFID())
                if owner.get() == 2:
                    if ts != 'WA':
                        layer.DeleteFeature(feature.GetFID())

            dummyAccess = feature.GetFieldAsString('ROAD')
            dummyWater = feature.GetFieldAsString('WATER')
            dummyBoth = feature.GetFieldAsString('ROADWATER')

            if accessDist.get() == 1 and waterFeat.get() == 0:
                if float(dummyAccess) == 0:
                    layer.DeleteFeature(feature.GetFID())

            if accessDist.get() == 0 and waterFeat.get() == 1:
                if float(dummyWater) == 0:
                    layer.DeleteFeature(feature.GetFID())

            if accessDist.get() == 1 and waterFeat.get() == 1:
                if float(dummyBoth) == 0:
                    layer.DeleteFeature(feature.GetFID())

            if feature.GetFieldAsDouble('GIS_ACRES') < float(parcelSize):
                layer.DeleteFeature(feature.GetFID())

            if feature.GetFieldAsDouble('MKRAT') < float(parcelVal):
                layer.DeleteFeature(feature.GetFID())

            if feature.GetFieldAsDouble('DECIDPER') < float(decidPerc):
                layer.DeleteFeature(feature.GetFID())

            if feature.GetFieldAsDouble('EVERGPER') < float(evergPerc):
                layer.DeleteFeature(feature.GetFID())

        dataSource.ExecuteSQL('REPACK ' + layer.GetName())
        del dataSource

        ##generate output CSV of acceptable rows
        #open results dbf and generate CSV file name
        now = datetime.datetime.now()
        todDate = str(now.year) + '_' + str(now.month) + '_' + str(now.day)
        csvName = shpName + '_' + todDate + '_' + 'recParcels.csv'
        csvPath = outPath + '/' + csvName

        dbfName1 = shpPath.split('/')[-1]
        dbfName = dbfName1.split('.')[0] + '.dbf'

        dbfPath = inPath + '/' + dbfName

        with open(csvPath, 'wb') as csvfile:
            in_db = dbf.Dbf(dbfPath, ignoreErrors=True)
            out_csv = csv.writer(csvfile)
            names = []
            for field in in_db.header.fields:
                names.append(field.name)
            out_csv.writerow(names)
            for rec in in_db:
                out_csv.writerow(rec.fieldData)
            in_db.close()

    def filePath(): #location of input files - and only input files!
        global inPath
        tempVar = tkFileDialog.askdirectory()
        inPath = tempVar

        inTextBox.configure(state='normal') #configures textbox for UI purposes
        inTextBox.delete(1.0, 'end')
        inTextBox.insert('end',inPath)
        inTextBox.configure(state='disabled')

    def outputPath(): #specifies desired location of output file
        global outPath
        tempVar = tkFileDialog.askdirectory()
        outPath = tempVar

        outTextBox.configure(state='normal') #configures textbox for UI purposes
        outTextBox.delete(1.0, 'end')
        outTextBox.insert('end',outPath)
        outTextBox.configure(state='disabled')

    def quitProg():
        master.destroy()

    ##grid placement in order

    #entries: e1 = acreage, e2 = value ratio
    #e3 = deciduous coverage, e4 = evergreen coverage

    #row0
    inButton = tk.Button(master,text='Select county input file directory',
                            command=filePath).grid(row=0, column=0, sticky=tk.E)

    inTextBox = tk.Text(master, state='disabled', width=70, height=1)
    inTextBox.grid(row=0, column=1, sticky=tk.W)

    #row1
    outputButton = tk.Button(master,text='Select output file directory',
                                command=outputPath).grid(row=1, column=0, sticky=tk.E)

    outTextBox = tk.Text(master, state='disabled', width=70, height=1)
    outTextBox.grid(row=1, column=1, columnspan=3, sticky=tk.W)

    #row2
    ownerLabel = tk.Label(master,
                            text=('Owner status (private owners exclude governments, '
                            'corporations, and other organizations)'),
                            font='Helvetica 10 bold').grid(row=2, column=0, sticky=tk.W, columnspan=3)

    #row3
    r1 = tk.Radiobutton(master,
                        text='Out-of-state owner only (Note: This filter will not work for Clallam or Jefferson county due to missing data)',
                        variable = owner,
                        value = 1).grid(row=3, column=0, sticky=tk.W)

    #row4
    r2 = tk.Radiobutton(master,
                        text='In-state owner only (Note: This filter will not work for Clallam or Jefferson county due to missing data)',
                        variable = owner,
                        value = 2).grid(row=4, column=0, sticky=tk.W)

    #row5
    r3 = tk.Radiobutton(master,
                        text='All owners (Note: This filter will not work for Clallam or Jefferson county due to missing data)',
                        variable = owner,
                        value = 3).grid(row=5, column=0, sticky=tk.W)

    #row6
    c3 = tk.Checkbutton(master,
                        text='Private owner only (Note: This filter will not work for San Juan or Island County due to missing data)',
                        variable=privOwner).grid(row=6, column=0, sticky=tk.W)

    #row7
    accessVar = tk.Label(master,
                            text=('Parcel access'),
                            font='Helvetica 10 bold').grid(row=7, column=0, sticky=tk.W)

    #row8
    c4 = tk.Checkbutton(master,
                        text='Parcels adjacent to roads only',
                        variable=accessDist).grid(row=8, column=0, sticky=tk.W)

    #row9
    c5 = tk.Checkbutton(master,
                        text='Parcels with no water features',
                        variable=waterFeat).grid(row=9, column=0, sticky=tk.W)

    #row10
    parcelSize = tk.Label(master,
                            text=('Minimum parcel size (minimum of 5, in acres):'),
                            font='Helvetica 10 bold').grid(row=10, column=0, sticky=tk.E)

    e1 = tk.Entry(master)
    e1.insert(10, '5')
    e1.grid(row=10, column=1, sticky=tk.W)

    #row11
    parcelVal = tk.Label(master,
                            text=('Land to total value ratio (0 to 1):'),
                            font='Helvetica 10 bold').grid(row=11, column=0, sticky=tk.E)

    e2 = tk.Entry(master)
    e2.insert(10, '.75')
    e2.grid(row=11, column=1, sticky=tk.W)

    #row13
    decidVar = tk.Label(master,
                            text=('Deciduous percent coverage per parcel (0 to 100):'),
                            font='Helvetica 10 bold').grid(row=13, column=0, sticky=tk.E)

    e3 = tk.Entry(master)
    e3.insert(10, '15')
    e3.grid(row=13, column=1, sticky=tk.W)

    #row14
    evergVar = tk.Label(master,
                            text=('Evergreen percent coverage per parcel (0 to 100):'),
                            font='Helvetica 10 bold').grid(row=14, column=0, sticky=tk.E)

    e4 = tk.Entry(master)
    e4.insert(10, '15')
    e4.grid(row=14, column=1, sticky=tk.W)

    #row15
    runButton = tk.Button(master, text='Run with selected filters',
                            command=dbfFilter).grid(row=15, column=0, sticky=tk.W)

    quitButton = tk.Button(master,text='Quit',
                            command=quitProg).grid(row=15, column=1, sticky=tk.W)

    master.title('Timber Filter')
    master.mainloop()

if __name__ == '__main__':
    main()