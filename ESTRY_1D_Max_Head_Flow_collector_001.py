# -*- coding: utf-8 -*-
"""
Created on Mon Apr 01 20:22:27 2019

@author: Simon.Desmet
"""

import pandas as pd# a module that allows spreadsheet functionality

import sys # allows system comands

import numpy as np # allows maths operations

import os # a module that allows os commands
import glob # a module that allows file sorting by extension.

#create blank lists for columns of future table
NFCDD_ID = []     
NFCDD_IDx = 1
NodePointName = []
ModelledFloodGroupCode = []
ReturnPeriod = []
ReturnPeriod_Q = []
LevelValue = []
FlowValue = []
Supporting = []
Deleted = []
Downloaded = []
Changed = []
For_upload = []
CheckCode = []   
Nodes_list = []
Links_list = []




#nodelist = raw_input("file path for list of nodes file please:")
nodelist = 'S:\\Sheffield Based Jobs\\CS090111_Kendal Package\\Pod B\\03 Delivery\\02 Hydraulics\\Fisher Beck\\TUFLOW\\WEM_Lot_1_Results\\NFCDD\\Nodes_names.csv'

Nodestable = pd.read_csv(nodelist, header=0)

# get location of ESTRY results files 

ONEDRESULTSPATH = raw_input("FOLDER path for ESTRY Flow and Head results please:")
#ISISRESULTSPATH = r'S:\Sheffield Based Jobs\CS078708_NW Package 3\Hydraulics\NFCDD_PROCESSING\WRAY\1DRESULTS'

FlowResults =[]#list for flow results file paths
HeadResults =[]#list for head results file paths


for filename in glob.glob(os.path.join(ONEDRESULTSPATH, '*1d_Q.csv')):
    print filename
    FlowResults.append(filename)#takes the path of each file in the folder than ends F.csv and adds it to the flow results list

for filename in glob.glob(os.path.join(ONEDRESULTSPATH, '*1d_H.csv')):
    print filename
    HeadResults.append(filename)# as above but for head files.


for HeadResultfile in HeadResults:
    with open(HeadResultfile) as f:
        Results = pd.read_csv(f, header=0)
# take return period out of file name
        pathsplit = HeadResultfile.split("\\")
        namesplit = pathsplit[-1].split('_')
        retperiodstr = namesplit[2]
        if 'F' in retperiodstr[-1]:
            retperiod = int(retperiodstr.strip('F'))               
        elif '5' in retperiodstr[-2]:
            retperiod = int(102)
        elif '8' in retperiodstr[-2]:
            retperiod = int(103)                            
        elif '2' in retperiodstr[-2]:
            retperiod = int(101)
        else:
            continue
        for column in Results:
            for node in Nodestable['node']:
                if node in column:
                    #create new ID and add to dataframe
                    NFCDD_ID.append(NFCDD_IDx)
                    NFCDD_IDx = NFCDD_IDx+1
                    #add node point name
                    #
                    Nodes_list.append(node)
                    #add modelled flood group code
                    #
                    #add return period
                    ReturnPeriod.append(retperiod)
                    # add level value - max value of column
                    maxlevel = max(Results[column])
                    LevelValue.append(maxlevel)
                    #supporting
                    #downloaded
                    #changed
                    #for upload
                    
        for FlowResultfile in FlowResults:
            if retperiodstr in FlowResultfile:
                with open(FlowResultfile) as fl:
                    flResults = pd.read_csv(fl, header=0)
                    for flcolumn in flResults:
                        for link in Nodestable['Link']:
                            if link in flcolumn:
                                maxQ = max(flResults[flcolumn])
                                FlowValue.append(maxQ)
                                Links_list.append(link)
                                ReturnPeriod_Q.append(retperiod)
                                
                                


DraftlevelTable = pd.DataFrame(
    {'Nodes' : Nodes_list,
     'ReturnPeriod' : ReturnPeriod,
     'LevelValue' : LevelValue,
    })
    
DraftflowTable = pd.DataFrame(
    {'Links' : Links_list,
     'FlowValue' : FlowValue,
     'ReturnPeriodQ' : ReturnPeriod_Q,
    })
    
# write DataFrame (NPMTable) to csv

DraftlevelTable.to_csv(path_or_buf=ONEDRESULTSPATH+'\\draftlevel.csv', sep=',')                                   
DraftflowTable.to_csv(path_or_buf=ONEDRESULTSPATH+'\\draftflow.csv', sep=',')        
                    #supporting
                    #downloaded
                    #changed
                    #for upload                    
                    
                    