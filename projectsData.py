import datetime, dateutil
from math import ceil, floor
from typing import List
import Levenshtein
from numpy.lib.function_base import diff
import pandas as pd
import numpy as np
#import hdf5

class project():

    def __init__(self, projID, projName, projTimeItems):
        self.projID = projID
        self.projName = projName
        self.projTimeItems = projTimeItems #list of tuples consisting of item name and product

    def get_itemNames(self):
        #all item names
        item_names = []
        for item in self.projTimeItems:
            item_names.append(item[0])
        return item_names

    def get_namesAndProducts(self):
        #return tuples of item names and products
        timeItems=[]
        for item in self.projTimeItems:
            timeItems.append((item[0],item[1]))
        return timeItems

    def get_itemFromName(self,itemName):
        for item in self.projTimeItems:
            if itemName==item[0]:
                return item

    def get_combinedItems(self):
        #simplified items list, combining products for similarly named items
        #13/02/2020 - still want to keep all items as it will make referencing back to the original items easier later
        timeItemsList = {}
        for itemToAdd in self.projTimeItems:
            for timeItem in timeItemsList:
                if Levenshtein.distance(itemToAdd[0],timeItem.key)<10:
                    #item name deemed to match item already in list, so add product
                    timeItemsList[timeItem.key] = timeItem.value.append(itemToAdd[1])
                    break
                else:
                    #no similar item in list, so add key with value of the product as first item in a new list
                    timeItemsList[itemToAdd[0]] = [itemToAdd[1]]

    def get_relatedItems(self, itemToNameCheck, strDiffValue):
        #13/02/2020 - this function should return a list of related items including both the name and product
        #only unique products should be returned, so we need the closest match for each product
        relatedItems = []
        for projTimeItem in self.projTimeItems:
            if Levenshtein.distance(itemToNameCheck,projTimeItem[0])<strDiffValue:
                relatedItems.append(projTimeItem)
        return relatedItems


    def get_products(self):
        #unique product names
        productsList = []
        for item in self.projTimeItems:
            if item[1] not in productsList:
                productsList.append(item[1])
        return productsList

projectsDF=pd.DataFrame()
# sample projects list - this could be replaced later by a feature to add or import a projects list
projectsDF = pd.DataFrame(
    {'proj_code':['PROJ001','PROJ002','PROJ003','PROJ004','PROJ005'],
     'proj_name':['Big Project','Little project','Waterfall project','Agile project','R&D project'],
     'task_list':[
         [('everyday task','ProdA'),('everyday task','ProdB'),('big task','ProdB')],
         [('everyday task','ProdA'),('small task','ProdB'),('routine tasks','General')],
         [('unexpected issue task','ProdA'),('special task','ProdB')],
         [('stand-up task','ProdA'),('sitting down','ProdB'),('bug fixing','ProdA'),('code review','ProdC'),('technical debt avoidance','ProdA')],
         [('where did the time go','ProdA'),('break-through celebration','ProdB')]
     ]
    }
)


""" 
projects_list.append(project('PROJ001','The big EPC project',[('doing everyday stuff','ProdA'),('some special task','ProdA'),('doing everyday stuff','ProdB'),('some special task','ProdB')]))
projects_list.append(project('PROJ002','The never ending project',[('doing everyday stuff','ProdA'),('some special task','ProdA'),('doing everyday stuff','ProdB'),('some special task','ProdB')]))
projects_list.append(project('PROJ003','The simple project',[('task 1','ProdA'),('task 2','ProdA')]))
projects_list.append(project('PROJ004','The everything project',[('generaltask1','ProdA'),('everydaything','ProdA'),('generaltask','ProdB'),('mostdaysthing','ProdB'),('task1','ProdC'),('manydaystask','ProdC'),('majortask','ProdD'),('slightly different task','ProdD')]))
projects_list.append(project('PROJ005','DemoProj',[('Routine','ProdA'),('Reactve','ProdA'),('Remedial','ProdA'),('Routine','ProdB'),('Reactive','ProdB'),('Remedial','ProdB'),('Admin Task','NonProd')]))
 """

projectsFilename = 'projectsData.json'

"""def saveProjectsData():
    with open(projectsFilename,'w'):
        projectsDF.to_json(projectsFilename)

saveProjectsData()    #WILL ONLY NEED THIS AGAIN IF FEATURE CREATED TO AMEND PROJECTS FROM APP"""

