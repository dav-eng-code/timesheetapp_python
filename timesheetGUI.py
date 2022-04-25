from tkinter import *
from tkinter import ttk
import datetime
import dateutil
import time

from pandas.core import frame

import projectsData
import math

bgColour1='SlateGray4'
fgColour1='white'
bgColour2='gray98'
fgColour2='gray40'
bgColour2s='SlateGray3' #'LightCyan3
bgColour3='gray95'
bgActColour3='gray90'


main_window = Tk()
main_window.title('Time Entry Application')
main_window.configure(bg=bgColour1)
main_window.pack_propagate(True)
#main_window.minsize(width=800,height=500)

headerFr = Frame(main_window,bg=bgColour1)
headerFr.pack(fill='x')

tableDisplayFr=Frame(highlightthickness=10,highlightbackground=bgColour1)
tableDisplayFr.pack(fill='x',pady=5)

tabButtonsFr=Frame(tableDisplayFr,bg=bgColour1)
tabButtonsFr.pack(fill='x')
entriesTableFr = Frame(tableDisplayFr,background=bgColour2,height=10)
entriesTableFr.pack(fill='x')
sortedEntriesTableFr=Frame(tableDisplayFr,background=bgColour2s,height=10)

frequentItemsFr = Frame(bg=bgColour1)
frequentItemsFr.pack(fill='x',pady=10)
frequentItemsFr.columnconfigure(0,minsize=400)
freqProjButtons=Frame(frequentItemsFr,bg=bgColour1)
freqItemsButtons=Frame(frequentItemsFr,bg=bgColour1)
freqDetButtons=Frame(frequentItemsFr,bg=bgColour1)

dataEntryFr = Frame(bg=bgColour3,highlightthickness=10,highlightbackground='gray65',highlightcolor='gray65')
dataEntryFr.pack(fill='x',ipadx=20,ipady=5)

#___________________HEADER FRAME______________________________


currentDateText = StringVar()
def updateTodaysDate():
    currentDateText.set('Today\'s Date: '+str(datetime.date.today())+'   View Entries for')
currentDateLabel = Label(headerFr,textvariable=currentDateText,bg=bgColour1,fg=fgColour1,padx=5)
currentDateLabel.grid(column=0, row=0,sticky='w')

todayDate = StringVar()
todayDate.set(str(datetime.date.today()))
dateList = ['31/12/99','31/12/99','31/12/99','31/12/99']
currentDateDropDown = OptionMenu(headerFr,todayDate,*dateList)
currentDateDropDown.configure(bg=bgColour1,fg=fgColour1,activebackground=bgColour1,activeforeground='silver',highlightbackground=bgColour1,bd=1)
currentDateDropDown.grid(column=1, row=0,sticky='w')
#listbox

#___________________MAIN TABLE DISPLAY_______________________________

sageSubmitButton=Button(headerFr,text='Upload to Sage',bg=bgColour2s,bd=0,highlightthickness=0)

def displayRawEntries():
    if rawViewButton['relief']=='sunken':
        rawViewButton.configure(relief='raised',bd=0)
        sageViewButton.configure(relief='sunken',bd=1)
        sortedEntriesTableFr.forget()
        entriesTableFr.pack(fill='x')
        sageSubmitButton.grid_forget()


def displaySageEntries():
    if sageViewButton['relief']=='sunken':
        sageViewButton.configure(relief='raised',bd=0)
        rawViewButton.configure(relief='sunken',bd=1)
        entriesTableFr.forget()
        sortedEntriesTableFr.pack(fill='x')
        sageSubmitButton.grid(column=2,row=0,padx=200)

rawViewButton = Button(tabButtonsFr,text='Raw Entries View',command=displayRawEntries,bg=bgColour2,activebackground=bgColour2,highlightthickness=0)
rawViewButton.grid(column=0,row=0)
sageViewButton=Button(tabButtonsFr,text='Sage View',relief='sunken', command=displaySageEntries,bg=bgColour2s,activebackground=bgColour2s, highlightthickness=0)
sageViewButton.grid(column=1,row=0)


#___________________ENTRIES TABLE FRAME______________________________

#entries view
#separate frame with 'Sage' view
#entries view contains grouped items with raw duration data


copyButtons = []
delButtons = []
editButtons = []
sepLines=[]
rows = []

