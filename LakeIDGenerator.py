"""""
This code generates a lake id for every unique lake; writing here for testing but may just end up in Oldapp.py 
"""""
from s3References import client, MasterData, dfMasterData, MetadataDB, dfMetadataDB

## Needs to filter by Country, Province, Sampling Method, Field Method, and Substrate

import pandas as pd
import random
from dataBase import masterFile
import csv

masterDataPandaFrame=dfMasterData


"""
This code loops through the existing MasterData file and makes a list of all unique Lake Names

lakeNames = set()
for row in masterFile:
    lakeNames.add(row[2])

print(lakeNames)
"""

masterDataPandaFrame.apply(set)

lakeName = list(masterDataPandaFrame.apply(set)[2])
lakeName = sorted(lakeName)

print(len(lakeName))

"""
This makes an empty csv file with the total amount of lakenames found in the file (plus 50) and makes a lake id
"""

lakeIDs = set()

for i in lakeName*10:
    lakeID= random.randint(1,len(lakeName))
    lakeIDs.add(lakeID)

print(len(lakeIDs))

lakeNames = dict(zip(lakeName, lakeName))

lakeNameandID = dict(zip(lakeIDs, lakeName))

print(lakeNameandID)





"""
This code reads the lake names and creates a lakeID for each unique lake name
"""
#masterDF = pd.read_csv('/data/MasterData.csv')
#masterDF['LakeID'] =


"""
This takes the lake names and lake IDs from above and creates a dictionary of them.
"""











## Example end results

"""""
Continent: North America
Country: USA
Province: NA
Sampling Method: Scum Focused
Field Method: Discrete Depth Sample
Substrate: 

"""""

"""""
Continent: Europe
Country: Germany
Province: NA
Sampling Method:
Field Method:
Substrate:

"""""



"""""
Continent: South America
Country: Brazil
Province: NA
Sampling Method:
Field Method:
Substrate:

"""""