def readProjectsFromFile():
    try:
        with open(projectsFilename):
            projectsDF=pd.read_json(projectsFilename)
    except FileNotFoundError as e:
        print('no such file for projects, results in:')
        print(e)
        return False
readProjectsFromFile()
projects_list = []
[projects_list.append(project(row[0],row[1],row[2])) for row in zip(projectsDF['proj_code'],projectsDF['proj_name'],projectsDF['task_list'])]

def get_projects(text=None):
    
    

    projects=[]
    if text==None:
        return projects_list
    else:
        for proj in projects_list:
            if Levenshtein.distance(text,proj.projName)<20:
                projects.append(proj)
    return projects

def find_project_from_name(name):
    for proj in projects_list:
        if name == proj.projName:
            return proj

def get_timeItems():
        #return all time items from all projects as a list of tuples (item name, product)
        items = []
        for project in projects_list:            
            for item in project.projTimeTitems:
                items.append(item)
        return items

def get_itemNames():
        #return all item names
        item_names = []
        items = get_timeItems()
        for item in items:
            item_names.append(item[0])
        return item_names

def get_products():
        #return list of unique products from time items
        productsList = []
        items = get_timeItems()
        for item in items:
            if item[1] not in productsList:
                productsList.append(item[1])
        return productsList
    


#print(projects_list[0].g )

#projects list will be list of project objects, each with id, name and list of timeItems as tuples of item description and product

class timeEntryObject():

    def __init__(self, entryDate, startTime, duration:str='', project='', details=''):
        self.entryDate = entryDate#dateutil.parser.parse(entryDate)
        self.startTime = startTime
        dur=duration.rsplit(' : ')
        self.duration = int(dur[0])*60+int(dur[1]) if (dur[0].isnumeric() and dur[1].isnumeric()) else 0
        self.project = project
        self.timeEntriesList = []
        self.details = details


    def add_timeEntriesList(self,name, product, fraction:str):
        try:
            fraction = float(fraction)
        except:
            fraction=0
        part_duration_mins = fraction*self.duration
        self.timeEntriesList.append((name,product,fraction,part_duration_mins))


