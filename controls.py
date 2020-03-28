"""""
This will have the data dictionaries for any filters we may use on the app. 
"""""

masterFile = "data/MasterData.csv"


## Date??
# Look into further, should be able to use built in tools as filter for this
month_Controls = dict(
    Jan="January",
    Feb="February",
    Mar="March",
    Apr="April",
    May="May",
    Jun="June",
    Jul="July",
    Aug="August",
    Sep="September",
    Oct="October",
    Nov="November",
    Dec="December",
)


## Geographic filters
# These aren't complete, need to look at all avail data first and try to scrape it/export necessary stuff

#LAKES = {
 #   'LakeID': "LakeName",
#}

from LakeIDGenerator import lakeNameandID

LAKES=lakeNameandID

COUNTRIES = dict(
    USA = "USA",
    EU = "Europe",
)

# Province and Region -- research further, can this be pulled from LAT/LONG? easily?

# PROVINCES = dict(
#     USA = "USA",
#     EU = "Europe",
# )
#
# REGIONS = dict(
#     USA = "USA",
#     EU = "Europe",
# )




## Methods

Substrate_Status = dict(
    PL = 'Planktronic',
    BE = 'Beach',
    PE = 'Periphyton',
)

Sample_Types = dict(
    RM = 'Routine Monitoring',
    RWC = 'Reactionary Water Column',
    SF = 'Scum Focused',
)

#need to code in depth integrated (m) for all
# and # of samples integrated for SIS
Field_Methods = dict(
    VIS = 'Vertically Integrated Sample',
    DDS = 'Discrete Depth Sample',
    SIS = 'Spatially Integrated Sample',
)

Microcystin_Method = dict(
    PPIA = 'PPIA',
    ELISA = 'ELISA',
    LCMSMS = 'LC-MSMS',
)


## Data
# need url link box for yes on all

Reporting_Measures = dict(
    PUBPR = 'Peer Reviewed or Published',
    FM = 'Field Method',
    LM = 'Lab Method',
    QAQC = 'QA/QC Available',
    INST = "Institution",
)

DB_Info = dict(
    DBID = 'Database ID',
    DBN = 'Database Name',
    UPBY = 'Uploaded By',
    UPDA = 'Upload Date',
    MCM = 'Microcystin_Method',
    NUML = 'Number of Lakes',
    NUMS = 'Number of Samples',
)