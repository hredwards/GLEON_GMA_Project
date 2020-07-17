"""""
This will have the data dictionaries for any filters we may use on the app. 
"""""

from s3References import client, MasterData, dfMasterData, MetadataDB, dfMetadataDB
from LakeIDGenerator import lakeNames, instNames

masterFile = "data/MasterData.csv"


## Date??
# Look into further, should be able to use built in tools as filter for this
## Geographic filters







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

LAKES=lakeNames

INSTITUTIONS = instNames

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
Substrate_Status = {
    'Planktronic' : 'Planktronic',
    'Beach' : 'Beach',
    'Periphyton' : 'Periphyton',
    'Not Reported': 'Not Reported',
}


Sample_Types = {
    'Routine Monitoring' : 'Routine Monitoring',
    'Reactionary Water Column' : 'Reactionary Water Column',
    'Scum Focused' : 'Scum Focused',
    'Not Reported': 'Not Reported',
}

Field_Methods = {
    'Vertically Integrated Sample' : 'Vertically Integrated Sample',
    'Discrete Depth Sample' : 'Discrete Depth Sample',
    'Spatially Integrated Sample' : 'Spatially Integrated Sample',
    'Not Reported' : 'Not Reported',
}

Microcystin_Method = {
    'PPIA' : 'PPIA',
    'ELISA' : 'ELISA',
    'LC-MSMS' : 'LC-MSMS',
    'Not Reported': 'Not Reported',
}


## Data

data_Review = {
    'Yes' : 'Yes',
    'No' : 'No',
    'Not Reported': 'Not Reported',
}



ynLabels = {
    'Yes': 'Yes',
    'No': 'No',
    'Not Reported' : 'Not Reported',
}


### Options
Substrate_Status_options = [{'label': str(Substrate_Status[substrate_status]), 'value': str(substrate_status)}
                  for substrate_status in Substrate_Status]

month_Controls_options = [{'label': str(month_Controls[month_status]),
                      'value': str(month_status)}
                     for month_status in month_Controls]


Sample_Types_options = [{'label': str(Sample_Types[sample_types]),
                      'value': str(sample_types)}
                     for sample_types in Sample_Types]

Field_Methods_options = [{'label': str(Field_Methods[field_methods]),
                      'value': str(field_methods)}
                     for field_methods in Field_Methods]

Microcystin_Method_options = [{'label': str(Microcystin_Method[microcystin_method]),
                      'value': str(microcystin_method)}
                     for microcystin_method in Microcystin_Method]


lake_status_options = [{'label': str(LAKES[lake_info]),
                      'value': str(lake_info)}
                     for lake_info in LAKES]

data_Review_options = [{'label': str(data_Review[yn]),
                      'value': str(yn)}
                     for yn in data_Review]

institution_status_options = [{'label': str(INSTITUTIONS[inst_info]),
                      'value': str(inst_info)}
                     for inst_info in INSTITUTIONS]

ynOptions = [{'label': str(ynLabels[ynVal]), 'value': str(ynVal)}
                  for ynVal in ynLabels]