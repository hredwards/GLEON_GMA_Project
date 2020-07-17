"""
    Constant values utilized in Dash application
"""
import pandas as pd
import numpy as np

from s3References import client, MasterData, dfMasterData, MetadataDB, dfMetadataDB


# Read in database info from the matadata file
metadataDB = dfMetadataDB

# Establish range of months and years that exist in data
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Established microcystin limits
USEPA_LIMIT = 4
WHO_LIMIT = 20

"""
    if type(lake_name) is not list:
        lake_name = [lake_name]

    if type(substrate) is not list:
        substrate = [substrate]
    print(substrate)
    if type(microcystin_types) is not list:
        microcystin_types = [microcystin_types]

    if type(sample) is not list:
        sample = [sample]

    if type(field) is not list:
        field = [field]

    if type(filtered) is not list:
        filtered = [filtered]

    if type(institution) is not list:
        institution = [institution]

    if type(peerRev) is not list:
        peerRev = [peerRev]

    if type(fieldRep) is not list:
        fieldRep = [fieldRep]

    if type(labRep) is not list:
        labRep = [labRep]

    if type(QA) is not list:
        QA = [QA]

"""