"""""
This will have the data dictionaries for any filters we may use on the app. 
"""""

from s3References import client, MasterData, dfMasterData, MetadataDB, dfMetadataDB
from LakeIDGenerator import lakeNameandID

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
Substrate_Status = {
    'PL' : 'Planktronic',
    'BE' : 'Beach',
    'PE' : 'Periphyton'
}


Sample_Types = dict(
    RM = 'Routine Monitoring',
    RWC = 'Reactionary Water Column',
    SF = 'Scum Focused',
)

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

data_Review = {
    'is' : 'Yes',
    'not' : 'No',
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
