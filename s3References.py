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
from boto.s3.connection import S3Connection


Bucket='gleongmabucket'
UploadFolder='gleongmabucket/UploadedData'

session = boto3.Session(profile_name="eb-cli")
#client = session.client('s3')

#session = boto3.session.Session(aws_access_key_id=os.environ['S3_KEY'], aws_secret_access_key=os.environ['S3_SECRET'])
client = session.client('s3')



MasterData = client.get_object(Bucket='gleongmabucket', Key='MasterData.csv')
dfMasterData = pd.read_csv(io.BytesIO(MasterData['Body'].read()))

MetadataDB = client.get_object(Bucket='gleongmabucket', Key='MetadataDB.csv')
dfMetadataDB = pd.read_csv(io.BytesIO(MetadataDB['Body'].read()))


creds = client.get_object(Bucket='gleongmabucket', Key='logins.csv')
dfCreds = pd.read_csv(io.BytesIO(creds['Body'].read()))


user_pwd = dfCreds.iloc[ : , 1]
user_names = dfCreds.iloc[ : , 0]
creds = dict(zip(list(user_names), list(user_pwd)))

usersNames = dfCreds.iloc[:, 2]
#print(dfMetadataDB[:10])