class timeEntryDFs():

    dataFilename = 'timesheetData.json'

    def __init__(self, entriesList: List[timeEntryObject] = None):
        self.entriesDF = pd.DataFrame()
        self.rawEntriesDF = pd.DataFrame()
        self.entriesList = entriesList            
        self.createRawEntriesDF()
        self.createSortedEntriesDF()
        #self.saveRawEntriesData()

    def appendEntry(self,entry:timeEntryObject):
        if self.entriesList == None: self.entriesList = []
        self.entriesList.append(entry)
        self.createRawEntriesDF()
        self.createSortedEntriesDF()
        self.saveRawEntriesData()
        for x in self.entriesList: assert str(x.entryDate)[0:4]!='1970'

    def createRawEntriesDF(self):
        self.rawEntriesDF=pd.DataFrame()
        if self.entriesList!=None and len(self.entriesList)>0:            
            for entry in self.entriesList:
                data = pd.DataFrame({'Date': [entry.entryDate], 'Start': [entry.startTime], 'Project': [entry.project],
                                    'Time Items List': [entry.timeEntriesList], 'Details': [entry.details]})
                self.rawEntriesDF=pd.concat([self.rawEntriesDF,data],sort=True,ignore_index=True)
            self.rawEntriesDF=self.rawEntriesDF.astype({'Date':str,'Details':str})
            for x in self.entriesList: assert str(x.entryDate)[0:4]!='1970'
        try: self.createRawEntriesDFsByDate()
        except:print('no!')

    def createRawEntriesDFsByDate(self):
        self.rawEntriesDfsDated={}
        if self.entriesList!=None and len(self.entriesList)>0:   
            dates1=[entry.entryDate for entry in self.entriesList] #list all dates
            dates2=list(set(dates1))
            df=pd.DataFrame()
            for date in dates2:
                for entry in self.entriesList:
                    if entry.entryDate==date:
                        data = pd.DataFrame({'Date': [entry.entryDate], 'Start': [entry.startTime], 'Project': [entry.project],
                                            'Time Items List': [entry.timeEntriesList], 'Details': [entry.details]})
                        df=pd.concat([df,data],sort=True,ignore_index=True)
                        df=df.astype({'Date':str,'Details':str})
                self.rawEntriesDfsDated[date]=df
        print(self.rawEntriesDfsDated)


    def createSortedEntriesDF(self):
        self.entriesDF=pd.DataFrame()
        self.finalSageEntries=pd.DataFrame()
        if self.entriesList!=None and len(self.entriesList)>0:
            for entry in self.entriesList:
                for item in entry.timeEntriesList:
                    if int(item[3])>0:
                        projID=find_project_from_name(entry.project).projID
                        data=pd.DataFrame({'Date': [entry.entryDate], 'Start': [entry.startTime], 'Duration': [item[3]],'ProjectID':[projID],
                                        'Project': [entry.project], 'Item Name': [item[0]], 'Item Product': [item[1]], 'Details': [entry.details]})
                        self.entriesDF=pd.concat([self.entriesDF,data],sort=True,ignore_index=True)
            try:
                def sortEntriesDF(df):
                    df.sort_values(by=['Duration'],inplace=True)
                    df.sort_values(by=['Details'],inplace=True)
                    df.sort_values(by='Item Product',inplace=True)
                    df.sort_values(by=['Item Name'],inplace=True)
                    df.sort_values(by=['Project'],inplace=True)
                    #df.sort_values(by=['Date'],inplace=True)
                index=pd.MultiIndex.from_frame(self.entriesDF[['ProjectID','Project','Item Name','Item Product','Details']])
                df = pd.DataFrame(self.entriesDF.values, index=index, columns=self.entriesDF.columns)
                #df=df.astype({'Duration':int})
                df=pd.DataFrame(df.aggregate('Duration'))
                df=df.groupby(level=['ProjectID','Project','Item Name','Item Product','Details']).sum()
                df.reset_index(inplace=True)
                df.sort_values(by=['Duration'],inplace=True,ascending=False)
                print(df)
                diffSum=int()
                def roundFcn(x):
                    nonlocal diffSum
                    if diffSum==0 or abs(diffSum<8): print('diffSum: '+str(diffSum));diff=x-round(x/15)*15; print('diff: '+str(diff));diffSum+=diff; print('rnd ...diffSum: '+str(diffSum)); return round(x/15)*15
                    elif diffSum<0: print('diffSum: '+str(diffSum));diff=x-floor(x/15)*15; print('diff: '+str(diff));diffSum+=diff; print('rnd down...diffSum: '+str(diffSum)); return floor(x/15)*15
                    else: print('diffSum: '+str(diffSum));diff=x-ceil(x/15)*15; print('diff: '+str(diff));diffSum+=diff;print('rnd up...diffSum: '+str(diffSum));  return ceil(x/15)*15
                    #if diffSum<0: diffSum+=x-floor(x/15)*15; return floor(x/15)*15
                    #else: diffSum+=x-ceil(x/15)*15; return ceil(x/15)*15
                df['Duration']=df['Duration'].apply(roundFcn)
                df=df.astype({'Duration':int})
                df.replace(0,np.nan,inplace=True)
                df.dropna(inplace=True)
                sortEntriesDF(df)
                df=df.reindex(['ProjectID','Project','Item Name','Item Product','Duration','Details'],axis='columns')
                self.finalSageEntries=df
            except BaseException as e:
                print('possible issue sorting; bad data?')
                print(e)
            for x in self.entriesList: assert str(x.entryDate)[0:4]!='1970'

    def saveRawEntriesData(self):
            with open(self.dataFilename,'w'):
                #self.rawEntriesDF.to_hdf(filename,key=self.rawEntriesDF)
                self.rawEntriesDF.to_json(self.dataFilename)

    def readDataFromFile(self):
        try:
            with open(self.dataFilename):
                self.rawEntriesDF=pd.read_json(self.dataFilename)
                #print(self.rawEntriesDF.dtypes)
            if not self.rawEntriesDF.empty:
                self.rawEntriesDF=self.rawEntriesDF.astype({'Date':str,'Details':str})
                self.convertTo_listOfTimeEntryObjects()
                self.createSortedEntriesDF()
                return True
            else: return False
        except FileNotFoundError as e:
            print('no such file for data, results in:')
            print(e)
            return False
        

    def convertTo_listOfTimeEntryObjects(self):
        self.entriesList=[]
        for row in self.rawEntriesDF.iterrows():
            row=row[1]
            #print(type(row['Date']))
            entry = timeEntryObject(entryDate=row['Date'], startTime=row['Start'], project=row['Project'], details=row['Details'])
            entry.timeEntriesList=row['Time Items List']
            self.entriesList.append(entry)
        for x in self.entriesList: assert str(x.entryDate)[0:4]!='1970'
