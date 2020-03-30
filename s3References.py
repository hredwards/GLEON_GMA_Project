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


import os
from boto.s3.connection import S3Connection
s3 = S3Connection(os.environ['S3_KEY'], os.environ['S3_SECRET'])


client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    config=Config(signature_version='s3v4'))



MasterData = client.get_object(Bucket='gleongmabucket', Key='MasterData.csv')
dfMasterData = pd.read_csv(io.BytesIO(MasterData['Body'].read()))

MetadataDB = client.get_object(Bucket='gleongmabucket', Key='MetadataDB.csv')
dfMetadataDB = pd.read_csv(io.BytesIO(MetadataDB['Body'].read()))


#print(dfMetadataDB[:10])