def copyEntry(row):
    #set item text in new entry area
    #- identify row
    #- use text directly from row to update items in data entry frame?
    project.set(sortedListOfEntries.entriesList[row].project)
    timeItem.set(sortedListOfEntries.entriesList[row].timeEntriesList[0][0])
    showRelatedTimeItems(None)
    items=sortedListOfEntries.entriesList[row].timeEntriesList
    for i in range(0,len(items)): fractions[i].set(items[i][2])
    details.set(sortedListOfEntries.entriesList[row].details)
    pass
def deleteEntry(row):
    #remove from list and update table
    del sortedListOfEntries.entriesList[row]
    updateEntriesTable(sortedListOfEntries.entriesList)
    sortedListOfEntries.createRawEntriesDF()
    sortedListOfEntries.createSortedEntriesDF()
    sortedListOfEntries.saveRawEntriesData()
    updateSortedEntriesTable()
    pass
def editEntry(row):
    #on press, change line to Entry items
    #on depress, update list item with Entry text then update table (which would replace Etnry items with Labels)

    pass

def updateEntriesTable(entriesList):
    copyButtons = []
    delButtons = []
    editButtons = []
    sepLines=[]
    rows = []
    [child.destroy() for child in  entriesTableFr.winfo_children()]

    i=0
    for entry in entriesList:
        durStr=''
        timeEntryName=''
        timeEntryProduct=''
        for productItem in entry.timeEntriesList:
            dur_mins=productItem[3]
            if dur_mins>0:
                durStr+='{:02.0f}'.format(dur_mins/60)+' : '+'{:02.0f}'.format(dur_mins-dur_mins/60)+'\n'
                timeEntryName+=productItem[0]+'\n'
                timeEntryProduct+=productItem[1]+'\n'        
        copyButtons.append(Button(entriesTableFr, text='Copy',command=lambda i=i: copyEntry(i),font='TkSmallCaptionFont',bg=bgColour2,bd=0))
        copyButtons[i].grid(column=0,row=i*2+1,padx=1,pady=2)
        delButtons.append(Button(entriesTableFr,  text='Delete',command=lambda i=i: deleteEntry(i),font='TkSmallCaptionFont',bg=bgColour2,bd=0))
        delButtons[i].grid(column=1,row=i*2+1,padx=1,pady=2)
        editButtons.append(Button(entriesTableFr,  text='Edit',command=lambda i=i: editEntry(i),font='TkSmallCaptionFont',bg=bgColour2,bd=0))
        editButtons[i].grid(column=2,row=i*2+1,padx=1,pady=2)
        rowHeaders=['Date','Time','Duration','Project','Entry Name/Type','Product','Details']
        rowItems=[(entry.entryDate,12),(entry.startTime,5),(durStr.strip('\n'),5),(entry.project,20),(timeEntryName.strip('\n'),20),(timeEntryProduct.strip('\n'),15),(entry.details,30)]
        columns=[]
        j=3
        for item in rowItems:
            if i==0: Label(entriesTableFr,text=rowHeaders[j-3],font='TkHeadingFont',bg=bgColour2,fg=fgColour2).grid(column=j,row=0)
            columnItem=Label(entriesTableFr,text=item[0],width=item[1],bg=bgColour2)
            columnItem.grid(column=j,row=(i*2)+1,padx=10,pady=2)
            columns.append(columnItem)
            j+=1
        rows.append(columns)
        #sepStyle=ttk.Style()
        #sepStyle.configure('TSeparator',background='white')
        newSeparator=ttk.Separator(entriesTableFr,orient='horizontal',style='TSeparator')
        sepLines.append(newSeparator)
        sepLines[i].grid(column=0,row=(i*2)+2,columnspan=j,ipadx=600)
        i+=1


#___________________SORTED AGGREGATED TABLE FRAME_______________________

def updateSortedEntriesTable():
    sepLines=[]
    [child.destroy() for child in  sortedEntriesTableFr.winfo_children()]
    columnWidths=[10,20,30,15,10,40]
    i=0
    for entry in sortedListOfEntries.finalSageEntries.iterrows():
        entry=entry[1]
        j=0
        for item in entry:
            if i==0:
                Label(sortedEntriesTableFr,text=sortedListOfEntries.finalSageEntries.columns[j],font='TkHeadingFont',bg=bgColour2s).grid(column=j,row=0)
            Label(sortedEntriesTableFr,text=item,width=columnWidths[j],bg=bgColour2s).grid(column=j, row=(i*2)+1,padx=5,pady=2)
            j+=1
        newSeparator=ttk.Separator(sortedEntriesTableFr,orient='horizontal',style='TSeparator')
        sepLines.append(newSeparator)
        sepLines[i].grid(column=0,row=i*2+2,columnspan=j,ipadx=600)
        i+=1


