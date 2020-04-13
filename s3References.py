""""
Variables introduced here:
client   ---- very important, this establishes client connection
MasterData ---  this pulls the csv file with ALL data aggregated in it; used for graphs on homepage from S3
dfMasterData  --- this uses panda to read the MasterData csv
MetadataDB  ---  this pulls the csv file with ALL Metadata aggregated in it
dfMetadataDB --- this uses panda to read the MetadataDB csv
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output


import boto3
import io
from botocore.client import Config
import pandas as pd
import os


Bucket='gleongmabucket'
UploadFolder="UploadedData"

session = boto3.Session(profile_name="eb-cli")


client = session.client('s3')



MasterData = client.get_object(Bucket='gleongmabucket', Key='MasterData.csv')
dfMasterData = pd.read_csv(io.BytesIO(MasterData['Body'].read()))

MetadataDB = client.get_object(Bucket='gleongmabucket', Key='MetadataDB.csv')
dfMetadataDB = pd.read_csv(io.BytesIO(MetadataDB['Body'].read()))


#print(dfMetadataDB[:10])
