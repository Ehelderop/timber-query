#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      eheldero
#
# Created:     13/06/2018
# Copyright:   (c) eheldero 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import pandas as pd
import Tkinter as tk
import tkFileDialog
import sys
import os
import datetime
import tkMessageBox
import selenium
from selenium import webdriver
import time
import selenium.webdriver.common.keys
from selenium.webdriver.common.keys import Keys
import warnings
warnings.simplefilter("ignore")

def main():
    global d
    global options

    master = tk.Tk()

    def onlineParc():
        global parcCount
        global df

        try:
            if df.empty:
                tkMessageBox.showinfo('Load CSV','Please load the CSV before loading a parcel.')
        except:
            tkMessageBox.showinfo('Load CSV','Please load the CSV before loading a parcel.')
            return

        ##Need a block of code for each county

        currentParcel = str(df.loc[:, ('PARCEL_ID')][parcCount])
        
        if shpName == "SanJuan":
            currentParcel = str.split(currentParcel,'.')[0]
            d.get('https://parcel.sanjuanco.com/PropertyAccess/?cid=0')
            
            #find the parcel entry field
            e = d.find_element_by_xpath('//*[@id="propertySearchOptions_geoid"]')
            time.sleep(1.0)
            e.send_keys(currentParcel)
            time.sleep(0.500)
            e.send_keys(Keys.RETURN)

        if shpName == "Snohomish":
            d.get('http://gis.snoco.org/maps/property/viewer.htm')

            #find the parcel entry field
            d.switch_to.frame(d.find_element_by_name('ToolFrame'))
            time.sleep(2.0)

            e = d.find_element_by_name('searchPID')
            time.sleep(0.500)
            e.send_keys(currentParcel)
            time.sleep(0.500)
            e.send_keys(Keys.RETURN)

        if shpName == "Skagit":
            d.get('https://www.skagitcounty.net/Search/Property/')
            time.sleep(1.0)

            #click parcel number radio button
            radioe = d.find_element_by_xpath("//body//div[@class='container_12']//div//div//div//div[1]//input[2]")
            time.sleep(1.0)
            radioe.click()
            time.sleep(0.500)

            #find parcel entry field
            e = d.find_element_by_xpath("//input[@id='tbAuto']")
            time.sleep(0.500)
            e.send_keys(currentParcel)
            time.sleep(0.500)
            e.send_keys(Keys.RETURN)

        if shpName == "King":
            if len(currentParcel) == 9:
                fixedParc = '0'+currentParcel
            if len(currentParcel) == 10:
                fixedParc = currentParcel

            d.get('https://gismaps.kingcounty.gov/parcelviewer2/')
            time.sleep(1.0)

            d.find_element_by_xpath("//span[@class='dijitReset dijitInline dijitSelectLabel'][contains(text(),'Address')]").click()
            time.sleep(0.500)
            d.find_element_by_xpath("//tr[@id='dijit_MenuItem_6']").click()
            time.sleep(0.500)

            e = d.find_element_by_xpath("//input[@id='searchInput']")
            time.sleep(0.500)
            e.send_keys(fixedParc)
            time.sleep(0.500)
            e.send_keys(Keys.RETURN)


        if shpName == "Jefferson":
            if len(currentParcel) == 9:
                fixedParc = currentParcel
            if len(currentParcel) == 8:
                fixedParc = '0'+currentParcel
            if len(currentParcel) == 7:
                fixedParc = '00'+currentParcel

            d.get('https://www.co.jefferson.wa.us/954/Property-Tax-Parcel-Search')
            time.sleep(1.0)

            #need to switch iframe
            d.switch_to.frame(d.find_element_by_xpath("//div[@id='customHtml1185f5c6-bada-4f65-ac4a-d7e6273ec92d']//div//iframe"))
            time.sleep(0.500)

            e = d.find_element_by_xpath("//*[@id='TBParcel']")
            time.sleep(0.500)
            e.send_keys(fixedParc)
            time.sleep(0.500)
            e.send_keys(Keys.RETURN)

        if shpName == "Island":
            dfURL = str(df['SMARTGOV_U'][parcCount])

            try:
                d.get(dfURL)
                time.sleep(2.0)
            except:
                tkMessageBox.showinfo('Missing URL','Dataset is missing URL for this parcel.')
                return

        if shpName == "Clallam":
            dfURL = str(df['PACS_LINK'][parcCount])

            try:
                d.get(dfURL)
                time.sleep(2.0)
            except:
                tkMessageBox.showinfo('Missing URL','Dataset is missing URL for this parcel.')
                return

    def loadCSV():
        ##Use Pandas for easier csv editing
        global df
        global parcCount
        parcCount=0

        df = pd.read_csv(inFile,index_col=False)

        #cast these as strings
        df['P_RATING1'] = df['P_RATING1'].astype(str)
        df['P_RATING2'] = df['P_RATING2'].astype(str)
        df['P_NOTES1'] = df['P_NOTES1'].astype(str)
        df['P_NOTES2'] = df['P_NOTES2'].astype(str)

        df['P_RATING1'] = df['P_RATING1'].replace('nan','')
        df['P_RATING2'] = df['P_RATING2'].replace('nan','')
        df['P_NOTES1'] = df['P_NOTES1'].replace('nan','')
        df['P_NOTES2'] = df['P_NOTES2'].replace('nan','')

        #create owner and tax fields
        if shpName == "SanJuan":
            try:
                df['OWNERZIP'] = df['OWNERZIP'].astype(str)
                df['OWNERZIP'] = df['OWNERZIP'].replace('nan','')
                df['OWNERZIP'] = df['OWNERZIP'].str.split('.', n=1, expand=True)[0]
                df['OWNERZIP'] = df['OWNERZIP'].replace('0','')

                df['OWNERSTATE'] = df['OWNERSTATE'].astype(str)
                df['OWNERSTATE'] = df['OWNERSTATE'].replace('nan','')

                df['OWNERCITY'] = df['OWNERCITY'].astype(str)
                df['OWNERCITY'] = df['OWNERCITY'].replace('nan','')

                df['OWNERLINE1'] = df['OWNERLINE1'].astype(str)
                df['OWNERLINE1'] = df['OWNERLINE1'].replace('nan','')

                df['OWNERADD'] = 'Owner name unavailable' + '\n' + df['OWNERLINE1'] + '\n' + df['OWNERCITY'] + ', ' + df['OWNERSTATE'] + ' ' + df['OWNERZIP']
            except:
                df['OWNERADD'] = 'Owner info missing for\nthis county.'

            df['TAXADD'] = 'Taxpayer info missing for\nthis county.'

        if shpName not in ["Jefferson","SanJuan"]:
            try:
                df['OWNERZIP'] = df['OWNERZIP'].astype(str)
                df['OWNERZIP'] = df['OWNERZIP'].replace('nan','')
                df['OWNERZIP'] = df['OWNERZIP'].str.split('.', n=1, expand=True)[0]
                df['OWNERZIP'] = df['OWNERZIP'].replace('0','')

                df['OWNERSTATE'] = df['OWNERSTATE'].astype(str)
                df['OWNERSTATE'] = df['OWNERSTATE'].replace('nan','')

                df['OWNERCITY'] = df['OWNERCITY'].astype(str)
                df['OWNERCITY'] = df['OWNERCITY'].replace('nan','')

                df['OWNERLINE1'] = df['OWNERLINE1'].astype(str)
                df['OWNERLINE1'] = df['OWNERLINE1'].replace('nan','')

                df['OWNERADD'] = df['OWNERNAME'] + '\n' + df['OWNERLINE1'] + '\n' + df['OWNERCITY'] + ', ' + df['OWNERSTATE'] + ' ' + df['OWNERZIP']
            except:
                df['OWNERADD'] = 'Owner info missing for\nthis county.'

            try:
                df['TAXPRZIP'] = df['TAXPRZIP'].astype(str)
                df['TAXPRZIP'] = df['TAXPRZIP'].replace('nan','')
                df['TAXPRZIP'] = df['TAXPRZIP'].str.split('.', n=1, expand=True)[0]
                df['TAXPRZIP'] = df['TAXPRZIP'].replace('0','')

                df['TAXPRSTATE'] = df['TAXPRSTATE'].astype(str)
                df['TAXPRSTATE'] = df['TAXPRSTATE'].replace('nan','')

                df['TAXPRCITY'] = df['TAXPRCITY'].astype(str)
                df['TAXPRCITY'] = df['TAXPRCITY'].replace('nan','')

                df['TAXPRLINE1'] = df['TAXPRLINE1'].astype(str)
                df['TAXPRLINE1'] = df['TAXPRLINE1'].replace('nan','')

                df['TAXADD'] = df['TAXPRNAME'] + '\n' +  df['TAXPRLINE1'] + '\n' +  df['TAXPRCITY'] + ', ' + df['TAXPRSTATE'] + ' ' + df['TAXPRZIP']
            except:
                df['TAXADD'] = 'Taxpayer info missing for\nthis county.'

        if shpName == "Jefferson":
            df['OWNERADD'] = df['OWNERNAME'] + "\nNo address info\nprovided."
            df['TAXADD'] = "Taxpayer info missing for\nthis county."

        #populate first row's data in the GUI
        parcCountStr = '%s/%s' % (parcCount+1, len(df.index))
        parcIDCurrent = df.loc[:, ('PARCEL_ID')][parcCount]
        ownerCurrent = df.loc[:, ('OWNERADD')][parcCount]
        taxCurrent = df.loc[:, ('TAXADD')][parcCount]
        sizeCurrent = round(df.loc[:, ('GIS_ACRES')][parcCount],2)

        parcNumBox.configure(state='normal')
        parcNumBox.delete(1.0, 'end')
        parcNumBox.insert('end', parcCountStr)
        parcNumBox.configure(state='disabled')

        parcIDBox.configure(state='normal')
        parcIDBox.delete(1.0, 'end')
        parcIDBox.insert('end', parcIDCurrent)
        parcIDBox.configure(state='disabled')

        ownerText.configure(state='normal')
        ownerText.delete(1.0, 'end')
        ownerText.insert('end', ownerCurrent)
        ownerText.configure(state='disabled')

        taxText.configure(state='normal')
        taxText.delete(1.0, 'end')
        taxText.insert('end', taxCurrent)
        taxText.configure(state='disabled')

        sizeText.configure(state='normal')
        sizeText.delete(1.0, 'end')
        sizeText.insert('end', sizeCurrent)
        sizeText.configure(state='disabled')

    def prevParc():
        global parcCount
        global df

        try:
            if df.empty:
                tkMessageBox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
        except:
            tkMessageBox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
            return

        #save typed results
        df.loc[:, ('P_RATING1')][parcCount] = rankText.get('1.0','end-1c')
        df.loc[:, ('P_RATING2')][parcCount] = rankText2.get('1.0','end-1c')
        df.loc[:, ('P_NOTES1')][parcCount] = notesText.get('1.0','end-1c')
        df.loc[:, ('P_NOTES2')][parcCount] = contactText.get('1.0','end-1c')

        #clear fields for next entry
        rankText.delete(1.0, 'end')
        notesText.delete(1.0, 'end')
        rankText2.delete(1.0, 'end')
        contactText.delete(1.0, 'end')

        #count stuff for parcel ID and number
        parcCount = parcCount-1

        if parcCount < 0:
            parcCount = len(df.index) + parcCount

        if parcCount >= len(df.index):
            parcCount = len(df.index) - parcCount

        parcCountStr = '%s/%s' % (parcCount+1, len(df.index))
        parcIDCurrent = df.loc[:, ('PARCEL_ID')][parcCount]
        ownerCurrent = df.loc[:, ('OWNERADD')][parcCount]
        taxCurrent = df.loc[:, ('TAXADD')][parcCount]
        sizeCurrent = round(df.loc[:, ('GIS_ACRES')][parcCount],2)

        parcNumBox.configure(state='normal')
        parcNumBox.delete(1.0, 'end')
        parcNumBox.insert('end', parcCountStr)
        parcNumBox.configure(state='disabled')

        parcIDBox.configure(state='normal')
        parcIDBox.delete(1.0, 'end')
        parcIDBox.insert('end', parcIDCurrent)
        parcIDBox.configure(state='disabled')

        ownerText.configure(state='normal')
        ownerText.delete(1.0, 'end')
        ownerText.insert('end', ownerCurrent)
        ownerText.configure(state='disabled')

        taxText.configure(state='normal')
        taxText.delete(1.0, 'end')
        taxText.insert('end', taxCurrent)
        taxText.configure(state='disabled')

        sizeText.configure(state='normal')
        sizeText.delete(1.0, 'end')
        sizeText.insert('end', sizeCurrent)
        sizeText.configure(state='disabled')

        #check for existing notes/ratings
        rankText.insert('end', df.loc[:, ('P_RATING1')][parcCount])
        notesText.insert('end', df.loc[:, ('P_NOTES1')][parcCount])
        rankText2.insert('end', df.loc[:, ('P_RATING2')][parcCount])
        contactText.insert('end', df.loc[:, ('P_NOTES2')][parcCount])

    def nextParc():
        global parcCount
        global df

        try:
            if df.empty:
                tkMessageBox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
        except:
            tkMessageBox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
            return

        #save typed results
        df.loc[:, ('P_RATING1')][parcCount] = rankText.get('1.0','end-1c')
        df.loc[:, ('P_RATING2')][parcCount] = rankText2.get('1.0','end-1c')
        df.loc[:, ('P_NOTES1')][parcCount] = notesText.get('1.0','end-1c')
        df.loc[:, ('P_NOTES2')][parcCount] = contactText.get('1.0','end-1c')

        #clear fields for next entry
        rankText.delete(1.0, 'end')
        notesText.delete(1.0, 'end')
        rankText2.delete(1.0, 'end')
        contactText.delete(1.0, 'end')

        #count stuff for parcel ID and number
        parcCount = parcCount+1

        if parcCount < 0:
            parcCount = len(df.index) + parcCount

        if parcCount >= len(df.index):
            parcCount = len(df.index) - parcCount

        parcCountStr = '%s/%s' % (parcCount+1, len(df.index))
        parcIDCurrent = df.loc[:, ('PARCEL_ID')][parcCount]
        ownerCurrent = df.loc[:, ('OWNERADD')][parcCount]
        taxCurrent = df.loc[:, ('TAXADD')][parcCount]
        sizeCurrent = round(df.loc[:, ('GIS_ACRES')][parcCount],2)

        parcNumBox.configure(state='normal')
        parcNumBox.delete(1.0, 'end')
        parcNumBox.insert('end', parcCountStr)
        parcNumBox.configure(state='disabled')

        parcIDBox.configure(state='normal')
        parcIDBox.delete(1.0, 'end')
        parcIDBox.insert('end', parcIDCurrent)
        parcIDBox.configure(state='disabled')

        ownerText.configure(state='normal')
        ownerText.delete(1.0, 'end')
        ownerText.insert('end', ownerCurrent)
        ownerText.configure(state='disabled')

        taxText.configure(state='normal')
        taxText.delete(1.0, 'end')
        taxText.insert('end', taxCurrent)
        taxText.configure(state='disabled')

        sizeText.configure(state='normal')
        sizeText.delete(1.0, 'end')
        sizeText.insert('end', sizeCurrent)
        sizeText.configure(state='disabled')

        #check for existing notes/ratings
        rankText.insert('end', df.loc[:, ('P_RATING1')][parcCount])
        notesText.insert('end', df.loc[:, ('P_NOTES1')][parcCount])
        rankText2.insert('end', df.loc[:, ('P_RATING2')][parcCount])
        contactText.insert('end', df.loc[:, ('P_NOTES2')][parcCount])

    def parcNavigate():
        global parcCount
        global df

        try:
            if df.empty:
                tkMessageBox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
        except:
            tkMessageBox.showinfo('Load CSV','Please load the CSV before navigating through parcels.')
            return

        newParc = int(parcNavText.get('1.0', 'end-1c'))

        #make sure entered value is valid
        if newParc < 1 or newParc > len(df.index):
            tkMessageBox.showinfo('Invalid parcel number','Make sure parcel number is between 1 and the maximum parcel number for this CSV.')
            parcNavText.delete(1.0, 'end')
            return

        #save typed results
        df.loc[:, ('P_RATING1')][parcCount] = rankText.get('1.0','end-1c')
        df.loc[:, ('P_RATING2')][parcCount] = rankText2.get('1.0','end-1c')
        df.loc[:, ('P_NOTES1')][parcCount] = notesText.get('1.0','end-1c')
        df.loc[:, ('P_NOTES2')][parcCount] = contactText.get('1.0','end-1c')

        #clear fields for next entry
        rankText.delete(1.0, 'end')
        notesText.delete(1.0, 'end')
        rankText2.delete(1.0, 'end')
        contactText.delete(1.0, 'end')

        #set new parcCount to entered value
        parcCount = newParc-1
        parcNavText.delete(1.0, 'end')

        parcCountStr = '%s/%s' % (parcCount+1, len(df.index))
        parcIDCurrent = df.loc[:, ('PARCEL_ID')][parcCount]
        ownerCurrent = df.loc[:, ('OWNERADD')][parcCount]
        taxCurrent = df.loc[:, ('TAXADD')][parcCount]
        sizeCurrent = round(df.loc[:, ('GIS_ACRES')][parcCount],2)

        parcNumBox.configure(state='normal')
        parcNumBox.delete(1.0, 'end')
        parcNumBox.insert('end', parcCountStr)
        parcNumBox.configure(state='disabled')

        parcIDBox.configure(state='normal')
        parcIDBox.delete(1.0, 'end')
        parcIDBox.insert('end', parcIDCurrent)
        parcIDBox.configure(state='disabled')

        ownerText.configure(state='normal')
        ownerText.delete(1.0, 'end')
        ownerText.insert('end', ownerCurrent)
        ownerText.configure(state='disabled')

        taxText.configure(state='normal')
        taxText.delete(1.0, 'end')
        taxText.insert('end', taxCurrent)
        taxText.configure(state='disabled')

        sizeText.configure(state='normal')
        sizeText.delete(1.0, 'end')
        sizeText.insert('end', sizeCurrent)
        sizeText.configure(state='disabled')

        rankText.insert('end', df.loc[:, ('P_RATING1')][parcCount])
        notesText.insert('end', df.loc[:, ('P_NOTES1')][parcCount])
        rankText2.insert('end', df.loc[:, ('P_RATING2')][parcCount])
        contactText.insert('end', df.loc[:, ('P_NOTES2')][parcCount])

    def filePath(): #location of input CSV
        global inFile
        global shpName
        tempVar = tkFileDialog.askopenfilename()
        inFile = tempVar
        shpName = str(inFile.split('/')[-1].split('_')[0])

        inTextBox.configure(state='normal') #configures textbox for UI purposes
        inTextBox.delete(1.0, 'end')
        inTextBox.insert('end',inFile)
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
        global outPath
        global df

        try:
            if not outPath:
                pass
        except:
            userQuit = tkMessageBox.askyesno('Warning','CSV cannot be saved without an output path selected.\nQuit without saving?')
            if userQuit == False:
                return
            if userQuit == True:
                master.destroy()
                return

        #save current fields (just like next/prev buttons)
        try:
            df.loc[:, ('P_RATING1')][parcCount] = rankText.get('1.0','end-1c')
            df.loc[:, ('P_RATING2')][parcCount] = rankText2.get('1.0','end-1c')
            df.loc[:, ('P_NOTES1')][parcCount] = notesText.get('1.0','end-1c')
            df.loc[:, ('P_NOTES2')][parcCount] = contactText.get('1.0','end-1c')
        except:
            master.destroy()
            return

        now = datetime.datetime.now()
        todDate = str(now.year) + '_' + str(now.month) + '_' + str(now.day)
        outNameRaw = shpName + '_' + todDate + '_parcelNotes.csv'
        outName = outPath + '/' + outNameRaw
        try:
            df = df.drop(['TAXADD','OWNERADD','Unnamed: 0'],axis=1)
        except:
            df = df.drop(['TAXADD','OWNERADD'],axis=1)
        df.to_csv(outName)

        master.destroy()

    ##grid construction, organized by row and column
    #row0
    inButton = tk.Button(master,text='Select input CSV file',
                            command=filePath).grid(row=0, column=0, sticky=tk.E)

    inTextBox = tk.Text(master, state='disabled', width=90, height=1)
    inTextBox.grid(row=0, column=1, columnspan=5, sticky=tk.W)

    #row1
    outputButton = tk.Button(master,text='Select output file directory',
                                command=outputPath).grid(row=1, column=0, sticky=tk.E)

    outTextBox = tk.Text(master, state='disabled', width=90, height=1)
    outTextBox.grid(row=1, column=1, columnspan=5, sticky=tk.W)

    #row2
    runButton = tk.Button(master, text='Load selected CSV',
                            command=loadCSV).grid(row=2, column=0, sticky=tk.W)

    nextButton = tk.Button(master, text='Next parcel',
                            command=nextParc).grid(row=2, column=1, sticky=tk.W)

    prevButton = tk.Button(master, text='Previous parcel',
                            command=prevParc).grid(row=2, column=2, sticky=tk.W)

    onlineButton = tk.Button(master, text='Open parcel page',
                                command=onlineParc).grid(row=2, column=3, sticky=tk.W)

    quitButton = tk.Button(master,text='Save and quit',
                            command=quitProg).grid(row=2, column=4, sticky=tk.W)

    #row3
    parcLabel = tk.Label(master, text='Parcel ID:')
    parcLabel.grid(row=3, column=0, sticky=tk.E, pady=(15,5))

    parcIDBox = tk.Text(master, state='disabled', width=20, height=1)
    parcIDBox.grid(row=3, column=1, pady=(15,5), sticky=tk.W)

    parcNumLabel = tk.Label(master, text='Parcel number/total:')
    parcNumLabel.grid(row=3, column=2, sticky=tk.E, pady=(15,5))

    parcNumBox = tk.Text(master, state='disabled', width=15, height=1)
    parcNumBox.grid(row=3, column=3, sticky=tk.W, pady=(15,5))

    #row4
    notesLabel = tk.Label(master, text='General notes:')
    notesLabel.grid(row=4, column=2, sticky=tk.W)

    ownerLabel = tk.Label(master, text='Owner info:')
    ownerLabel.grid(row=4, column=4, sticky=tk.W)

    taxLabel = tk.Label(master, text='Taxpayer info:')
    taxLabel.grid(row=4, column=6, sticky=tk.W)

    #row5
    rankLabel = tk.Label(master, text='Clay\'s timber rank:')
    rankLabel.grid(row=5, column=0, sticky=tk.E)

    rankText = tk.Text(master, width=18, height=1)
    rankText.grid(row=5, column=1, sticky=tk.W)

    notesText = tk.Text(master, width=45, height=5)
    notesText.grid(row=5, column=2, columnspan=2, rowspan=5, sticky=tk.W)

    ownerText = tk.Text(master, state='disabled', width=30, height=5)
    ownerText.grid(row=5, column=4, columnspan=2, rowspan = 5, sticky=tk.W)

    taxText = tk.Text(master, state='disabled', width=30, height=5)
    taxText.grid(row=5, column=6, columnspan=2, rowspan = 5, sticky=tk.W)

    #row6
    rankLabel2 = tk.Label(master, text = 'Clay\'s complete rank:')
    rankLabel2.grid(row=6, column=0, sticky=tk.E)

    rankText2 = tk.Text(master, width=18, height=1)
    rankText2.grid(row=6, column=1, sticky=tk.W)

    #row7
    parcNavLabel = tk.Label(master, text='Navigate to parcel #:')
    parcNavLabel.grid(row=7, column=0, sticky=tk.E, pady=(10,0))

    parcNavText = tk.Text(master, width=15, height=1)
    parcNavText.grid(row=7, column=1, sticky=tk.W, pady=(10,0))

    #row8
    parcNavButton = tk.Button(master, text='Navigate to parcel',
                                command=parcNavigate).grid(row=8, column=0, sticky=tk.E)

    #row10
    contactLabel = tk.Label(master, text = 'Contact notes:')
    contactLabel.grid(row=10, column=2, sticky=tk.W)

    sizeLabel = tk.Label(master, text='Parcel size (acres):')
    sizeLabel.grid(row=10, column=4, sticky=tk.W, pady=(5,0))

    sizeText = tk.Text(master, state='disabled', width=16, height=1)
    sizeText.grid(row=10, column=5, sticky=tk.W, pady=(5,0))

    #row11
    contactText = tk.Text(master, width=45, height=5)
    contactText.grid(row=11, column=2, columnspan=2, rowspan=5, sticky=tk.W)

    master.title('CSV Editor')
    master.mainloop()

if __name__ == '__main__':
    global options
    global d
    
    options = webdriver.ChromeOptions()
    
    chPath = os.path.abspath(os.path.dirname(sys.argv[0]))+'\\'+'chromedriver.exe'
    
    d = webdriver.Chrome(executable_path=chPath, chrome_options=options)
    d.get('https://www.google.com')

    main()