#___________________ FREQ USED ITEMS FRAME______________________________    


def useSelectedFreqProj(event:Event):
    project.set(event.widget['text'])
    listTimeItems(None)

prodFilter:list=['ProdA','ProdB','ProdC','ProdD','NonProd']


def useProductFilter(event:Event):
    global prodFilter
    #timeItem.set(event.widget['text'])
    #showRelatedTimeItems(None)
    prodButton:Button=event.widget
    if prodButton['relief']=='raised':
        prodButton.configure(relief='sunken',bd=1,highlightbackground=fgColour2,fg=fgColour1)
        prodFilter.append(prodButton['text'])
        listTimeItems(None)
        #showRelatedTimeItems(None)
        return 'break'
    else:
        prodButton.configure(relief='raised',bd=0,highlightbackground='maroon',fg='silver')
        prodFilter.remove(prodButton['text'])
        listTimeItems(None)
        return 'break'

def useSelectedFreqDetails(event:Event):
    details.set(event.widget['text'])

def updateFreqItems():
    global freqProjLabel,freqItemsLabel,freqDetLabel
    [child.destroy() for child in freqProjButtons.winfo_children()]
    [child.destroy() for child in freqItemsButtons.winfo_children()]
    [child.destroy() for child in freqDetButtons.winfo_children()]
    freqProjLabel=Label(freqProjButtons,text='Freq Projects',bg=bgColour1,fg=fgColour1,font='TkHeadingFont')
    freqItemsLabel=Label(freqItemsButtons,text='Time Items:\n Product Filter',bg=bgColour1,fg=fgColour1,font='TkHeadingFont')
    freqDetLabel=Label(freqDetButtons,text='Freq Details',bg=bgColour1,fg=fgColour1,font='TkHeadingFont')
    freqProjLabel.pack(pady=10)
    freqItemsLabel.grid(column=0,columnspan=2,row=0, pady=10)
    freqDetLabel.pack(pady=10)
    freqProjButtons.grid(column=1,row=0,padx=40,sticky='N')
    freqItemsButtons.grid(column=2,row=0,padx=40,sticky='N')
    freqDetButtons.grid(column=3,row=0,padx=40,sticky='N')
    recentProjects=sortedListOfEntries.entriesDF['Project'].unique()
    recentTimeItems=sortedListOfEntries.entriesDF['Item Product'].unique()
    recentDetails=sortedListOfEntries.entriesDF['Details'].unique()
    i = 0
    for project in recentProjects:
        if i>3: break
        i+=1
        recentButton = Button(freqProjButtons,text=project,font='TkSmallCaptionFont',bd=0,bg=bgColour1,highlightbackground=bgColour1,fg=fgColour1)
        recentButton.pack()
        recentButton.bind('<Button-1>',useSelectedFreqProj)
    i = 0
    j = 0
    for timeItem in ['ProdA','ProdB','ProdC','ProdD','NonProd']:
        #if i>3: break
        recentButton = Button(freqItemsButtons,text=timeItem,font='TkSmallCaptionFont',relief='sunken', bd=1,bg=bgColour1,highlightbackground=fgColour2,fg=fgColour1)
        recentButton.grid(column=j,row=i+1)
        #recentButton.bind('<ButtonRelease-1>',useProductFilter)
        recentButton.bind('<Button-1>',useProductFilter)
        i+=1
        if i>2: i=0; j+=1
    i = 0
    for details in recentDetails:
        if i>3: break
        i+=1
        if details!='':
            recentButton = Button(freqDetButtons,text=details,font='TkSmallCaptionFont',bd=0,bg=bgColour1,highlightbackground=bgColour1,fg=fgColour1)
            recentButton.pack()
            recentButton.bind('<Button-1>',useSelectedFreqDetails)

    

#___________________ DATA ENTRY FRAME______________________________

startDate=StringVar()
startTime=StringVar()
endTime=StringVar()
duration=StringVar()
project=StringVar()
timeItem=StringVar()
details =StringVar()

product1=StringVar()
product2=StringVar()
product3=StringVar()
product4=StringVar()
products=[product1,product2,product3,product4]

fractions=[StringVar(),StringVar(),StringVar(),StringVar()]

global selectedProject
global listOfItems
overallListOfEntries=[]
sortedListOfEntries=projectsData.timeEntryDFs()

def listProjects(event):
    #check the entered text and get required project values
    projects=projectsData.get_projects(projectEntry.get())
    listValues=[proj.projName for proj in projects]
    projectEntry.configure(values=listValues)
    projectEntry.event_generate('<Button-1>')
    #use lambda if re-adding validate to combobox in this funciton

