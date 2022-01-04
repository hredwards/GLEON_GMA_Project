import dash
import sys
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output


import boto3
import io
from botocore.client import Config
import pandas as pd
import os
from boto.s3.connection import S3Connection


Bucket='gleongmabucket'
UploadFolder='UploadedData/'
AssetsFolder='Assets/'


#session = boto3.Session(profile_name="eb-cli")
session = boto3.session.Session(aws_access_key_id=os.environ['S3_KEY'], aws_secret_access_key=os.environ['S3_SECRET'])
client = session.client('s3')


## MasterData and MetaData
MasterData = client.get_object(Bucket='gleongmabucket', Key='Assets/MasterData.csv')
dfMasterData = pd.read_csv(io.BytesIO(MasterData['Body'].read()))

def pullMasterdata():
    MasterData = client.get_object(Bucket='gleongmabucket', Key='Assets/MasterData.csv')
    dfMasterData = pd.read_csv(io.BytesIO(MasterData['Body'].read()))
    dfMasterData['Year'] = pd.DatetimeIndex(dfMasterData['DATETIME']).year
    dfMasterData['Month'] = pd.DatetimeIndex(dfMasterData['DATETIME']).month
    dfMasterData['Date Reported'] = pd.to_datetime(dfMasterData['DATETIME'])
    return dfMasterData

def pullMetaDB():
    MetadataDB = client.get_object(Bucket='gleongmabucket', Key='Assets/MetadataDB.csv')
    dfMetadataDB = pd.read_csv(io.BytesIO(MetadataDB['Body'].read()))
    return dfMetadataDB


MetadataDB = client.get_object(Bucket='gleongmabucket', Key='Assets/MetadataDB.csv')
dfMetadataDB = pd.read_csv(io.BytesIO(MetadataDB['Body'].read()))


## Example Datasheet
#exampleSheet = client.get_object(Bucket='gleongmabucket', Key='Assets/GLEON_GMA_Example.xlsx')
#dfexampleSheet = pd.read_excel(io.BytesIO(exampleSheet['Body'].read()))


## blank example CSV Datasheet for users to fill out
exampleSheet = client.get_object(Bucket='gleongmabucket', Key='Assets/GLEON_GMA_EXAMPLE.csv')
dfexampleSheet = pd.read_csv(io.BytesIO(exampleSheet['Body'].read()))


## Blank outline csv for graphs to reference when no filters met -- not for users
csvOutline = client.get_object(Bucket='gleongmabucket', Key='Assets/GLEON_GMA_OUTLINE.csv')
dfcsvOutline = pd.read_csv(io.BytesIO(csvOutline['Body'].read()))
dfcsvOutline.rename(columns={'Date': 'DATETIME', },
              inplace=True)

## User credentials/login
creds = client.get_object(Bucket='gleongmabucket', Key='logins.csv')
dfCreds = pd.read_csv(io.BytesIO(creds['Body'].read()))


user_pwd = dfCreds["pass"]
user_names = dfCreds["user"]
creds = dict(zip(list(user_names), list(user_pwd)))
usersNames = dfCreds["name"]
userId = dfCreds["id"]
