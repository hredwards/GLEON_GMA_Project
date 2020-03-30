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