def listTimeItems(event):
    #function to populate time items after project is selcted
    global selectedProject
    if projectEntry.get()!='':
        selectedProject = projectsData.find_project_from_name(projectEntry.get())
        # listValues=selectedProject.get_itemNames()
        # timeItemEntry.configure(values=listValues)
        # timeItemEntry.event_generate('<Button-1>')
        listValues=selectedProject.get_namesAndProducts()
        #if prodFilter==None: listValues=[item[0] for item in listValues]
        #else:
        filteredList=[]
        for item in listValues:
            if item[1] in prodFilter: filteredList.append(str(item[0])+' - '+str(item[1]))
        listValues=filteredList
        timeItemEntry.configure(values=listValues)
        timeItemEntry.event_generate('<Button-1>')

relatedItems=[]
relatedFractions=[]

def showRelatedTimeItems(event):
    #selectedTimeItem = selectedProject.get_itemFromName(timeItemEntry.get())
    global listOfItems
    relatedItems
    relatedFractions
    for item in relatedItems:
        item.destroy()
    for item in relatedFractions:
        item.destroy()
    selectedProject = projectsData.find_project_from_name(projectEntry.get())
    #if selectedProject!=None:
    listOfItems = selectedProject.get_relatedItems(str(timeItemEntry.get()).split(' - ')[0],3) #takes name and returns a list of tuples containin item name and product
        #filteredList=[]
        #for item in listOfItems:
        #    if item[1]==prodFilter: filteredList.append(item)
    #listOfItems=filteredList
    for prod in products:
        prod.set('')
    s = min(len(listOfItems),len(products))
    timeItemsFr.grid_forget()
    for x in range(0,s):
        products[x].set(listOfItems[x][0]+'  '+listOfItems[x][1])
        item = Label(timeItemsFr,textvariable=products[x],bg=bgColour3)
        item.grid(column=0,row=x)
        itemFraction = Entry(timeItemsFr,textvariable=fractions[x],width=5)
        itemFraction.grid(column=1,row=x)
        relatedItems.append(item)
        relatedFractions.append(itemFraction)
        timeItemsFr.grid(column=6,row=2,pady=10)

def clearEntry():
    project.set('')
    timeItem.set('')
    details.set('')
    timeItemsFr.grid_forget()
    print('widget status'+str(timeItemsFr.winfo_ismapped()))


def addEntry():
    global overallListOfEntries
    global sortedListOfEntries
    print('widget status'+str(timeItemsFr.winfo_ismapped()))
    if projectEntry.get()!='' and timeItemEntry.get()!='' and duration.get()!='00 : 00' and timeItemsFr.winfo_ismapped():
        newEntry = projectsData.timeEntryObject(startDate.get(),startTime.get(),duration.get(),project.get(),details.get())
        assert str(newEntry.entryDate)[0:4]!='1970'
        try:
            s = min(len(listOfItems),len(products))
            for i in range(0,s):
                newEntry.add_timeEntriesList(listOfItems[i][0],listOfItems[i][1],fractions[i].get())
            
            #overallListOfEntries.append(newEntry)
            sortedListOfEntries.appendEntry(newEntry)
            updateEntriesTable(sortedListOfEntries.entriesList)
            #sortedListOfEntries=projectsData.timeEntryDFs(overallListOfEntries)
            updateSortedEntriesTable()
            updateFreqItems()
            startTime.set(endTime.get()[0:5])
            clearEntry()

        except NameError as e:
            print(e)
        #except BaseException as e:
        #    print(e)

use_current_time = True

def useCurrentTime():
    global use_current_time
    if currTimeButton['relief']=='sunken':
        currTimeButton['relief']='raised'
        endEntry.configure(readonlybackground='white',state='normal')
        durEntry.configure(readonlybackground='white',state='normal')
        use_current_time = False
        endTime.set(str(getCurrentDateTime().strftime('%H:%M')))
    else:
        currTimeButton['relief']='sunken'
        endEntry.configure(readonlybackground='silver',state='readonly')
        durEntry.configure(readonlybackground='silver',state='readonly')
        use_current_time = True

