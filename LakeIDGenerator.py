"""""
This code generates a lake id for every unique lake; writing here for testing but may just end up in Oldapp.py 
"""""
from s3References import dfMasterData, dfMetadataDB

## Needs to filter by Country, Province, Sampling Method, Field Method, and Substrate

import random

"""
This code loops through the existing MasterData file and makes a list of all unique Lake Names

lakeNames = set()
for row in masterFile:
    lakeNames.add(row[2])

print(lakeNames)
"""

dfMasterData.apply(set)

lakeName = list(dfMasterData.apply(set)[2])
lakeName = sorted(lakeName)
lakeNames = dict(zip(lakeName, lakeName))


dfMetadataDB.apply(set)
instName = list(dfMetadataDB.apply(set)[4])
instName = sorted(instName)
instNames = dict(zip(instName, instName))
print(instNames)


"""
This makes an empty csv file with the total amount of lakenames found in the file (plus 50) and makes a lake id
"""

lakeIDs = set()

for i in lakeName*10:
    lakeID= random.randint(1,len(lakeName))
    lakeIDs.add(lakeID)


lakeNameandID = dict(zip(lakeIDs, lakeName))








