# -*- coding: utf-8 -*-
"""
Created on Fri Jan 06 10:02:28 2017

@author: simon.desmet
"""

# NFCDD NODE POINT MEASUREMENT WRITER



# This program is for writing results from ISIS 1D results files to an NFCDD format node point table file

#import relevent modules

import pandas as pd # a module that allows spreadsheet functionality

import sys # allows system comands

import numpy as np # allows maths operations

import os # a module that allows os commands
import glob # a module that allows file sorting by extension.

######################################
# create Nodepointtable using Pandas


NFCDD_ID = []     
NodePointName = []
ModelledFloodGroupCode = []
ReturnPeriod = []
LevelValue = []
FlowValue = []
Supporting = []
Deleted = []
Downloaded = []
Changed = []
For_upload = []
CheckCode = []       
#NPM = pd.DataFrame(data)      
#our NodePointMeasurement table is now created with a dummy entry on the first row
#note Pandas orders the columns alphabetically by default
##################################

# get location of ing file for node list

INGPATH = raw_input("file path for LNG file please:")
#INGPATH = r'S:\Sheffield Based Jobs\CS078708_NW Package 3\Hydraulics\NFCDD_PROCESSING\WRAY\FILES\WRAY.lng'
print INGPATH

#get naming data
#EAcode = 'ea1207'
EAcode = raw_input("EA Region-Area-Catchment code please, e.g. ea01207")
#River = 'Wray'
River = raw_input("River Name, e.g. Wray")
#Code_end = 'SFRM_2015'
Code_end = raw_input("Modelled Flood Group Name, e.g. SFRM_2015")
MFGC=EAcode+River+Code_end

# get location of ISIS results files 

ISISRESULTSPATH = raw_input("FOLDER path for ISIS Flow and Head results please:")
#ISISRESULTSPATH = r'S:\Sheffield Based Jobs\CS078708_NW Package 3\Hydraulics\NFCDD_PROCESSING\WRAY\1DRESULTS'

FlowResults =[]#list for flow results file paths
HeadResults =[]#list for head results file paths


for filename in glob.glob(os.path.join(ISISRESULTSPATH, '*F.csv')):
    print filename
    FlowResults.append(filename)#takes the path of each file in the folder than ends F.csv and adds it to the flow results list

for filename in glob.glob(os.path.join(ISISRESULTSPATH, '*H.csv')):
    print filename
    HeadResults.append(filename)# as above but for head files.


# open ING file and read nodes into list.

INGLIST = []
with open(INGPATH) as f:
    INGOPEN = f.readlines()
    for x in INGOPEN:
        #y = x[:-2]
        y = x.replace("\n","")
        INGLIST.append(y)
INGLIST.reverse()

#create NFCDD ID from INGLIST and associate each number with node id in INGLIST (using python dict)
NFCDD_no = 1
NFCDD_no_list = []
for node in INGLIST:
    NFCDD_no_list.append(NFCDD_no)
    NFCDD_no = NFCDD_no+1
NFCDD_dict = dict(zip(INGLIST, NFCDD_no_list))

##################################
# cycle through each Flow results file going through all the results in each file copying out the nodes that match INGLIST into the NodePointMeasurement table

for HeadResultfile in HeadResults:
    with open(HeadResultfile) as f:
        Results = f.readlines()
# take return period out of file name
        pathsplit = HeadResultfile.split("_")
        retperiod = int(pathsplit[-3])            
        for j in Results:
            k = j.split(",")
            if k[0] in INGLIST:
                LV = round(float(k[1]),2)
                LevelValue.append(LV)
                NodePointName.append(EAcode+k[0])
                ModelledFloodGroupCode.append(MFGC)
                ReturnPeriod.append(retperiod)
                Supporting.append('FALSE')
                Deleted.append('FALSE')
                Downloaded.append('FALSE')
                Changed.append('FALSE')
                For_upload.append('TRUE')
                NFCDD_ID.append(NFCDD_dict[k[0]])
                
            else:
                continue

 
for FlowResultfile in FlowResults:
    with open(FlowResultfile) as f:
        Results = f.readlines()
        for j in Results:
            k = j.split(",")
            if k[0] in INGLIST:
                FV = round(float(k[1]),2)
                FlowValue.append(FV)
                CheckCode.append(k[0])
            else:
                continue
            
#create DataFrame (spreadsheet like table)            

NPMTable = pd.DataFrame(
    {'NodePointName' : NodePointName,
     'ModelledFloodGroupCode' : ModelledFloodGroupCode,
     'ReturnPeriod' : ReturnPeriod,
     'LevelValue' : LevelValue,
     'FlowValue' : FlowValue,
     'Supporting' : Supporting,
     'Downloaded' : Downloaded,
     'Changed' : Changed,
     'For_upload' : For_upload,
     'NFCDD_ID' : NFCDD_ID
    })

NPMTable = NPMTable.sort(['NodePointName'])
    
    
    
#reorder columns in table
NPMTable = NPMTable[['NFCDD_ID','NodePointName','ModelledFloodGroupCode','ReturnPeriod','LevelValue','FlowValue','Supporting','Downloaded','Changed','For_upload']]

# write DataFrame (NPMTable) to csv

NPMTable.to_csv(path_or_buf=ISISRESULTSPATH+'\\NPM\\'+MFGC+'.csv', sep=',')