dataEntryFr.grid_columnconfigure(0, minsize=100)
Label(dataEntryFr,text='Date',bg=bgColour3).grid(column=1,row=0)
Entry(dataEntryFr,textvariable=startDate,width=12,justify='center').grid(column=1,row=1, padx=3)
Label(dataEntryFr,text='Start',bg=bgColour3).grid(column=2,row=0)
Entry(dataEntryFr,textvariable=startTime,width=8,justify='center').grid(column=2,row=1, padx=3)
Label(dataEntryFr,text='End',bg=bgColour3).grid(column=3,row=0)
endEntry = Entry(dataEntryFr,textvariable=endTime,width=8,justify='center',readonlybackground='silver',state='readonly')
endEntry.grid(column=3,row=1, padx=3)
Label(dataEntryFr,text='Duration',bg=bgColour3).grid(column=4,row=0)
durEntry=Entry(dataEntryFr,textvariable=duration,width=8,justify='center',readonlybackground='silver', state='readonly')
durEntry.grid(column=4,row=1, padx=3)
currTimeButton = Button(dataEntryFr,text='Use current time',relief='sunken',command=useCurrentTime,bg=bgColour3,activebackground=bgActColour3,highlightthickness=0)
currTimeButton.grid(columnspan=2,column=3,row=2, sticky='N')
Label(dataEntryFr,text='Project',bg=bgColour3).grid(column=5,row=0)
projectNames = [proj.projName for proj in projectsData.get_projects()]
projectEntry = ttk.Combobox(dataEntryFr,values=projectNames,textvariable=project)#, validatecommand=listProjects, validate='all')
projectEntry.bind('<Return>',listProjects)
projectEntry.bind('<KP_Enter>',listProjects)
projectEntry.bind('<<ComboboxSelected>>',listTimeItems)
projectEntry.grid(column=5,row=1, padx=3)
Label(dataEntryFr,text='Time Item',bg=bgColour3).grid(column=6,row=0)
timeItemEntry = ttk.Combobox(dataEntryFr,textvariable=timeItem)
timeItemEntry.bind('<<ComboboxSelected>>',showRelatedTimeItems)
timeItemEntry.grid(column=6,row=1, padx=3)
timeItemsFr = Frame(dataEntryFr,bg=bgColour3)
#timeItemsFr.grid(column=5,row=2,pady=10)

#[Entry(timeItemsFr,textvariable=fractions[x]).pack() for x in range(0,len(products))]
Label(dataEntryFr,text='Details',bg=bgColour3).grid(column=7,row=0)
Entry(dataEntryFr,textvariable=details,width=40).grid(column=7,row=1, padx=3)

add_clear_ButtonsFr=Frame(dataEntryFr)
add_clear_ButtonsFr.grid(column=7,row=2)
Button(add_clear_ButtonsFr,text='Add Entry',command=addEntry,bg=bgColour3,activebackground=bgActColour3,highlightthickness=0).grid(column=1,row=0,padx=2)
Button(add_clear_ButtonsFr,text='Clear',command=clearEntry,bg=bgColour3,activebackground=bgActColour3,highlightthickness=0).grid(column=0,row=0)

#create thread
#loop update of time and duration text
#sleep thread for 0.5s
def getCurrentDateTime():
    return datetime.datetime.now()

start=getCurrentDateTime()
startDate.set(getCurrentDateTime().date())
startTime.set(getCurrentDateTime().strftime('%H:%M'))

def updatetime():
    try:
        if use_current_time:
            endTime.set(str(getCurrentDateTime().strftime('%H:%M %S')))
        startTimeFrmStr = datetime.datetime(*(time.strptime(startTime.get(),'%H:%M')[0:6]))
        endTimeFrmStr = datetime.datetime(*(time.strptime(endTime.get()[0:5],'%H:%M')[0:6]))
        timeDiff = endTimeFrmStr-startTimeFrmStr
        timeDiffHours = math.floor(timeDiff.seconds/3600)
        timeDiffMins = timeDiff.seconds/60 - timeDiffHours*60
        duration.set('{:02.0f}'.format(timeDiffHours)+' : '+'{:02.0f}'.format(timeDiffMins))
        updateTodaysDate()
        #[child.bind('<Button-1>',useSelectedFreqTimeItem) for child in freqItemsButtons.winfo_children()]
    except BaseException as e:
        pass
    main_window.after(499,updatetime)

main_window.after(0,updatetime)

def loadDataOnProgramStartUp():
    #this code will update table from saved data when program starts
    #global overallListOfEntries
    global sortedListOfEntries
    sortedListOfEntries=projectsData.timeEntryDFs()
    dataRead=sortedListOfEntries.readDataFromFile()
    if dataRead:
        updateEntriesTable(sortedListOfEntries.entriesList)
        updateSortedEntriesTable()
        updateFreqItems()

loadDataOnProgramStartUp()
main_window.mainloop()